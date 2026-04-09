#!/usr/bin/env python3
"""
download_tiles.py — Download OpenStreetMap tiles for offline use.

Usage:
    python download_tiles.py --region us --output ./drive/maps
    python download_tiles.py --region world --output ./drive/maps
    python download_tiles.py --bbox 40.0,-75.0,42.0,-71.0 --max-zoom 14 --output ./drive/maps

Respects OSM tile usage policy: proper User-Agent, max 2 requests/sec.
"""

import os
import sys
import math
import time
import argparse
import urllib.request

TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
USER_AGENT = 'SurvivalAI-TileDownloader/1.0 (offline survival product)'
DELAY = 0.5  # seconds between requests (be nice to OSM servers)

# Pre-defined regions [south_lat, west_lon, north_lat, east_lon]
REGIONS = {
    'world':        [-60, -180, 72, 180],
    'us':           [24.5, -125.0, 49.5, -66.5],
    'us-east':      [24.5, -90.0, 47.0, -66.5],
    'us-west':      [31.0, -125.0, 49.5, -102.0],
    'us-midwest':   [36.0, -104.0, 49.5, -80.0],
    'us-south':     [24.5, -106.0, 37.0, -75.0],
    'northeast':    [39.5, -80.0, 47.5, -66.5],
    'southeast':    [24.5, -92.0, 37.0, -75.0],
    'pacific-nw':   [42.0, -125.0, 49.5, -116.5],
    'california':   [32.5, -124.5, 42.0, -114.0],
    'texas':        [25.8, -106.6, 36.5, -93.5],
    'florida':      [24.5, -87.6, 31.0, -80.0],
    'new-england':  [41.0, -73.7, 47.5, -66.9],
    'europe':       [35.0, -11.0, 60.0, 30.0],
    'uk':           [49.9, -8.2, 58.7, 1.8],
    'canada':       [41.7, -141.0, 60.0, -52.6],
    'australia':    [-44.0, 112.0, -10.0, 154.0],
}

# Default zoom levels per region type
DEFAULT_ZOOMS = {
    'world':    (1, 6),
    'us':       (1, 9),
    'default':  (1, 12),
    'state':    (1, 13),
}


def lat_lon_to_tile(lat, lon, zoom):
    """Convert lat/lon to tile x,y at given zoom."""
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(math.radians(lat)) +
            1.0 / math.cos(math.radians(lat))) / math.pi) / 2.0 * n)
    x = max(0, min(n - 1, x))
    y = max(0, min(n - 1, y))
    return x, y


def count_tiles(bbox, min_zoom, max_zoom):
    """Count total tiles to download."""
    south, west, north, east = bbox
    total = 0
    for z in range(min_zoom, max_zoom + 1):
        x_min, y_max = lat_lon_to_tile(south, west, z)
        x_max, y_min = lat_lon_to_tile(north, east, z)
        total += (x_max - x_min + 1) * (y_max - y_min + 1)
    return total


def estimate_size(tile_count):
    """Rough estimate of download size."""
    avg_kb = 25  # average tile size
    mb = tile_count * avg_kb / 1024
    if mb > 1024:
        return f'{mb/1024:.1f} GB'
    return f'{mb:.0f} MB'


def download_tiles(bbox, min_zoom, max_zoom, output_dir, resume=True):
    """Download tiles for given bounding box and zoom range."""
    south, west, north, east = bbox
    total = count_tiles(bbox, min_zoom, max_zoom)
    downloaded = 0
    skipped = 0
    errors = 0

    print(f'Downloading tiles: zoom {min_zoom}-{max_zoom}')
    print(f'Bounding box: {south},{west} to {north},{east}')
    print(f'Total tiles: {total:,}')
    print(f'Estimated size: {estimate_size(total)}')
    print(f'Output: {output_dir}')
    print(f'Estimated time: {total * DELAY / 60:.0f} minutes')
    print()

    if total > 50000:
        resp = input(f'This will download {total:,} tiles. Continue? (y/n): ')
        if resp.lower() != 'y':
            print('Cancelled.')
            return

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', USER_AGENT)]
    urllib.request.install_opener(opener)

    start_time = time.time()

    for z in range(min_zoom, max_zoom + 1):
        x_min, y_max = lat_lon_to_tile(south, west, z)
        x_max, y_min = lat_lon_to_tile(north, east, z)

        z_total = (x_max - x_min + 1) * (y_max - y_min + 1)
        z_done = 0

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                tile_path = os.path.join(output_dir, str(z), str(x), f'{y}.png')

                # Skip if already downloaded
                if resume and os.path.exists(tile_path) and os.path.getsize(tile_path) > 100:
                    skipped += 1
                    z_done += 1
                    downloaded += 1
                    continue

                os.makedirs(os.path.dirname(tile_path), exist_ok=True)
                url = TILE_URL.format(z=z, x=x, y=y)

                try:
                    urllib.request.urlretrieve(url, tile_path)
                    downloaded += 1
                    z_done += 1
                except Exception as e:
                    errors += 1
                    z_done += 1

                # Progress
                elapsed = time.time() - start_time
                rate = downloaded / max(elapsed, 1)
                remaining = (total - downloaded) / max(rate, 0.1)

                sys.stdout.write(f'\r  z{z}: {z_done}/{z_total}  |  Total: {downloaded}/{total}  |  Errors: {errors}  |  ~{remaining/60:.0f}m left  ')
                sys.stdout.flush()

                time.sleep(DELAY)

        print()  # newline after each zoom level

    elapsed = time.time() - start_time
    actual_size = get_dir_size(output_dir)

    print()
    print(f'Done in {elapsed/60:.1f} minutes')
    print(f'Downloaded: {downloaded - skipped}  Skipped (existing): {skipped}  Errors: {errors}')
    print(f'Total size on disk: {actual_size}')


def get_dir_size(path):
    """Get total size of directory."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            total += os.path.getsize(os.path.join(dirpath, f))
    if total > 1024**3:
        return f'{total/1024**3:.2f} GB'
    return f'{total/1024**2:.1f} MB'


def main():
    parser = argparse.ArgumentParser(description='Download OSM tiles for offline use')
    parser.add_argument('--region', choices=list(REGIONS.keys()),
                        help='Pre-defined region')
    parser.add_argument('--bbox', type=str,
                        help='Custom bounding box: south,west,north,east')
    parser.add_argument('--min-zoom', type=int, default=1,
                        help='Minimum zoom level (default: 1)')
    parser.add_argument('--max-zoom', type=int, default=None,
                        help='Maximum zoom level (default: auto based on region)')
    parser.add_argument('--output', type=str, default='./maps',
                        help='Output directory (default: ./maps)')
    parser.add_argument('--list', action='store_true',
                        help='List available regions and exit')

    args = parser.parse_args()

    if args.list:
        print('Available regions:')
        print()
        for name, bbox in sorted(REGIONS.items()):
            for zname, (zmin, zmax) in DEFAULT_ZOOMS.items():
                pass
            tiles = count_tiles(bbox, 1, 9)
            print(f'  {name:15s}  bbox: {bbox}  ~{estimate_size(tiles)} at z1-9')
        print()
        print('Example usage:')
        print('  python download_tiles.py --region us --output ./drive/maps')
        print('  python download_tiles.py --region northeast --max-zoom 13 --output ./drive/maps')
        print('  python download_tiles.py --bbox 40.0,-75.0,42.0,-71.0 --max-zoom 14 --output ./drive/maps')
        return

    if not args.region and not args.bbox:
        parser.error('Specify --region or --bbox (use --list to see regions)')

    if args.region:
        bbox = REGIONS[args.region]
        if args.max_zoom is None:
            if args.region == 'world':
                args.max_zoom = 6
            elif args.region in ('us', 'europe', 'canada', 'australia'):
                args.max_zoom = 9
            else:
                args.max_zoom = 12
    else:
        parts = [float(x.strip()) for x in args.bbox.split(',')]
        if len(parts) != 4:
            parser.error('bbox must be: south,west,north,east')
        bbox = parts
        if args.max_zoom is None:
            args.max_zoom = 12

    # Show preview
    total = count_tiles(bbox, args.min_zoom, args.max_zoom)
    print()
    print(f'  Region:     {args.region or "custom"}')
    print(f'  Zoom:       {args.min_zoom} to {args.max_zoom}')
    print(f'  Tiles:      {total:,}')
    print(f'  Est. size:  {estimate_size(total)}')
    print(f'  Est. time:  {total * DELAY / 60:.0f} minutes')
    print()

    download_tiles(bbox, args.min_zoom, args.max_zoom, args.output)


if __name__ == '__main__':
    main()
