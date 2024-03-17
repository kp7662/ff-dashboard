<script>
    import { Container } from 'sveltestrap';

    import Navbar from "../lib/Navbar.svelte";
    import Sidebar from "../lib/Sidebar.svelte";
    import Footer from "../lib/Footer.svelte";
  
    export let segment;
  
    let theme = "dark";
    let color = "dark";
    let title = "FF Admin";
  </script>
  
  <svelte:head>
    <title>{title}</title>
  </svelte:head>
  
  {#if segment !== 'pages'}
    <div class="sb-nav-fixed">
      <Navbar {segment} {color} {title} />
      <div id="layoutSidenav">
        <Sidebar {segment} {theme} />
        <div id="layoutSidenav_content">
          <main>
            <Container fluid={true}>
              <slot />
            </Container>
          </main>
          <Footer />
        </div>
      </div>
    </div>
  {:else}
    <body>
      <slot />
    </body>
  {/if}
  