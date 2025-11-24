#!/usr/bin/python3

"""
download gps traces within a bounding box or by id
convert .gpx to .geojson
"""

import requests
import time
from gpxtools import gpx_to_geojson


def fetch_gps_trackpoints(min_lon, min_lat, max_lon, max_lat):
    """
    Fetch GPS trackpoints from OSM API for a bounding box.
    Returns:
        GPX data as string
    """
    base_url = "https://api.openstreetmap.org/api/0.6/trackpoints"

    bbox = f"{min_lon},{min_lat},{max_lon},{max_lat}"

    # pageNumber
    params = {
        'bbox': bbox,
        'page': 0
    }

    headers = {
        'User-Agent': 'GPSTraceFetcher/1.0'
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def download_trace_by_id(trace_id):
    """
    Download a specific public GPS trace by its ID.

    Args:
        trace_id: The OSM trace ID

    Returns:
        GPX data as string
    """
    url = f"https://api.openstreetmap.org/api/0.6/gpx/{trace_id}/data"

    headers = {
        'User-Agent': 'GPSTraceFetcher/1.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading trace {trace_id}: {e}")
        return None


def save_gpx(gpx_data, filename):
    """Save GPX data to a file."""
    if gpx_data:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(gpx_data)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    print("Fetching GPS trackpoints...")

    # only allows max 5000 points
    gpx_data = fetch_gps_trackpoints(-71.075, 42.36, -71.06, 42.37)
    if gpx_data:
        save_gpx(gpx_data, "trackpoints.gpx")
        gpx_to_geojson("trackpoints.gpx", "trackpoints.geojson")

    #  by id
    # trace_data = download_trace_by_id(12345)
    # if trace_data:
    #     save_gpx(trace_data, "trace_12345.gpx")

    # delay for API rate limit
    time.sleep(1)
