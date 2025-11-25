<script>
  import { onMount, onDestroy } from 'svelte';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';
  import 'leaflet-gpx';

  export let center = [42.3601, -71.0589];
  export let zoom = 13;
  export let gpxUrl = '/gpx/12117691.gpx';

  let mapElement;
  let map;
  let gpxLayer;

  onMount(() => {
    // Initialize Leaflet map
    map = L.map(mapElement).setView(center, zoom);

    // Add tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
    }).addTo(map);
  });

  onDestroy(() => {
    if (map) map.remove();
  });

  // Load GPX whenever gpxUrl changes
  $: if (map && gpxUrl) {
    // Clear old layer
    if (gpxLayer) {
      map.removeLayer(gpxLayer);
    }

    // GPX layer
    gpxLayer = new L.GPX(gpxUrl, {
      async: true,
      marker_options: {
        startIconUrl: 'https://raw.githubusercontent.com/mpetazzoni/leaflet-gpx/master/pin-icon-start.png',
        endIconUrl: 'https://raw.githubusercontent.com/mpetazzoni/leaflet-gpx/master/pin-icon-end.png',
        shadowUrl: 'https://raw.githubusercontent.com/mpetazzoni/leaflet-gpx/master/pin-shadow.png',
      },
    })
      .on('loaded', (e) => {
        map.fitBounds(e.target.getBounds());
      })
      .addTo(map);
  }
</script>

<div bind:this={mapElement} class="w-[45%] h-screen"></div>

<style>
  div {
    min-height: 400px;
  }
</style>
