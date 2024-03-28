import { derived, writable } from 'svelte/store';

// default affiliation
export const selectedAffiliation = writable('CIDU'); 

const defaultAdminDash = {
  averageFareTakeValue: 0,
  limit: 10,
}

function createAdminDashStore() {
  const { subscribe, set, update } = writable(defaultAdminDash);
  return {
    subscribe,
    set,
    update,
    reset: () => set(defaultAdminDash)
  };
}

export const AdminDashStore = createAdminDashStore();



//////////////////////////
// export const gigsWithFareTake = derived(adminDash, ($a) => {
//   const activities = $a.allActivities;
//   return getFilteredGigsWithNonNaNTakeRates(activities);
// });

// export const gigStats = derived(gigsWithFareTake, ($gigs) => {
//   return {
//     takeRatePct: _.meanBy($gigs, (x) => x.take_rate),
//     takeRateValue: averageFareTakeValue($gigs),
//     takeRateVariability: variabilityOfFareTake($gigs),
//     avgAndVariabilityPerDriver: averageAndVariabilityPerDriver($gigs)
//   };
// });
