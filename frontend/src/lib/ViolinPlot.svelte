<script>
    import { onMount } from 'svelte';
    let imageUrl = '';
  
    onMount(async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/view-plot');
        if (response.ok) {
          const data = await response.json();
          imageUrl = data.image;
        } else {
          console.error('Failed to fetch plot:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching the plot:', error);
      }
    });
  </script>
  
  <div class="flex flex-col items-center w-full bg-white rounded-lg shadow-xl p-4">
      <h2 class="text-xl font-bold">Driver Perception of Uber Fees</h2>
      <span class="text-sm font-semibold text-gray-500">Drivers' perceptions mirror the maximum fees taken from their fares, while the fair fee they want is less than what platforms take.</span>
      {#if imageUrl}
          <img src="{imageUrl}" alt="Driver Perception of Uber Fees" class="mt-2"/>
      {:else}
          <p>Loading plot...</p>
      {/if}
  </div>
  
  <style>
    img {
      max-width: 100%;
      height: auto;
    }
  </style>
  