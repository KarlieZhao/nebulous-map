#!/usr/bin/python3

"""
Scan through .osm file, read category tags, write them into categories.txt
Filter by catogories/tags, write filtered features into _filtered.osm and geojson.
"""

import subprocess
import os
import osmium
from collections import defaultdict

FILENAME = "somerville"


class TagCounter(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.tags = defaultdict(set)

    def node(self, n):
        for tag in n.tags:
            self.tags[tag.k].add(tag.v)

    def way(self, w):
        for tag in w.tags:
            self.tags[tag.k].add(tag.v)

    def relation(self, r):
        for tag in r.tags:
            self.tags[tag.k].add(tag.v)


class FeatureFilter(osmium.SimpleHandler):
    def __init__(self, output_file):
        osmium.SimpleHandler.__init__(self)
        self.writer = osmium.SimpleWriter(output_file)
        # MODIFY FILTERS HERE
        self.filter_tags = {
            # 'addr:street': []
        }

    def node(self, n):
        if self._should_include(n):
            self.writer.add_node(n)

    def node(self, n):
        # Include node if it matches filter OR is needed by a way
        if self._should_include(n) or n.id in self.needed_nodes:
            self.writer.add_node(n)

    def way(self, w):
        if self._should_include(w):
            self.writer.add_way(w)

    def _should_include(self, obj):
        if not self.filter_tags:
            # print("Filter list is empty; outputing all features.")
            return True

        for tag in obj.tags:
            # check if tag key starts with any of our filter prefixes
            for filter_key in self.filter_tags:
                if tag.k.startswith(filter_key):
                    # if specific values are listed, check them
                    if self.filter_tags[filter_key]:
                        if tag.v in self.filter_tags[filter_key]:
                            return True
                    # if empty list, include all with this prefix
                    else:
                        return True
        return False

    def close(self):
        self.writer.close()


def main():
    # ===== GET ALL CATOGORIES FROM ORIGINAL OSM ====
    # Count all tags
    print("Analyzing OSM file...")
    counter = TagCounter()
    counter.apply_file(f"{FILENAME}.osm", locations=True)

    # show categories
    with open("osm_categories.txt", "w", encoding="utf-8") as f:
        f.write("All Categories Found\n")
        for key in sorted(counter.tags.keys()):
            # print(f"\n{key}:")
            f.write(f"\n{key}:\n")
            for value in sorted(counter.tags[key]):
                # print(f"  - {value}")
                f.write(f"  - {value}\n")

    print(f"\nCategories saved to {FILENAME}_catogories.txt")

    OSM_FILE = os.path.join('osm', f"{FILENAME}_filtered.osm")
    GEOJSON_FILE = os.path.join('geojson', f'{FILENAME}_filtered.geojson')

    # ===== CREATE FILTERED OSM AND GEOJSON ====
    # remove file if it exists
    if os.path.exists(OSM_FILE):
        os.remove(OSM_FILE)

    filter_handler = FeatureFilter(OSM_FILE)
    filter_handler.apply_file(f"{FILENAME}.osm", locations=True)
    filter_handler.close()
    print(f"Filtered osm: {OSM_FILE}")

    # convert to GeoJSON
    subprocess.run([
        'osmium', 'export',
        OSM_FILE,
        '-o', GEOJSON_FILE,
        '--overwrite'
    ], check=True)

    print(f"Geojson: {GEOJSON_FILE}")


if __name__ == "__main__":
    main()
