<script>
  import "../app.css";
  import { Container } from "@sveltestrap/sveltestrap";

  import Navbar from "../lib/Navbar.svelte";
  import Footer from "../lib/Footer.svelte";

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