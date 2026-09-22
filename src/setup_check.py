"""
DAY 1 — Setup + real orbit data.

WHY THIS STEP EXISTS:
Every SSA task starts with knowing an object's orbit *right now*. Operationally, that comes from
a TLE (Two-Line Element set) — a compact snapshot of an object's orbital elements plus atmospheric
drag terms, published by the US Space Force / Celestrak from radar tracking. It's not a perfect
orbit, it's a fitted approximation — but it's what the whole industry actually uses for cataloguing.

TODO(you): once orekit is installed, uncomment the imports below and get this running.
"""

import requests

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
# Smaller, easier group to start with while you're learning:
DEBRIS_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-1408-debris&FORMAT=tle"
ISS_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=tle"
HUBBLE_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=20580&FORMAT=tle"

def fetch_tles(url):
    """
    Pull a TLE set from Celestrak.

    WHY: Celestrak is a free public mirror of the official Space-Track catalog. Using real,
    current data (not synthetic numbers) is what makes this project defensible in an interview —
    you can be asked "where did this orbit come from?" and have a real answer.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    lines = [l for l in resp.text.splitlines() if l.strip()]
    # TLE format: every object is 3 lines — name, line 1, line 2
    objects = []
    for i in range(0, len(lines) - 2, 3):
        objects.append({
            "name": lines[i].strip(),
            "line1": lines[i + 1],
            "line2": lines[i + 2],
        })
    return objects


def check_orekit():
    """
    TODO(you): install orekit (see README), then implement this.

    WHY THIS MATTERS: Orekit needs a small reference-data package (leap seconds, Earth orientation
    parameters, etc.) to do anything — this is the same kind of reference data real mission-analysis
    tools need, and knowing *why* it's needed (not just running the install command) is worth
    understanding before day 2.

    Docs to read for this step: https://www.orekit.org/site-orekit-python/
    """
    import orekit
    from orekit.pyhelpers import setup_orekit_curdir
    orekit.initVM()
    setup_orekit_curdir()
    print("Orekit initialized OK")

if __name__ == "__main__":
    print("Fetching a small debris TLE set from Celestrak...")
    objs = fetch_tles(DEBRIS_URL)
    print(f"Got {len(objs)} objects. First one:")
    print(objs[0])

    print("\nChecking Orekit is installed and initialized...")
    check_orekit()
