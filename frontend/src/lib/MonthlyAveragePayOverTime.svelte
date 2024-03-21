<!-- frontend/src/lib/MonthlyPayChart.svelte -->
<script>
    import { onMount } from 'svelte';
    let Chart;
    let chartData = [];
  
    // Conditionally import svelte-apexcharts if running in the browser environment
    if (typeof window !== 'undefined') {
      // Dynamically import the module
      import('svelte-apexcharts').then(module => {
        Chart = module.Chart;
      }).catch(error => {
        console.error('Error importing svelte-apexcharts:', error);
      });
    }
  
    onMount(async () => {
      console.log('Attempting to fetch data...');
      try {
        const response = await fetch('http://localhost:5000/monthly-pay');
        console.log('Response status:', response.status);
        const responseData = await response.json();
        console.log('Fetched data:', responseData);
  
        // Parse fetched data and calculate average monthly pay
        const rideshareData = responseData.rideshare_data;
        const processedData = processData(rideshareData);
        console.log('Processed data:', processedData);
        chartData = processedData.monthly_average_pay;
        console.log('Chart data:', chartData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    });
  
    // Function to process fetched data and calculate average monthly pay
    function processData(data) {
      const rideshare_df = data.map(entry => ({
        current_pay: parseFloat(entry.current_pay),
        start_datetime: new Date(entry.start_datetime)
      }));
      
      rideshare_df.forEach(entry => {
        entry.start_datetime.setDate(1); // Set day to 1st to get the year and month accurately
      });
  
      // Group data by year and month
      const monthlyData = {};
      rideshare_df.forEach(entry => {
        const yearMonth = entry.start_datetime.toISOString().slice(0, 7); // Format: 'YYYY-MM'
        if (!monthlyData[yearMonth]) {
          monthlyData[yearMonth] = [];
        }
        monthlyData[yearMonth].push(entry.current_pay);
      });
  
      // Calculate monthly average pay
      const monthlyAveragePay = Object.entries(monthlyData).map(([yearMonth, pays]) => ({
        year_month: yearMonth,
        average_pay: pays.reduce((acc, pay) => acc + pay, 0) / pays.length
      }));
  
      return { monthly_average_pay: monthlyAveragePay };
    }
  </script>
  
  <style>
    /* Add your custom CSS styles here if needed */
    .monthly-pay-chart {
      /* Add your styles for the chart container */
    }
  </style>
  
  <div class="monthly-pay-chart">
    {#if Chart && chartData.length > 0}
      <!-- Render the Chart component if it's available and chartData is not empty -->
      <Chart type="area" series={[{ name: 'Monthly Average Pay', data: chartData.map(entry => ({ x: entry.year_month, y: entry.average_pay })) }]} />
    {:else}
      <!-- Provide a placeholder or loading indicator -->
      <p>Loading chart...</p>
    {/if}
  </div>
  