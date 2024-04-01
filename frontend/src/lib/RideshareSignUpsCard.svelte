<script>
import { onMount } from 'svelte';
import { Card, CardBody } from '@sveltestrap/sveltestrap';

export let cardTitle = "";
let totalSignUps = 'Loading...'; // Placeholder text while fetching data
let lastUpdated = 'Fetching...'; // Placeholder for the last updated time

onMount(async () => {
    const response = await fetch('http://localhost:5000/rideshare-sign-ups');
    const data = await response.json();
    totalSignUps = data.total_sign_ups; // Display the raw number of total sign-ups
    lastUpdated = new Date(data.last_updated).toLocaleDateString('en-US', {
        year: '2-digit',
        month: '2-digit',
        day: '2-digit'
        });
});
</script>

<Card class="flex flex-col border-0 shadow-lg">
<CardBody class="p-4">
    <div class="flex items-center justify-between">
    <div class="text-lg font-semibold">{cardTitle}</div>
    </div>

    <div class="text-4xl font-bold my-3">{totalSignUps}</div>

    <!-- Updated to display lastUpdated instead of a static value -->
    <div class="flex justify-between items-center mb-2">
    <div>Last Updated</div>
    <div class="flex items-center text-green-500">
        {lastUpdated}
    </div>
    </div>
</CardBody>
</Card>
