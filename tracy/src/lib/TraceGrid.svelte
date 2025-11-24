<script>
  const traces = [
    '12117685.svg',
    '12117739.svg',
    '12117781.svg',
    '12117813.svg',
    '12117827.svg',
    '12117687.svg',
    '12117740.svg',
    '12117782.svg',
    '12117814.svg',
    '12117870.svg',
    '12117691.svg',
    '12117766.svg',
    '12117789.svg',
    '12117815.svg',
    '12117871.svg',
    '12117699.svg',
    '12117777.svg',
    '12117794.svg',
    '12117816.svg',
    '12117873.svg',
    '12117713.svg',
    '12117778.svg',
    '12117798.svg',
    '12117823.svg',
    '12117881.svg',
    '12117715.svg',
    '12117779.svg',
    '12117811.svg',
    '12117825.svg',
    '12117882.svg',
    '12117728.svg',
    '12117780.svg',
    '12117812.svg',
    '12117826.svg',
  ];

  const sizeClasses =
    {
      small:
        'row-span-1',
      medium:
        'row-span-2',
      tall: 'row-span-3',
    };
</script>

<div
  class="w-[55%] p-4"
>
  <div
    class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4"
  >
    {#each traces as url, index}
      <div
        class="overflow-hidden"
      >
        <img
          src={`/public/svg/${url}`}
          alt={`SVG ${index + 1}`}
          class="w-full h-auto block"
        />
      </div>
    {/each}
  </div>
</div>
