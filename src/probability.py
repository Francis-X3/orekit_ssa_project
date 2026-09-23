"""
DAY 7 — Probability of collision: from "how close" to "how risky."

WHY THIS STEP EXISTS:
A raw miss distance doesn't account for the fact that we never know an object's true position
exactly — TLE-derived positions carry uncertainty. Probability of collision (Pc) folds that
uncertainty in: given how close two objects come, and how much we trust each position estimate,
what's the actual chance they physically collide? This is the metric real operators act on, not
raw distance alone.

ASSUMPTIONS (worth stating explicitly — not operational-grade):
- sigma_a_km / sigma_b_km are illustrative uncertainty estimates supplied by the caller, NOT
  derived from real tracking covariance (TLEs don't carry that data).
- Uncertainty is treated as isotropic (a circle, not a real stretched ellipse) for both objects.
- Valid when hbr_km << combined sigma (small hard-body-radius approximation).
"""

import math
from conjunction import find_closest_approach
from setup_check import fetch_tles, COSMOS_2605_URL, STARLINK_32747_URL


def probability_of_collision(min_distance_km, sigma_a_km, sigma_b_km, hbr_km=0.01):
    """
    Simplified 2D Pc estimate: Pc ≈ (hbr_km^2 / (2*sigma^2)) * exp(-min_distance_km^2 / (2*sigma^2))
    where sigma = combined uncertainty = sqrt(sigma_a_km^2 + sigma_b_km^2).
    """
    sigma = math.hypot(sigma_a_km, sigma_b_km)
    fade_factor = math.exp(-0.5 * (min_distance_km / sigma) ** 2)
    pre_factor = hbr_km ** 2 / (2 * sigma ** 2)
    return pre_factor * fade_factor


if __name__ == "__main__":
    cosmos = fetch_tles(COSMOS_2605_URL)[0]
    starlink = fetch_tles(STARLINK_32747_URL)[0]
    print(f"Screening {cosmos['name']} vs {starlink['name']}...")

    result = find_closest_approach((cosmos["line1"], cosmos["line2"]), (starlink["line1"], starlink["line2"]))
    min_distance_km = result["min_distance_km"]
    print(f"closest approach distance: {min_distance_km:.3f} km")

    # illustrative sigma values — not operationally tracked, for demonstration only
    sigma_a_km = 0.3
    sigma_b_km = 0.1
    pc = probability_of_collision(min_distance_km, sigma_a_km, sigma_b_km)
    print(f"probability of collision: {pc:.3e}")