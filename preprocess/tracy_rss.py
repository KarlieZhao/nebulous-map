#!/usr/bin/python3

"""Fetch GPS traces from OpenStreetMap RSS feed"""

from datetime import datetime
import requests
import os
import time
import xmltodict
from pathlib import Path
from gpxtools import gpx_to_geojson, gpx_to_svg

from xml.etree import ElementTree as ET

import gzip
import bz2


def fetch_rss(url):
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = xmltodict.parse(res.text)
    items = data['rss']['channel']['item']

    traces = []
    for item in items:
        link = item['link']
        trace_id = link.split('/')[-1]
        traces.append({
            'id': trace_id,
            'title': item['title'],
            'dataURL': f'https://www.openstreetmap.org/trace/{trace_id}/data'
        })

    return traces


def fetch_trace(url):
    res = requests.get(url)
    if not res.ok:
        return None

    content_type = res.headers.get('content-type', '')
    content = res.content

    if content_type == 'application/gpx+xml':
        return content.decode('utf-8')

    if content_type == 'application/x-gzip':
        return gzip.decompress(content).decode('utf-8')

    if content_type == 'application/x-bzip2':
        return bz2.decompress(content).decode('utf-8')

    print(f'Unhandled MIME type: {content_type}')
    return None


def download_gpx(item, title, outdir):
    gpx_name = title + '.gpx'
    name_base = title
    path = os.path.join(outdir, gpx_name)

    # skip if file exists
    if os.path.exists(path):
        # print(f"{gpx_name} exists. Skipping.")
        return 0

    print(f"writing {gpx_name}")
    try:
        xml = fetch_trace(item['dataURL'])

        if not xml:
            print('Data format not right, skipping.')
            return 0

        # Save GPX file
        Path(f'/Users/karlie/Documents/GitHub/maps/preprocess/gpx/{gpx_name}').write_text(
            xml, encoding='utf-8')
        print(f'Saved {gpx_name}')

        # # convert to geojson and svg
        # try:
        #     geojson_name = name_base + ".geojson"
        #     geojson_path = os.path.join(
        #         "/Users/karlie/Documents/GitHub/maps/preprocess/geojson", geojson_name)
        #     gpx_to_geojson(path, geojson_path)
        #     # svg_name = name_base + ".svg"
        #     # svg_path = os.path.join("/Users/karlie/Documents/GitHub/maps/preprocess/svg", svg_name)
        #     # gpx_to_svg(path, svg_path)
        # except Exception as e:
        #     print(f"Error processing {gpx_name}: {e}")
    except Exception as e:
        print(f'Error downloading {gpx_name}: {e}')
    time.sleep(0.5)
    return 1


def main():
    rss_url = 'https://www.openstreetmap.org/traces/rss'

    # print('Fetching RSS...')
    items = fetch_rss(rss_url)
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: found {len(items)} items.')

    outdir = "/Users/karlie/Documents/GitHub/maps/preprocess/gpx"
    os.makedirs(outdir, exist_ok=True)
    success = 0

    for i in range(min(10, len(items))):
        item = items[i]
        success += download_gpx(item, item["id"], outdir)

    print(f"Downloaded {success} new traces.")


if __name__ == "__main__":
    main()
    # print("Done.")
