<script>
    import { onMount } from 'svelte';
    let items = [];
  
    onMount(async () => {
      const response = await fetch('http://localhost:5000/api/data');
      if (response.ok) {
        const data = await response.json();
        items = data.items;
      } else {
        console.error('Failed to fetch:', response.statusText);
      }
    });
  </script>
  
  <main>
    <h1>Data from Flask API</h1>
    {#if items.length > 0}
      <ul>
        {#each items as item}
          <li>{item.id}: {item.name} - {item.value}</li>
        {/each}
      </ul>
    {:else}
      <p>Loading data or no data available...</p>
    {/if}
  </main>
  