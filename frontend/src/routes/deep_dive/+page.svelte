<!-- frontend/src/routes/time/+page.svelte -->
<script>
import {
    Breadcrumb,
    BreadcrumbItem,
    Card,
    CardBody,
    CardText,
} from "@sveltestrap/sveltestrap"

import { goto } from "$app/navigation";

</script>

<style>
button.link-button {
    background: none;
    border: none;
    color: blue;
    text-decoration: underline;
    cursor: pointer;
}
</style>

<h1 class="mt-4 mb-4">Deep Dive Analysis - Coming Soon!</h1>
<Breadcrumb class="mb-4">
  <BreadcrumbItem>
    <button class="link-button" on:click={() => goto('/')}>
      Home
    </button>
  </BreadcrumbItem>
  <BreadcrumbItem active>Deep Dive Analysis</BreadcrumbItem>
</Breadcrumb>

<Card class="mb-4">
  <CardBody>
    <p class="text-lg mb-4 leading-relaxed">
      Welcome to the "Deep Dive Analysis" page, currently under development. 
      This page is designed to provide researchers, labor organizers, and 
      rideshare workers with sophisticated data visualizations that offer deep 
      insights into critical data. Our goal is to empower our users with immediate 
      access to relevant information, enhancing advocacy efforts for fair wages and 
      improved working conditions. 
    </p>
    <p class="text-lg mb-4 leading-relaxed">
      Here, you will soon be able to explore complex datasets through intuitive 
      and comprehensive graphical representations, enabling more effective decision-making 
      and strategy development. Stay tuned as we work to bring these powerful tools 
      to your fingertips.
    </p>
    <p class="text-lg mb-4 leading-relaxed">
      Thank you for your patience as we finalize this vital resource. We are excited 
      to support your efforts in driving meaningful change in the gig economy.
    </p>
  </CardBody>
</Card>
