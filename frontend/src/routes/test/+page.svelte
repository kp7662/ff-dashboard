<script>
import DropDownMenu from "../../lib/DropDownMenu.svelte";
import StoreTest from '../../lib/StoreTest.svelte';
import { selectedAffiliation } from '../../lib/stores/store';

let testCounter = 0;
$: console.log('Affiliation in +page.svelte:', $selectedAffiliation, testCounter);

function incrementCounter() {
    testCounter += 1;
    selectedAffiliation.update(n => n); // This line doesn't change the value but should trigger subscribers.
}
</script>

<h1>Hello World</h1>
<!-- <StoreTest /> -->
<DropDownMenu />

<p>Selected Affiliation: {$selectedAffiliation}</p>

<button on:click={incrementCounter}>Increment Counter</button>
