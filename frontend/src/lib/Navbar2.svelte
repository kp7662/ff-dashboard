<script>
  import {
    Navbar,
    NavbarBrand,
    Nav,
    ListGroup,
    Form,
    InputGroup,
    Label,
    Input,
    Button,
    Dropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem,
  } from "@sveltestrap/sveltestrap";

  export let color;
  export let title;

  let isOpen = false; // state to control the dropdown

  function searchHandle(event) {
    event.preventDefault();
  }

  function toggleDropdown() {
    isOpen = !isOpen; // toggles the dropdown open state
  }
</script>

<Navbar class="sb-topnav navbar-expand" {color} dark expand="md">
  <NavbarBrand href=".">{title}</NavbarBrand>
  <Nav class="ml-auto" navbar>
    <!-- <Form inline on:submit={searchHandle}>
        <InputGroup>
          <Input
            type="search"
            name="search"
            id="exampleSearch"
            placeholder="Search for..."
            aria-label="Search" />
          <Button color="primary" type="submit">
            <i class="fas fa-search" />
          </Button>
        </InputGroup>
      </Form> -->
    <!-- <ListGroup class="ml-auto ml-md-0">
      <Dropdown {isOpen} toggle={toggleDropdown}>
        <DropdownToggle nav caret on:click={toggleDropdown}>
          <i class="fas fa-user fa-fw ml-3" />
        </DropdownToggle>
        <DropdownMenu right>
          <DropdownItem href="settings">Settings</DropdownItem>
          <DropdownItem href="activity_log">Activity Log</DropdownItem>
          <DropdownItem divider />
          <DropdownItem href="pages/authentication/login">Logout</DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </ListGroup> -->
  </Nav>
</Navbar>

