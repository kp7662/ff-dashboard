<script>
    import { Card, CardBody } from '@sveltestrap/sveltestrap';
    
    export let cardTitle = "";
  </script>
  
  <Card class="flex flex-col border-0 shadow-lg">
    <CardBody class="p-4">
      <div class="flex items-center justify-between">
        <div class="text-lg font-semibold">{cardTitle}</div>
      </div>
  
      <div class="text-4xl font-bold my-3">75%</div>
  
      <div class="flex justify-between items-center mb-2">
        <div>Aggregate</div>
        <div class="flex items-center text-green-500">
          7% 
        </div>
      </div>
    </CardBody>
  </Card>