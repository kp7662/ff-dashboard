<script>
  import { Card, CardBody } from '@sveltestrap/sveltestrap';
  import { writable } from 'svelte/store';

  export let cardTitle = ""; // Prop for card title
  let affiliations = ['CIDU', 'RDU', 'DU', 'CDU', 'DDA', 'Unaffiliated'];
  let selectedAffiliation = writable(affiliations[0]);

  async function fetchAffiliationData(affiliation) {
    console.log(`Fetching data for ${affiliation}`);
  }

  function handleAffiliationChange(event) {
    selectedAffiliation.set(event.target.value);
  }

  $: if ($selectedAffiliation) {
    fetchAffiliationData($selectedAffiliation);
  }
</script>

<Card class="flex flex-col border-0 shadow-lg">
  <CardBody class="p-4">
    <div class="flex items-center justify-between">
      <div class="text-lg font-semibold">{cardTitle}</div>
      <div class="relative">
        <select 
          class="py-1 px-2 text-secondary bg-white border rounded-md shadow-sm" 
          onchange={handleAffiliationChange}
        >
          {#each affiliations as affiliation}
            <option value={affiliation}>{affiliation}</option>
          {/each}
        </select>
      </div>
    </div>
    
    <div class="text-4xl font-bold my-3">75%</div>

    <div class="flex justify-between items-center mb-2">
      <div>Conversion rate</div>
      <div class="flex items-center text-green-500">
        7% <!-- You can include an icon here -->
      </div>
    </div>
  </CardBody>
</Card>
