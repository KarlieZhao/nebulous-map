"""
Plot gpx traces on a map
"""

import gpxpy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob

# ---------- Load GPX file(s) ----------


def load_gpx(file_path):
    with open(file_path, 'r') as f:
        gpx = gpxpy.parse(f)
    traces = []
    for track in gpx.tracks:
        for segment in track.segments:
            points = [(p.longitude, p.latitude) for p in segment.points]
            if points:
                traces.append(points)
    return traces

# ---------- Plot traces on a map ----------


def plot_traces(traces_list, output_file="map.png"):
    plt.figure(figsize=(16, 10))

    # Mercator projection
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_global()

    # Add land, oceans, coastlines
    ax.add_feature(cfeature.LAND, facecolor="#f2f2f2")
    ax.add_feature(cfeature.OCEAN, facecolor="#dcecff")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor="gray")

    # Plot each GPX trace
    for trace in traces_list:
        lons, lats = zip(*trace)
        ax.plot(lons, lats, transform=ccrs.Geodetic(),
                color='red', linewidth=1.2)

    plt.title("GPX Traces Map")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {output_file}")


# ---------- MAIN ----------
if __name__ == "__main__":
    # Load all GPX files in current directory
    gpx_files = glob.glob("*.gpx")
    all_traces = []

    for f in gpx_files:
        traces = load_gpx(f)
        all_traces.extend(traces)
        print(f"Loaded {len(traces)} traces from {f}")

    plot_traces(all_traces)
