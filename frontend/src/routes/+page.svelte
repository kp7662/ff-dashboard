<!-- frontend/src/routes/+page.svelte -->
<script>
import StackedColumnChart from "../lib/StackedColumnChart.svelte";
import ViolinPlot from "../lib/ViolinPlot.svelte";
import DropDownMenu from "../lib/DropDownMenu.svelte";
import DateRangePicker from "../lib/DateRangePicker.svelte"
import RideshareSignUpsCard from "../lib/RideshareSignUpsCard.svelte";
import DeliverySignUpsCard from "../lib/DeliverySignUpsCard.svelte";
import AverageTipsPerDelivery from "../lib/AverageTipsPerDeliveryCard.svelte"
import AverageTipsPerRideshare from "../lib/AverageTipsPerRideshareCard.svelte"
import AveragePayPerMinDelivery from "../lib/AveragePayPerMinDeliveryCard.svelte"
import AveragePayPerMinRideshare from "../lib/AveragePayPerMinRideshareCard.svelte"

import { Card, CardBody } from "@sveltestrap/sveltestrap";

import { selectedAffiliation } from '../lib/stores/store';

let title = "FF Admin Dashboard";

// Auto-subscribe to the store for console log.
// $: console.log('Affiliation in +page.svelte:', $selectedAffiliation);
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>


<nav class="flex flex-col justify-center px-5 py-2 text-gray-700 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-800 dark:border-gray-700 mb-4" aria-label="Breadcrumb">
  <ol class="inline-flex items-center space-x-1 md:space-x-2 rtl:space-x-reverse">
    <li aria-current="page">
      <div class="flex items-center">
        <i class="fa fa-home text-gray-400 mr-1" aria-hidden="true"></i>
        <a href="/" class="text-base font-semibold text-gray-600 dark:text-gray-400">Home</a>
      </div>
    </li>
  </ol>
</nav>


<div class="border border-gray-200 bg-white rounded-lg p-4 mb-12">
  <h2 class="mb-4 pl-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-4xl lg:text-5xl">
    Filters
  </h2>

  <div class="mb-4 pl-4">
    <h5 style="display: inline-block; margin-right: 10px;" class="mb-2 text-2xl font-base tracking-tight text-gray-900 dark:text-white">By Affiliation:</h5>
    <DropDownMenu class="pl-4" style="display: inline-block;" />
  </div>

  <div class="mb-4 pl-4" style="display: flex; align-items: center;">
    <h5 style="margin-right: 10px;" class="mb-2 text-2xl font-base tracking-tight text-gray-900 dark:text-white">By Date Range:</h5>
    <DateRangePicker class="pl-4" />
  </div>
</div>


<div class="border border-gray-200 bg-white rounded-lg p-4 mb-12">
  <h2 class="mb-12 pl-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-4xl lg:text-5xl">
    Live Stats
  </h2>

  <div
    class="grid grid-cols-1
    grid-rows-2 md:grid-cols-3 grid-rows-2 gap-3"
  >
    <RideshareSignUpsCard cardTitle="Total Drivers Sign-ups (Rideshare)" />
    <AverageTipsPerRideshare cardTitle="Average Tips per Ride (Rideshare)" />
    <AveragePayPerMinRideshare cardTitle="Average Pay per Minute (Rideshare)" />

    <DeliverySignUpsCard cardTitle="Total Drivers Sign-ups (Delivery)" />
    <AverageTipsPerDelivery cardTitle="Average Tips per Order (Delivery)" />
    <AveragePayPerMinDelivery cardTitle="Average Pay per Minute (Delivery)" />
  </div>
</div>

<div class="border border-gray-200 bg-white rounded-lg p-4 mb-12">
  <h2 class="mb-12 pl-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-4xl lg:text-5xl">
    Charts Analysis
  </h2>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
    <StackedColumnChart />
    <ViolinPlot />
  </div>
</div>

<Card class="mb-4">
  <CardBody>
    <p class="text-xl mb-4 font-bold leading-relaxed"> 
      Development in Progress
    </p>
    <p class="text-lg mb-4 leading-relaxed">
      This section is still under development. More visualizations will be displayed here in the future.
    </p>
    <p class="text-lg mb-4 leading-relaxed">
    </p>
  </CardBody>
</Card>

