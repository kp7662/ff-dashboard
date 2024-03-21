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

import MonthlyPayChart from "../../lib/MonthlyPayChart.svelte"

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

<h1 class="mt-4">Time Analysis</h1>
<Breadcrumb class="mb-4">
<BreadcrumbItem>
    <button class="link-button" on:click={() => goto('/')}>
    Dashboard
    </button>
</BreadcrumbItem>
<BreadcrumbItem active>Time Analysis</BreadcrumbItem>
</Breadcrumb>



<Card class="mb-4">
<CardBody>
    <div class="col-xl-6">
        <MonthlyPayChart />
    </div>

    <!-- <p class="mb-0">
    This page is an example of using static navigation. By removing the
    <code>.sb-nav-fixed</code>
    class from the
    <code>body</code>
    , the top navigation and side navigation will become static on scroll.
    Scroll down this page to see an example.
    </p> -->
</CardBody>
</Card>
<div style="height: 100vh;" />
<Card class="mb-4">
<CardBody>
    When scrolling, the navigation stays at the top of the page. This is the end
    of the static navigation demo.
</CardBody>
</Card>
