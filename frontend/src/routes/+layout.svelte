<script>
  import "../app.css";
  import { Container } from "@sveltestrap/sveltestrap";

  import Navbar from "../lib/Navbar.svelte";
  import Footer from "../lib/Footer.svelte";

  import { onMount } from 'svelte';

  // Function to set background color on mount
  onMount(() => {
    document.body.style.backgroundColor = '#fcf8fb';
  });

  let title = "FF Admin";

</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="flex flex-col min-h-screen">
  <Navbar />
  <main class="flex-grow">
    <Container fluid>
      <slot></slot>
    </Container>
  </main>
  <Footer class="mt-auto" />
</div>