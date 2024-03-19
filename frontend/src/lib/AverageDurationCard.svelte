<script>
  import DashboardCard from "./DashboardCard.svelte";

  import { AdminDashStore } from "./stores/store";

  $: console.log(
    "[+page.svelte] avgTripDurationCard: ",
    $AdminDashStore.averageTripDuration,
  );

  $: averageTripDuration = $AdminDashStore.averageTripDuration
    ? $AdminDashStore.averageTripDuration
    : "??";

  const updateLimit = (newLimit) => {
    AdminDashStore.update((store) => {
      store.limit = newLimit;
    });
  };
</script>

<DashboardCard cardTitle="Average Duration" cardColor="primary">
  <h1 class="text-lg font-bold">
    {averageTripDuration} minutes
  </h1>
  <p class="text-xs text-gray-600">Average trip duration</p>
</DashboardCard>
