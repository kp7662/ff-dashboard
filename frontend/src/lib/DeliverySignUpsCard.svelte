<script>
    import { Card, CardBody } from '@sveltestrap/sveltestrap';
    import { selectedAffiliation, startDate, endDate } from '../lib/stores/store';
    
    export let cardTitle = "";
    let totalSignUps = 'Loading...';
    let lastUpdated = 'Fetching...';
    
    const fetchData = async () => {
        const affiliation = $selectedAffiliation;
        const start = $startDate;
        const end = $endDate;
        const url = `http://localhost:5000/delivery-sign-ups?affiliation=${affiliation}&start_date=${start}&end_date=${end}`; // Construct the URL with the selected affiliation, start_date, and end_date
        const response = await fetch(url);
        const data = await response.json();
        totalSignUps = data.total_sign_ups;
        lastUpdated = new Date(data.last_updated).toLocaleDateString('en-US', {
        year: '2-digit',
        month: '2-digit',
        day: '2-digit'
        });
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
    <div class="text-xl font-semibold">{cardTitle}
    </div>
    </div>

    <div class="text-5xl font-bold my-3">
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-600">{totalSignUps}</span>
    </div>
    
    <!-- Display the last updated time -->
    <div class="flex justify-between items-center mb-2 text-base">
    <div>Last Updated</div>
    <div class="flex items-center text-green-500 text-base">
        {lastUpdated}
    </div>
    </div>
</CardBody>
</Card>
