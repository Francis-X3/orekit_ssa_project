import math
from conjunction import find_closest_approach
from setup_check import fetch_tles, DEBRIS_URL,  ISS_URL, HUBBLE_URL, COSMOS_2605_URL, STARLINK_32747_URL

def probability_of_collision(min_distance_km, sigma_a_km, sigma_b_km, hbr_km=0.01):

    # adding the sigma
    sigma = math.hypot(sigma_a_km, sigma_b_km)
    fade_factor = math.exp(-0.5 * (min_distance_km / sigma) ** 2)
    pre_factor = hbr_km ** 2 / (2* sigma**2)
    return pre_factor * fade_factor
if __name__ == "__main__":
    cosmos= fetch_tles(COSMOS_2605_URL)[0]
    starlink= fetch_tles(STARLINK_32747_URL)[0]
    print(f"Screening {cosmos['name']} vs {starlink['name']}...")
    print(starlink["name"])
    print(starlink["line1"])

    result = find_closest_approach((cosmos["line1"], cosmos["line2"]), (starlink["line1"], starlink["line2"]))
    print(cosmos ["line1"], cosmos ["line2"])
    min_distance_km=result["min_distance_km"]
    print(f"closest approach distance: {min_distance_km:.3f} km")
    #illustrative sigma values not operationally tracked, just for demonstration
    sigma_a_km = 0.3
    sigma_b_km = 0.1
    pc = probability_of_collision(min_distance_km, sigma_a_km, sigma_b_km)
    print(f"probability of collision: {pc:.3e}")
    """
    Simplified 2D Pc estimate — see project notes for derivation and assumptions
    (isotropic uncertainty, small-HBR approximation, no real covariance data since
    TLEs don't provide it — sigma values here are illustrative estimates, not
    tracked truth).
    """