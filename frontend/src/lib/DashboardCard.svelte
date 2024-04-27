<script>
  export let cardTitle = "";
  export let cardColor;
  export let cardFooterText = "View Details";
  let className;

  export { className as class };
</script>

<div
  class={`border-2 shadow-md p-4 bg-white text-black row-span-1 col-span-2 ${className}`}
>
  <div>
    <div>{cardTitle}</div>
  </div>
  <div class="d-flex align-items-center justify-content-between">
    <slot />
    <div class="small text-white">
      <i class="fas fa-angle-right" />
    </div>
  </div>
</div>

