<script>
    import { Card, CardBody } from '@sveltestrap/sveltestrap';
    import { selectedAffiliation, startDate, endDate } from '../lib/stores/store';
    
    export let cardTitle = "";
    let average_tip_percentage = 'Loading...';
    let average_tip_value = 'Loading...';
    let aggregate_tip_value = 'Loading...';
    
    const fetchData = async () => {
        const affiliation = $selectedAffiliation;
        const start = $startDate;
        const end = $endDate;
        const url = `http://localhost:5000/average-tips-per-delivery?affiliation=${affiliation}&start_date=${start}&end_date=${end}`; // Construct the URL with the selected affiliation, start_date, and end_date
        const response = await fetch(url);
        const data = await response.json();
        average_tip_percentage = `${data.average_tip_percentage_per_delivery_order}%`;
        average_tip_value = `$ ${data.average_tip_value_per_delivery_order}`;
        aggregate_tip_value = `$ ${data.aggregate_tip_value_delivery}`;
    };
    
    // Fetch data initially when the component is mounted
    fetchData();
    
    // Watch for changes in the selected affiliation, start_date, and end_date and update totalSignUps accordingly
    $: {
        $selectedAffiliation;
        $startDate;
        $endDate;
        fetchData();
    }
</script>

<Card class="flex flex-col border-0 shadow-lg font-sans">
<CardBody class="p-4">
    <div class="flex items-center justify-between">
    <div class="text-xl font-semibold">{cardTitle}</div>
    </div>

    <div class="text-5xl font-bold my-3">
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-600">{average_tip_percentage}</span>
    </div>

    <!-- Display actual value -->
    <div class="flex justify-between items-center mb-2 text-base">
    <div>Average Tip (by Affiliation)</div>
    <div class="flex items-center text-green-500 text-base">
        {average_tip_value}
    </div>
    </div>

    <!-- Display aggregate value for comparison -->
    <div class="flex justify-between items-center mb-2 text-base">
        <div>Average Tip (Overall)</div>
        <div class="flex items-center text-green-500 text-base">
            {aggregate_tip_value}
        </div>
        </div>
</CardBody>
</Card>
