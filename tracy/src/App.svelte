<script>
  import Map from './lib/Map.svelte';
  import TraceGrid from './lib/TraceGrid.svelte';
  import Notebook from './lib/Notebook.svelte';

  // let traces = ['12117691.svg', 'trace2.svg', 'trace3.svg'];
  const traces = [
    '12117691.svg',
    '12117685.svg',
    '12117687.svg',
    '12117873.svg',
    '12117720.svg',
    '12117870.svg',
    '12118410.svg',
    '12118559.svg',
    '12117871.svg',
    '12117859.svg',
    '12117816.svg',
    '12118516.svg',
    '12117779.svg',
    '12117778.svg',
    '12117815.svg',
    '12118461.svg',
    '12118475.svg',
    '12118514.svg',
    '12117814.svg',
    '12117794.svg',
    '12117780.svg',
    '12118465.svg',
    '12117781.svg',
    '12117811.svg',
    '12117813.svg',
    '12118507.svg',
    '12118513.svg',
    '12117740.svg',
    '12118473.svg',
    '12117782.svg',
    '12118512.svg',
    '12117812.svg',
    '12117823.svg',
    '12117798.svg',
    '12118497.svg',
    '12118468.svg',
    '12118454.svg',
    '12117766.svg',
    '12117825.svg',
    '12117789.svg',
    '12118451.svg',
    '12117777.svg',
    '12117826.svg',
    '12118452.svg',
    '12117827.svg',
    '12117840.svg',
    '12118540.svg',
    '12117713.svg',
    '12117882.svg',
    '12117699.svg',
    '12118557.svg',
    '12118437.svg',
    '12117739.svg',
    '12117881.svg',
    '12117715.svg',
    '12117728.svg',
  ];
  let selectedGpxUrl = null;

  function handleTraceSelect(event) {
    selectedGpxUrl = event.detail.gpxUrl;
  }
</script>

<main class="flex flex-row h-screen overflow-hidden">
  <TraceGrid {traces} on:selectTrace={handleTraceSelect} />
  <Map gpxUrl={selectedGpxUrl} />
  <!-- <Notebook /> -->
</main>
