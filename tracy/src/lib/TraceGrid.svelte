<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let traces = [];
  const sizeClasses = {
    small: 'row-span-1',
    medium: 'row-span-2',
    tall: 'row-span-3',
  };

  const handleImageClick = (url) => {
    // Extract the filename without extension and add .gpx
    const filename = url.replace('.svg', '.gpx');
    dispatch('selectTrace', { gpxUrl: `/gpx/${filename}` });
  };
</script>

<div class="w-[55%] h-screen overflow-scroll p-4">
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 h-fit">
    {#each traces as url, index}
      <div class="overflow-hidden cursor-pointer" on:click={() => handleImageClick(url)}>
        <img src={`/svg/${url}`} alt={`SVG ${index + 1}`} class="w-full h-auto block" />
      </div>
    {/each}
  </div>
</div>
