<script>
    import { onMount } from 'svelte';
    
    let categories = [];
    let selectedDetail = null;
    let displayTimeout;

function showDetail(payItem) {
    clearTimeout(displayTimeout); // Clear any existing timeout to avoid premature hiding
    selectedDetail = payItem;

    // Set a timeout to clear the selectedDetail after 3 seconds (3000 milliseconds)
    displayTimeout = setTimeout(() => {
        selectedDetail = null;
    }, 3000);
}

// A simple mapping of income types to color classes
const colorMap = {
    'income_pay': 'bg-red-500',
    'income_tips': 'bg-green-500',
    'income_bonus': 'bg-blue-500',
    'income_fees': 'bg-yellow-500'
};

onMount(async () => {
    const response = await fetch('http://127.0.0.1:5000/pay-breakdown');
    if (response.ok) {
        const fetchedData = await response.json();
        
        // Transform fetched data, computing percentages for each pay type and retaining the type
        categories = fetchedData.map(category => {
            const totalIncome = category.pay.reduce((sum, payItem) => sum + payItem.amount, 0);
            const payWithPercentages = category.pay.map(payItem => ({
                type: payItem.type, // Retain the type of each income breakdown
                amount: (payItem.amount / totalIncome) * 100, // Convert amount to percentage of total
                color: colorMap[payItem.type] || 'bg-gray-400' // Map type to a color, fallback to gray
            }));
            
            return {
                ...category,
                pay: payWithPercentages
            };
        });
        
    } else {
        console.error('Failed to fetch data from the API');
    }
});

</script>

<style>
    .pay-segment:hover {
      opacity: 0.7;
      cursor: pointer;
    }
</style>

<div class="w-full">
    <div class="flex flex-col items-center w-full bg-white rounded-lg shadow-xl p-4" style="min-height: 450px;">
        <h2 class="text-xl font-bold">Avg. Income Breakdown by Category (Percentages)</h2>
        <span class="text-sm font-semibold text-gray-500">Live data from the database</span>
    <div class="flex items-end flex-grow w-full mt-2 space-x-2 sm:space-x-3">
        {#each categories as { name, pay }}
            <div class="flex flex-col items-center w-full">
                <div class="relative flex flex-col items-center w-full h-64">
                    {#each pay as payItem}
                    <!-- Accessibility feature -->
                        <button 
                            type="button" 
                            on:click={() => showDetail(payItem)}
                            class={`w-full relative flex items-center justify-center ${payItem.color} pay-segment focus:outline-none border-none p-0`} 
                            style="height: {payItem.amount}%;"
                            aria-label={`Show details for ${payItem.type}`}>
                            <span class="text-xs text-white absolute z-10">{Math.round(payItem.amount)}%</span>
                        </button>
                    {/each}
                </div>
                <span class="text-xs font-bold mt-2">{name}</span>
            </div>
        {/each}
    </div>
    {#if selectedDetail}
        <div class="absolute top-0 left-1/2 transform -translate-x-1/2 mt-4 p-2 border rounded shadow-lg bg-white" style="z-index: 50;">
            <p><strong>Type:</strong> {selectedDetail.type.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Amount:</strong> {selectedDetail.amount.toFixed(2)}%</p>
        </div>
    {/if}
    <div class="flex justify-center space-x-4 mt-4">
        <div class="flex items-center"><div class="w-4 h-4 bg-red-500"></div><span class="ml-2">Income Pay</span></div>
        <div class="flex items-center"><div class="w-4 h-4 bg-green-500"></div><span class="ml-2">Income Tips</span></div>
        <div class="flex items-center"><div class="w-4 h-4 bg-blue-500"></div><span class="ml-2">Income Bonus</span></div>
        <div class="flex items-center"><div class="w-4 h-4 bg-yellow-500"></div><span class="ml-2">Income Fees</span></div>
    </div>
</div>
</div>
