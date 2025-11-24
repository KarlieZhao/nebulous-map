<script>
  import Map from './lib/Map.svelte';
  import TraceGrid from './lib/TraceGrid.svelte';
  import Notebook from './lib/Notebook.svelte';

  let geojsonData = null;

  function handleGeojsonLoaded(event) {
    geojsonData = event.detail;
  }
</script>

<main class="flex flex-row">
  <TraceGrid />
  <Notebook />
</main>
