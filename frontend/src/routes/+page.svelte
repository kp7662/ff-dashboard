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

import { Breadcrumb, BreadcrumbItem } from "@sveltestrap/sveltestrap";

import { selectedAffiliation } from '../lib/stores/store';

let title = "FF Admin Dashboard";

// Auto-subscribe to the store for console log.
$: console.log('Affiliation in +page.svelte:', $selectedAffiliation);
</script>


<svelte:head>
  <title>{title}</title>
</svelte:head>
<h1 class="mt-4">Overview</h1>

<Breadcrumb class="mb-4">
  <BreadcrumbItem active>Dashboard</BreadcrumbItem>
</Breadcrumb>

<div class="mb-8">
  <h5 style="display: inline-block; margin-right: 10px;">Select an Affiliation:</h5>
  <DropDownMenu style="display: inline-block;" />
</div>

<div class="mb-8" style="display: flex; align-items: center;">
  <h5 style="margin-right: 10px;">Select a Date Range:</h5>
  <DateRangePicker />
</div>

<div
  class="grid grid-cols-1
  grid-rows-2 md:grid-cols-3 grid-rows-2 gap-3"
>
  <RideshareSignUpsCard cardTitle="Total Drivers Sign-ups (Rideshare)" />
  <AverageTipsPerRideshare cardTitle="Average Tips per Order (Rideshare)" />
  <AveragePayPerMinRideshare cardTitle="Average Pay per Minute (Rideshare)" />

  <DeliverySignUpsCard cardTitle="Total Drivers Sign-ups (Delivery)" />
  <AverageTipsPerDelivery cardTitle="Average Tips per Order (Delivery)" />
  <AveragePayPerMinDelivery cardTitle="Average Pay per Minute (Delivery)" />
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
  <StackedColumnChart />
  <ViolinPlot />
</div>