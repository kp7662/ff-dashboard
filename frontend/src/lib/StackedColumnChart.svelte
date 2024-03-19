<!-- <script>
import { onMount } from 'svelte';

let categories = [];
let maxAmount = 0;

onMount(async () => {
    const response = await fetch('http://127.0.0.1:5000/pay-breakdown');
    if (response.ok) {
    const fetchedData = await response.json();
    console.log("Fetched data:", fetchedData);

    // Transform the fetched data into the expected format
    categories = fetchedData.map(item => {
        console.log(`Processing category: ${item.name}`); // Log each category being processed
        const transformedPay = item.pay.map(p => {
        console.log(`Amount for ${item.name}: ${p.amount}, Color: ${p.color}`); // Log each payment entry
        return {
            amount: p.amount,
            color: p.color
        };
        });

        return {
        name: item.name,
        pay: transformedPay
        };
    });

    // Find the maximum pay amount across all categories and payments
    maxAmount = Math.max(...categories.flatMap(category => category.pay.map(p => p.amount)));
    console.log("Max amount:", maxAmount); // Log the calculated maximum amount

    // Log the final transformed categories array
    console.log("Transformed categories for chart:", categories);
    } else {
    console.error('Failed to fetch data from the API');
    }
});
</script> -->

<!-- <style>
.group:hover .group-hover\:block {
    display: block;
}
</style> -->
  
  
<!-- <div>
<div class="flex flex-col items-center w-full max-w-screen-md p-6 pb-6 bg-white rounded-lg shadow-xl sm:p-8">
    <h2 class="text-xl font-bold">Pay Breakdown by Category (Rideshare & Delivery)</h2>
    <span class="text-sm font-semibold text-gray-500">2023</span>
    <div class="flex items-end flex-grow w-full mt-2 space-x-2 sm:space-x-3">
    {#each categories as { name, pay }}
        <div class="relative flex flex-col items-center flex-grow pb-5 group">
        {#each pay as { amount, color }}
            <div class={`relative flex justify-center w-full ${color}`} style="height: {100 * amount / maxAmount}%;">
            </div>
        {/each}
        <span class="absolute bottom-0 text-xs font-bold">{name}</span>
        </div>
    {/each}
    </div>
</div>
</div> -->

<!-- ///////////////////////////////////// -->
<script>
import { onMount } from 'svelte';

let categories = [
    {
    name: "Rideshare",
    pay: [
        { amount: 9.209225, color: 'bg-red-500', staticHeight: '100px' },
        { amount: 1.29878, color: 'bg-green-500', staticHeight: '80px' },
        { amount: 2.958838356164383, color: 'bg-blue-500', staticHeight: '60px' },
        { amount: 7.339930000000001, color: 'bg-yellow-500', staticHeight: '40px' }
    ]
    },
    {
    name: "Delivery",
    pay: [
        { amount: 4.682063572149344, color: 'bg-red-500', staticHeight: '120px' },
        { amount: 4.83602, color: 'bg-green-500', staticHeight: '90px' },
        { amount: 0.8981390486147414, color: 'bg-blue-500', staticHeight: '70px' },
        { amount: 0.30205499999999996, color: 'bg-yellow-500', staticHeight: '50px' }
    ]
    }
];
console.log("Categories ", categories);
</script>

<style>
.group:hover .group-hover\:block {
    display: block;
}
</style>

<div>
<div class="flex flex-col items-center w-full max-w-screen-md p-6 pb-6 bg-white rounded-lg shadow-xl sm:p-8">
    <h2 class="text-xl font-bold">Pay Breakdown by Category (Rideshare & Delivery)</h2>
    <span class="text-sm font-semibold text-gray-500">2023</span>
    <div class="flex items-end flex-grow w-full mt-2 space-x-2 sm:space-x-3">
    {#each categories as { name, pay }}
        <div class="relative flex flex-col items-center flex-grow pb-5 group">
        {#each pay as { color, staticHeight }}
            <div class={`relative flex justify-center w-full ${color}`} style="height: {staticHeight};"></div>
        {/each}
        <span class="absolute bottom-0 text-xs font-bold">{name}</span>
        </div>
    {/each}
    </div>
</div>
</div>