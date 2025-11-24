"""Helpers: gpx_to_geojson, gpx_to_svg"""
#!/usr/bin/python3

import json
import gpxpy
import os
import xml.etree.ElementTree as ET


def gpx_to_geojson(gpx_file, output_file, write_tracks=True, write_routes=False, write_waypoints=False):
    """
    Convert GPX file to GeoJSON.
    """
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)

    features = []

    # Process tracks
    if write_tracks:
        for track in gpx.tracks:
            for segment in track.segments:
                coordinates = []
                for point in segment.points:
                    coordinates.append(
                        [point.longitude, point.latitude, point.elevation or 0])
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates
                    },
                    "properties": {
                        "name": track.name or "Unnamed Track",
                        "type": "track"
                    }
                }
                features.append(feature)

    # Process routes
    if write_routes:
        for route in gpx.routes:
            coordinates = []
            for point in route.points:
                coordinates.append(
                    [point.longitude, point.latitude, point.elevation or 0])
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {
                    "name": route.name or "Unnamed Route",
                    "type": "route"
                }
            }
            features.append(feature)

    # Process waypoints
    if write_waypoints:
        for waypoint in gpx.waypoints:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [waypoint.longitude, waypoint.latitude, waypoint.elevation or 0]
                },
                "properties": {
                    "name": waypoint.name or "Unnamed Waypoint",
                    "type": "waypoint",
                    "description": waypoint.description
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"Converted {len(features)} features to {output_file}")


def gpx_to_svg(gpx_path, svg_path, width=800, height=600):
    """Convert GPX file to SVG visualization"""
    tree = ET.parse(gpx_path)
    root = tree.getroot()

    # Handle GPX namespace
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    if not root.tag.endswith('gpx'):
        ns = {'gpx': 'http://www.topografix.com/GPX/1/0'}

    # Extract all track points
    points = []

    # With namespace
    for trkpt in root.findall('.//gpx:trkpt', ns):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        points.append((lon, lat))

    # fallback without prefix
    if not points:
        for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/0}trkpt'):
            lat = float(trkpt.get('lat'))
            lon = float(trkpt.get('lon'))
            points.append((lon, lat))

    if not points:
        # Try without namespace
        for trkpt in root.findall('.//trkpt'):
            lat = float(trkpt.get('lat'))
            lon = float(trkpt.get('lon'))
            points.append((lon, lat))

    if not points:
        print(f"We tried, but no track points found in {gpx_path}")
        return

    # Calculate bounds
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    # Add padding
    lon_range = max_lon - min_lon or 0.01
    lat_range = max_lat - min_lat or 0.01
    padding = 0.1
    min_lon -= lon_range * padding
    max_lon += lon_range * padding
    min_lat -= lat_range * padding
    max_lat += lat_range * padding

    # Transform coordinates to SVG space
    def transform(lon, lat):
        x = (lon - min_lon) / (max_lon - min_lon) * width
        y = height - (lat - min_lat) / (max_lat - min_lat) * height
        return x, y

    # Build SVG path
    svg_points = [transform(lon, lat) for lon, lat in points]
    path_data = f"M {svg_points[0][0]},{svg_points[0][1]}"
    for x, y in svg_points[1:]:
        path_data += f" L {x},{y}"

    # Create SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <rect width="100%" height="100%" fill="#f0f0f000"/>
    <path d="{path_data}" stroke="#DBE4EE" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="{svg_points[0][0]}" cy="{svg_points[0][1]}" r="5" fill="#22c55e"/>
    <circle cx="{svg_points[-1][0]}" cy="{svg_points[-1][1]}" r="5" fill="#ef4444"/>
</svg>'''

    with open(svg_path, 'w') as f:
        f.write(svg)
    print(f"SVG saved as: {svg_path}")


if __name__ == "__main__":
    # gpx_to_geojson("./gpx/2025_11_18_10_42_35.gpx", "./geojson/test.geojson")
    svg_folder = "../tracy/public/svg"
    existing = []
    with os.scandir(svg_folder) as svgs:
        for svg in svgs:
            filename = os.path.basename(svg).split(".")[0]
            existing.append(filename)

    with os.scandir("./gpx") as traces:
        for trace in traces:
            filename = os.path.basename(trace)
            basename = filename.split(".")[0]
            if basename not in existing:
                # print(basename)
                gpx_to_svg(trace, f"{svg_folder}/{basename}.svg")
