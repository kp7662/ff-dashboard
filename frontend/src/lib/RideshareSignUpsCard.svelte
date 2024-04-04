<script>
import { Card, CardBody } from '@sveltestrap/sveltestrap';
import { selectedAffiliation, startDate, endDate } from '../lib/stores/store';

export let cardTitle = "";
let totalSignUps = 'Loading...'; // Placeholder text while fetching data
let lastUpdated = 'Fetching...'; // Placeholder for the last updated time

const fetchData = async () => {
    const affiliation = $selectedAffiliation; // Get the selected affiliation from the store
    const start = $startDate; // Get the selected start date from the store
    const end = $endDate; // Get the selected end date from the store
    // console.log("Fetching data for affiliation:", affiliation);
    // console.log("Start Date:", start);
    // console.log("End Date:", end);
    const url = `http://localhost:5000/rideshare-sign-ups?affiliation=${affiliation}&start_date=${start}&end_date=${end}`; // Construct the URL with the selected affiliation, start_date, and end_date
    console.log("URL:", url);
    const response = await fetch(url); // Fetch data from the constructed URL
    const data = await response.json();
    console.log("Received data:", data);
    totalSignUps = data.total_sign_ups; // Display the raw number of total sign-ups
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
    console.log("Selected affiliation changed:", $selectedAffiliation);
    console.log("Start Date changed:", $startDate);
    console.log("End Date changed:", $endDate);
    fetchData();
}
</script>

<Card class="flex flex-col border-0 shadow-lg">
<CardBody class="p-4">
    <div class="flex items-center justify-between">
    <div class="text-lg font-semibold">{cardTitle}</div>
    </div>

    <div class="text-4xl font-bold my-3">{totalSignUps}</div>

    <!-- Display the last updated time -->
    <div class="flex justify-between items-center mb-2">
    <div>Last Updated</div>
    <div class="flex items-center text-green-500">
        {lastUpdated}
    </div>
    </div>
</CardBody>
</Card>
