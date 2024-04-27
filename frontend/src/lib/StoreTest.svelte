<script>
    import { selectedAffiliation } from '../lib/stores/store';

    function updateAffiliation(newAffiliation) {
        selectedAffiliation.set(newAffiliation);
    }
</script>

<div>
    <p>Current Affiliation: {$selectedAffiliation}</p>
    <button on:click={() => updateAffiliation('CIDU')}>Set to CIDU</button>
    <button on:click={() => updateAffiliation('RDU')}>Set to RDU</button>
    <button on:click={() => updateAffiliation('DU')}>Set to DU</button>
</div>
