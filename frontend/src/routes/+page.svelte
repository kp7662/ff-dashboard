<!-- https://github.com/consultingninja/svelteTemplateProject/blob/main/src/App.svelte -->

<script>
  import Navbar from "$lib/Navbar.svelte";
  import Footer from "../lib/Footer2.svelte";
  import DashboardCard from "../lib/DashboardCard.svelte";
  import Card from "../lib/Card.svelte"
  import StackedColumnChart from "../lib/StackedColumnChart.svelte"

  import { linkUtil } from "../utils/linkUtil";
  import url from "../url";
  // $: console.log($url);
  // console.log(url); // Should log the store, not `undefined`
  import { pageUtil } from "../utils/pageUtil";
  import Page from "../lib/Page.svelte";

  import { Row, Breadcrumb, BreadcrumbItem } from "@sveltestrap/sveltestrap";
  import AverageDurationCard from "../lib/AverageDurationCard.svelte";

  import { AdminDashStore } from "../lib/stores/store";

  export let data;

  const { stats } = data;

  console.log("[+page.svelte] avgTripDuration: ", stats.averageTripDuration);

  AdminDashStore.set({
    ...AdminDashStore,
    averageTripDuration: stats.averageTripDuration,
  });

  $: console.log(
    "[+page.svelte] AdminDashStore: ",
    $AdminDashStore.averageTripDuration,
  );

  // this promise/fetch is now dependent on the store, and will re-fetch
  // whenever $AdminDashStore.limit changes
  // look (online) for something like 'svete fetch dependent on store' and I'm
  // sure you'll find resources!
  $: averageTripDurationPromise = fetch(
    "http://localhost:5000/api/rideshare/average-trip-duration",
    {
      method: "POST",
      body: JSON.stringify({ limit: $AdminDashStore.limit || null }),
    },
  ).then((r) => (r.ok ? r.json() : r.text()));

  // $: averageTripDuration = $averageTripDurationPromise.then((d) => {
  //   console.log("[+page.svelte] avgTripDuration (from store): ", d);
  //   return d;
  // });

  let title = "FF Admin Dashboard";

  // Testing communicating with backend
  let rand = -1;
  function getRand() {
    fetch("http://127.0.0.1:5000/rand")
      .then((d) => d.text())
      .then((d) => (rand = d));
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
<div
  class="grid grid-cols-1
  grid-rows-4 md:grid-cols-4 grid-rows-1 gap-4"
>
  <!-- <AverageDurationCard class="row-span-2" cardTitle="Average Trip Duration" /> -->
  <Card cardTitle="Total Number of Rideshare Drivers Sign-ups" />
  <Card cardTitle="Average Take Rate" />
  <Card cardTitle="Average Pay per Mile" />
  <Card cardTitle="Danger Card" />
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <StackedColumnChart />
  <StackedColumnChart />
</div>