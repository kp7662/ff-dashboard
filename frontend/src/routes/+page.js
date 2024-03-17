import { AdminDashStore } from "../lib/stores/store"

export async function load(props) {
  console.log("[+page.js] input:", props)

  console.log("[+page.js] AdminDashStore:", AdminDashStore.averageTripDuration)


  // How to: change query based on URL parameters
  // i.e. you change URL to be /?numTrips=100
  const searchParams = new URLSearchParams(props.url.searchParams)
  console.log("[+page.js] searchParams:", searchParams)
  const numTripsFilter = searchParams.get("numTrips")
  console.log("[+page.js] numTripsFilter:", numTripsFilter)
  /////////
  //
  // Fix this: if there's an error, don't return error text! The page expects it to be a number
  const averageTripDurationRes = await fetch("http://localhost:5001/api/rideshare/average-trip-duration"
    // include below if e.g. you want to use url parameters to filter the data to the API server
    // (passing the numTrips param on the client to the server)
    // numTripsFilter ? { method: "POST", body: JSON.stringify({ numTrips: numTripsFilter }) } : {}
  )
    .then((r) => r.ok ? r.json() : r.text())

  const averageTripDuration = averageTripDurationRes.average_trip_duration
  console.log("[+page.js] averageTripDuration:", { averageTripDuration })
  let averageTakeRate = 0.0

  return {
    "stats": {
      averageTripDuration,
      averageTakeRate,
    },
  }
}
