
<!-- tailwindcss.com/docs/grid-template-columns -->
<!-- frontend/src/lib/DropDownManu.svelte -->

<script>
import { selectedAffiliation } from '../lib/stores/store';
import { onMount } from 'svelte';

// Local component state for the selected affiliation label
let selectedAffiliationLabel = 'CIDU';

// Function to handle affiliation selection
function handleAffiliationChange(event) {
    const affiliation = event.target.dataset.affiliation;
    console.log('Selected affiliation:', affiliation); // Log for debugging
    selectedAffiliation.set(affiliation);
    // Update the button label to reflect the selected affiliation
    selectedAffiliationLabel = affiliation || 'Select Affiliation';
}

// Ensure the label updates if the selected affiliation changes outside this component
onMount(() => {
    selectedAffiliation.subscribe((value) => {
        selectedAffiliationLabel = value || 'Select Affiliation';
        // console.log('Selected affiliation changed to:', value);
    });
});
</script>

<button id="dropdownHoverButton" data-dropdown-toggle="dropdownHover" data-dropdown-trigger="hover" 
    class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 
        font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 
        dark:hover:bg-blue-700 dark:focus:ring-blue-800" type="button">
    {selectedAffiliationLabel}
    <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" 
    fill="none" viewBox="0 0 10 6">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
    </svg>
</button>

<!-- Dropdown menu -->
<div id="dropdownHover" class="z-10 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-64 dark:bg-gray-700">
    <ul class="py-2 text-base text-gray-700 dark:text-gray-200" aria-labelledby="dropdownHoverButton">
        <li>
            <button data-affiliation="CIDU" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">CIDU</button>
        </li>
        <li>
            <button data-affiliation="RDU" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">RDU</button>
        </li>
        <li>
            <button data-affiliation="DU" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">DU</button>
        </li>
        <li>
            <button data-affiliation="CDU" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">CDU</button>
        </li>
        <li>
            <button data-affiliation="DDA" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">DDA</button>
        </li>
        <li>
            <button data-affiliation="Unaffiliated" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">Unaffiliated</button>
        </li>
        <li>
            <button data-affiliation="All" on:click={handleAffiliationChange} class="block px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left">All</button>
        </li>
    </ul>
</div>
    