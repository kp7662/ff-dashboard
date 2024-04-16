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

<h1 class="mt-4 mb-4">Time Analysis - Coming Soon!</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
    <button class="link-button" on:click={() => goto('/')}>
        Home
    </button>
    </BreadcrumbItem>
    <BreadcrumbItem active>Time Analysis</BreadcrumbItem>
</Breadcrumb>

<Card class="mb-4">
<CardBody>
    <p class="text-lg mb-4 leading-relaxed">
    Welcome to the "Time Analysis" page, a dedicated space for exploring 
    visualizations of data collected over various time intervals. This page is 
    designed to empower researchers, analysts, and policy makers with dynamic insights 
    into temporal data trends for more informed decision-making.
    </p>
    <p class="text-lg mb-4 leading-relaxed">
    Through interactive and detailed charts, you will be able to track changes, 
    understand patterns, and derive conclusions from datasets extended across 
    different periods. Our tools are intended to help you visualize the progression 
    and impacts of different variables over time.
    </p>
    <p class="text-lg mb-4 leading-relaxed">
    We appreciate your patience as we continue to enhance and develop this page. 
    Stay tuned for updates and new features that will further enhance your 
    analytical capabilities.
    </p>
</CardBody>
</Card>
      