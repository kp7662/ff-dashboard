<script>
    import { Card, CardBody, CardFooter, CardHeader, CardText, 
        CardSubtitle, Table, Row } from 'sveltestrap';
  
    export let cardTitle = "";
    export let cardColor;
    export let cardFooterText = "View Details";
  </script>
  
  <Card inverse color={cardColor} class="mb-4">
    <CardBody>
      <CardText>{cardTitle}</CardText>
    </CardBody>
    <CardFooter class="d-flex align-items-center justify-content-between">
      <a class="small text-white stretched-link" href="charts">
        {cardFooterText}
      </a>
      <div class="small text-white">
        <i class="fas fa-angle-right" />
      </div>
    </CardFooter>
  </Card>