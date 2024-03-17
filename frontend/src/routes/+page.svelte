<!-- https://github.com/consultingninja/svelteTemplateProject/blob/main/src/App.svelte -->

<script>
import Navbar from "$lib/Navbar.svelte";
import Footer from "../lib/Footer2.svelte";
import DashboardCard from "../lib/DashboardCard.svelte";

import { linkUtil } from "../utils/linkUtil";
import url from "../url";
// $: console.log($url);
// console.log(url); // Should log the store, not `undefined`
import { pageUtil } from "../utils/pageUtil";
import Page from "../lib/Page.svelte";

import { Row, Breadcrumb, BreadcrumbItem } from 'sveltestrap';

let title = "FF Admin Dashboard"

// Testing communicating with backend
let rand = -1;
  function getRand() {
    fetch("http://127.0.0.1:5000/rand")
      .then(d => d.text())
      .then(d => (rand = d));
  }
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>
<h1 class="mt-4">Dashboard</h1>

<!-- Testing communication with backend -->
<h1>Your number is {rand}!</h1>
<button on:click={getRand}>Get a random number</button>

<Breadcrumb class="mb-4">
  <BreadcrumbItem active>Dashboard</BreadcrumbItem>
</Breadcrumb>
<Row>
  <div class="col-xl-3 col-md-6">
    <DashboardCard cardTitle="Primary Card" cardColor="primary" />
  </div>
  <div class="col-xl-3 col-md-6">
    <DashboardCard cardTitle="Warning Card" cardColor="warning" />
  </div>
  <div class="col-xl-3 col-md-6">
    <DashboardCard cardTitle="Success Card" cardColor="success" />
  </div>
  <div class="col-xl-3 col-md-6">
    <DashboardCard cardTitle="Danger Card" cardColor="danger" />
  </div>
</Row>

















<!-- <Navbar data={linkUtil}/> -->
<!-- <Navbar2 {segment} {color} {title} />
<main>
    <h1>Hello World!</h1>
    <br>
    <Row>
        <div class="col-xl-3 col-md-6">
          <DashboardCard cardTitle="Primary Card" cardColor="primary" />
        </div>
        <div class="col-xl-3 col-md-6">
          <DashboardCard cardTitle="Warning Card" cardColor="warning" />
        </div>
        <div class="col-xl-3 col-md-6">
          <DashboardCard cardTitle="Success Card" cardColor="success" />
        </div>
        <div class="col-xl-3 col-md-6">
          <DashboardCard cardTitle="Danger Card" cardColor="danger" />
        </div>
      </Row>
    {#each pageUtil as page}
    {#if $url.hash === page.url || ($url.hash === '' && page.url === '#/')}
      <Page page={page} />
    {/if}
    {/each} -->
<!-- </main>
<Footer2 />


<style>
    main {
        min-height: calc(100vh - 4rem); /* Adjust 4rem based on navbar height */
        padding-bottom: 4rem; /* Adjust based on footer height */
        display: flex;
        justify-content: center;
        align-items: left;
        flex-direction: column;
    }

    h1 {
        margin: 0;
        font-size: 2rem; /* Adjust as needed */
    }

</style> -->