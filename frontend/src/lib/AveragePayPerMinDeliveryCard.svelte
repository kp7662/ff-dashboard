<script>
    import { Card, CardBody } from '@sveltestrap/sveltestrap';
    import { selectedAffiliation, startDate, endDate } from '../lib/stores/store';
    
    export let cardTitle = "";
    let average_pay_per_minute_delivery = 'Loading...';
    let aggregate_pay_per_minute_delivery = 'Loading...';
    
    const fetchData = async () => {
        const affiliation = $selectedAffiliation; 
        const start = $startDate;
        const end = $endDate;
        const url = `http://localhost:5000/average-pay-per-min?affiliation=${affiliation}&start_date=${start}&end_date=${end}`; // Construct the URL with the selected affiliation, start_date, and end_date
        const response = await fetch(url);
        const data = await response.json();
        average_pay_per_minute_delivery = `$ ${data.average_pay_per_minute_delivery}`;
        aggregate_pay_per_minute_delivery = `$ ${data.aggregate_pay_per_minute_delivery}`;
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
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-600">{average_pay_per_minute_delivery}</span>
    </div>
    <div class="flex justify-between items-center mb-2 text-base">
    <div>Average Pay per Minute (Overall)</div>
    <div class="flex items-center text-green-500 text-base">
        {aggregate_pay_per_minute_delivery}
    </div>
    </div>
</CardBody>
</Card>
