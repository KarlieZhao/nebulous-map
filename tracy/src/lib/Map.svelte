<script>
  import { onMount, onDestroy } from 'svelte';
  import L from 'leaflet';

  export let center = [42.3601, -71.0589]; // Default: Boston
  export let zoom = 13;
  export let geojsonData = null;

  let mapElement;
  let map;
  let geojsonLayer;

  onMount(() => {
    // Initialize the map
    map = L.map(mapElement).setView(center, zoom);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
    }).addTo(map);

    // Fix for default marker icon issue in Leaflet with bundlers
    // delete L.Icon.Default.prototype._getIconUrl;
    // L.Icon.Default.mergeOptions({
    //   iconRetinaUrl:
    //     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    //   iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    //   shadowUrl:
    //     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    // });
  });

  onDestroy(() => {
    if (map) {
      map.remove();
    }
  });

  // Reactive statement to update GeoJSON layer when data changes
  $: if (map && geojsonData) {
    // Remove existing layer if present
    if (geojsonLayer) {
      map.removeLayer(geojsonLayer);
    }

    // Add new GeoJSON layer
    geojsonLayer = L.geoJSON(geojsonData, {
      style: (feature) => ({
        color: '#3b82f6',
        weight: 2,
        fillColor: '#60a5fa',
        fillOpacity: 0.5,
      }),
      onEachFeature: (feature, layer) => {
        // Add popup with properties
        if (feature.properties) {
          const props = Object.entries(feature.properties)
            .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
            .join('<br>');
          layer.bindPopup(props);
        }
      },
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: 8,
          fillColor: '#3b82f6',
          color: '#1e40af',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8,
        });
      },
    }).addTo(map);

    // Fit map to GeoJSON bounds
    const bounds = geojsonLayer.getBounds();
    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }
</script>

<div bind:this={mapElement} class="w-full h-full"></div>

<style>
  div {
    min-height: 400px;
  }
</style>
