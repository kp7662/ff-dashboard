<script lang="ts">
    import {
      Card,
      CardBody,
      CardFooter,
      CardHeader,
      CardSubtitle,
      CardText,
      CardTitle
    } from '@sveltestrap/sveltestrap';
  
    export let cardTitle = "";
    export let cardSubtitle = "";
    export let cardContent = "";
    export let cardFooter = "";
  
    // Colorado Independent Drivers United, Rideshare Drivers United, Drivers Union, 
    // Connecticut Drivers United, DMV Drivers Alliance, Unaffiliated
    let affiliations = ['CIDU', 'RDU', 'DU', 'CDU', 'DDA', 'Unaffiliated'];
    let selectedAffiliation = affiliations[0]; // Default to the first affiliation
  
    function handleAffiliationChange(event) {
      selectedAffiliation = event.target.value;
    }
  </script>
  
  <div class="border-2 shadow-md p-4 bg-white text-black row-span-1 col-span-2">
    <Card>
      <CardHeader>
        <div class="flex justify-between items-center">
          <CardTitle>{cardTitle}</CardTitle>
          <select on:change={handleAffiliationChange} class="ml-auto">
            {#each affiliations as affiliation}
              <option value={affiliation}>{affiliation}</option>
            {/each}
          </select>
        </div>
      </CardHeader>
      <CardBody>
        <CardSubtitle>{cardSubtitle}</CardSubtitle>
        <CardText>{cardContent} Hello World</CardText>
      </CardBody>
      <CardFooter>{cardFooter}</CardFooter>
    </Card>
  </div>
  