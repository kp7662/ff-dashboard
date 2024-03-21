<!-- https://svelte.dev/repl/3ad4a548a4c442b69f20c25021ac8fbf?version=4.1.0 -->

<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // Define variables to hold data and chart dimensions
  let data = [];
  let width = 928 * 3;
  let height = 700 * 3;
  let marginTop = 80 * 3;
  let marginRight = 30;
  let marginBottom = 150 * 1.5; // Increased margin for better label visibility
  let marginLeft = 200 * 1.5 + 100; // Increased margin and added padding for y-axis label visibility
  let xAxisLabelPadding = 60; // Padding between x-axis labels and x-axis line

  // Function to fetch data from the backend
  async function fetchData() {
    try {
      const response = await fetch('http://localhost:5000/monthly-pay');
      const json = await response.json();
      data = json.monthly_average_pay;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  // Fetch data when the component mounts
  onMount(() => {
    fetchData();
  });

  // Define scales and line generator
  let xScale, yScale, line;

  $: {
    // Create the x (horizontal position) scale.
    xScale = d3.scaleUtc()
      .domain(d3.extent(data, d => new Date(d.year_month)))
      .range([marginLeft, width - marginRight]);

    // Create the y (vertical position) scale.
    yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.current_pay)])
      .range([height - marginBottom, marginTop]);

    // Create the line generator.
    line = d3.line()
      .x(d => xScale(new Date(d.year_month)))
      .y(d => yScale(d.current_pay));
  }
</script>

<svg
  width={width}
  height={height}
  viewBox={`0 0 ${width} ${height}`}
  style="max-width: 100%; height: auto;"
>
  <!-- Chart Title -->
  <text fill="currentColor" text-anchor="middle" x={width / 2} y={marginTop / 4} font-size="5em" font-weight="bold">
    Monthly Average Pay
  </text>

  <!-- X-Axis -->
  <g transform={`translate(0, ${height - marginBottom})`}>
    <line stroke="currentColor" x1={marginLeft} x2={width - marginRight} y1="0" y2="0" /> <!-- X-Axis Line -->
    {#each xScale.ticks() as tick}
      <!-- X-Axis Ticks -->
      <line stroke="currentColor" x1={xScale(tick)} x2={xScale(tick)} y1="0" y2="6" />
      <!-- X-Axis Tick Labels -->
      <text fill="currentColor" text-anchor="middle" x={xScale(tick)} y={xAxisLabelPadding} font-size="3em">
        {`${tick.getMonth() + 1}/${tick.getFullYear().toString().slice(2)}`}
      </text>
    {/each}
  </g>

  <!-- Y-Axis and Grid Lines -->
  <g transform={`translate(${marginLeft}, 0)`}>
    {#each yScale.ticks() as tick}
      {#if tick !== 0}
        <!-- Grid Lines -->
        <line stroke="currentColor" stroke-opacity="0.1" x1={0} x2={width - marginLeft} y1={yScale(tick)} y2={yScale(tick)} />
        <!-- Y-Axis Ticks -->
        <line stroke="currentColor" x1={0} x2={-6} y1={yScale(tick)} y2={yScale(tick)} />
      {/if}
      <!-- Y-Axis Tick Labels -->
      <text fill="currentColor" text-anchor="end" dominant-baseline="middle" x={-9} y={yScale(tick)} font-size="3em">
        {tick}
      </text>
    {/each}
    <!-- Y-Axis Label -->
    <text fill="currentColor" text-anchor="start" x={-marginLeft} y={marginTop / 4} font-size="3em">
      ↑ Average Pay ($)
    </text>
  </g>

  <!-- Draw Line -->
  {#if data.length > 0}
    <path fill="none" stroke="steelblue" stroke-width="5" d={line(data)} />
  {/if}
</svg>
