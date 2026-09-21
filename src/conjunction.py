"""
DAY 3-4 — Conjunction screening: the actual "SSA" part of Space Situational Awareness.

WHY THIS STEP EXISTS:
Given two propagated tracks, the operational question is never "are they close right now" — it's
"over the next N hours/days, what is the MINIMUM distance they ever reach, and when." That minimum
is the conjunction event. Real operators compare this against a threshold (often ~1 km for a hard
alert, tens of km for a "worth a closer look") and decide whether to recommend a collision-avoidance
maneuver. You are building a tiny, honest version of that pipeline.

TODO(you): implement find_closest_approach() using propagate_object() from propagate.py.
"""

import math
from propagate import propagate_object
from setup_check import fetch_tles, DEBRIS_URL
from org.orekit.propagation.analytical.tle import TLE , TLEPropagator
from org.orekit.frames import FramesFactory


def distance_km(pos_a, pos_b):
    """Euclidean distance between two [x,y,z] km position vectors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos_a, pos_b)))


def find_closest_approach(tle_a, tle_b, duration_hours=72, step_minutes=1):
    """
    Propagate BOTH objects over the same time window and find the minimum separation.

    STEPS TO IMPLEMENT:
    1. Call propagate_object() for object A and object B, same duration, same step size.
       (Important: same time grid, so you're comparing positions at matching instants —
       this is the most common bug in a first attempt.)
    2. Walk through both tracks together, compute distance_km() at each matching timestep.
    3. Track the minimum distance and the time it occurred.
    4. Return {"min_distance_km": ..., "time_seconds": ..., "time_readable": ...}

    WHY step_minutes=1 here vs step_minutes=5 in propagate.py's default: conjunction events can
    be brief — if your sampling is too coarse you can step OVER the actual closest point and
    report a falsely large minimum. This is a real limitation of "screening by sampling" (as
    opposed to the analytical/optimization-based approach real SSA systems use) — worth
    understanding as a limitation, not hiding it.
    """
    results_A = propagate_object(tle_a[0], tle_a[1], duration_hours, step_minutes)
    results_B = propagate_object(tle_b[0], tle_b[1], duration_hours, step_minutes)
    min_distance = float("inf")
    min_distance_time = None
    
                                                                   
    for sample_a, sample_b in zip(results_A, results_B):
        dist = distance_km(sample_a["position_km"], sample_b["position_km"])
        if dist < min_distance:
            min_distance = dist
            min_distance_time = sample_a["t_seconds"]
    return {
        "min_distance_km": min_distance,
        "time_seconds": min_distance_time,
        "time_readable":f"{min_distance_time/3600:.2f} hours",}
    

def classify_risk(min_distance_km):
    """
    Toy risk bucket, NOT an operational threshold (real ones depend on object size, covariance,
    etc. — this is deliberately simplified so you can reason about the shape of the problem).
    """
    if min_distance_km < 1:
        return "HIGH — would warrant real covariance analysis in practice"
    elif min_distance_km < 25:
        return "MODERATE — flagged for follow-up screening"
    else:
        return "LOW — logged, no action"


if __name__ == "__main__":
    objs = fetch_tles(DEBRIS_URL)
    if len(objs) < 2:
        raise SystemExit("Need at least 2 objects in this TLE group to compare")

    a, b = objs[0], objs[1]
    print(f"Screening {a['name']} vs {b['name']}...")

    result = find_closest_approach(
        (a["line1"], a["line2"]),
        (b["line1"], b["line2"]),
    )
    print(result)
    print("Risk bucket:", classify_risk(result["min_distance_km"]))
