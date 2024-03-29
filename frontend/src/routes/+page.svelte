<!-- https://github.com/consultingninja/svelteTemplateProject/blob/main/src/App.svelte -->

<!-- frontend/src/routes/+page.svelte -->
<script>
import StableStatsCard from "../lib/StableStatsCard.svelte";
import StackedColumnChart from "../lib/StackedColumnChart.svelte";
import MonthlyPayChart from "../lib/MonthlyPayChart.svelte";
import DropDownMenu from "../lib/DropDownMenu.svelte";
import DateRangePicker from "../lib/DateRangePicker.svelte"

import { Row, Breadcrumb, BreadcrumbItem } from "@sveltestrap/sveltestrap";

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
  <h5 style="margin-right: 10px;">Pick a Date Range:</h5>
  <DateRangePicker />
</div>

<div
  class="grid grid-cols-1
  grid-rows-2 md:grid-cols-4 grid-rows-2 gap-4"
>
  <!-- <AverageDurationCard class="row-span-2" cardTitle="Average Trip Duration" /> -->
  <StableStatsCard cardTitle="Total Sign-ups (Rideshare)" />
  <StableStatsCard cardTitle="Total Sign-ups (Delivery)" />
  <StableStatsCard cardTitle="Average Hourly Base Pay vs Minimum Wage" />
  <StableStatsCard cardTitle="Survey Results on “fair” take vs real (Rideshare)" />
  <StableStatsCard cardTitle="Average Tips per Delivery Order" />
  <StableStatsCard cardTitle="Average Pay per Min" />
  <StableStatsCard cardTitle="XXX" />
  <StableStatsCard cardTitle="XXX" />
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <StackedColumnChart />
  <MonthlyPayChart affiliation={$selectedAffiliation} />
</div>