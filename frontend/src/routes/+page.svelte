<!-- frontend/src/routes/+page.svelte -->
<!-- https://github.com/consultingninja/svelteTemplateProject/blob/main/src/App.svelte -->

<script>
  import Navbar from "$lib/Navbar.svelte";
  import Footer from "../lib/Footer2.svelte";
  import DashboardCard from "../lib/DashboardCard.svelte";
  import StableStatsCard from "../lib/StableStatsCard.svelte"
  import StackedColumnChart from "../lib/StackedColumnChart.svelte"
  import MonthlyPayChart from "../lib/MonthlyPayChart.svelte"

  import { Row, Breadcrumb, BreadcrumbItem } from "@sveltestrap/sveltestrap";
  import AverageDurationCard from "../lib/AverageDurationCard.svelte";

  // import { AdminDashStore } from "../lib/stores/store";

  // export let data;

  // const { stats } = data;

  // console.log("[+page.svelte] avgTripDuration: ", stats.averageTripDuration);
  // console.log('[+page.svelte] Loaded: Time Page');

  // AdminDashStore.set({
  //   ...AdminDashStore,
  //   averageTripDuration: stats.averageTripDuration,
  // });

  // $: console.log(
  //   "[+page.svelte] AdminDashStore: ",
  //   $AdminDashStore.averageTripDuration,
  // );

  // this promise/fetch is now dependent on the store, and will re-fetch
  // whenever $AdminDashStore.limit changes
  // look (online) for something like 'svete fetch dependent on store' and I'm
  // sure you'll find resources!
  // $: averageTripDurationPromise = fetch(
  //   "http://localhost:5000/rideshare/average-trip-duration",
  //   {
  //     method: "POST",
  //     body: JSON.stringify({ limit: $AdminDashStore.limit || null }),
  //   },
  // ).then((r) => (r.ok ? r.json() : r.text()));

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
<h6>Your number is {rand}!</h6>
<button on:click={getRand}>Get a random number</button>

<Breadcrumb class="mb-4">
  <BreadcrumbItem active>Dashboard</BreadcrumbItem>
</Breadcrumb>
<div
  class="grid grid-cols-1
  grid-rows-2 md:grid-cols-4 grid-rows-2 gap-4"
>
  <!-- <AverageDurationCard class="row-span-2" cardTitle="Average Trip Duration" /> -->
  <StableStatsCard cardTitle="Total Number of Rideshare Drivers Sign-ups" />
  <StableStatsCard cardTitle="Total Number of Delivery Drivers Sign-ups" />
  <StableStatsCard cardTitle="Average Take Rate" />
  <StableStatsCard cardTitle="Survey Results on “fair” take vs real" />
  <StableStatsCard cardTitle="Average Pay per Mile" />
  <StableStatsCard cardTitle="Average Pay per Minute/Hour" />
  <StableStatsCard cardTitle="Customer Rate per Mile/Minute" />
  <StableStatsCard cardTitle="XXX" />
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <StackedColumnChart />
  <MonthlyPayChart />
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <!-- <MonthlyPayChart /> -->
</div>
