"""
DAY 5 — Inspection mission design: "how would I actually get to that object?"

WHY THIS STEP EXISTS:
The JD's own first line is "design of a satellite mission for the inspection of other objects in
space." Conjunction screening tells you two objects are close; mission design asks the opposite
question — given a chaser satellite and a target object's orbit, what maneuver gets you there
on purpose, and what does it cost in delta-v (the standard currency of "how much fuel/effort").

The simplest real answer, for two roughly co-planar circular orbits, is a Hohmann transfer:
one burn to leave the starting orbit onto an ellipse reaching the target altitude, coast, one
burn to circularize at the target. It's not how a real rendezvous mission would necessarily do
it (phasing, plane changes, and proximity operations add real complexity) — but it's the
textbook starting point every real mission designer still reasons from first.

TODO(you): implement hohmann_transfer() below by hand (not from a library) — this is the one
part of the project worth deriving yourself, since it's short enough to fully understand.
"""

import math

MU = 398600.4418  # km^3/s^2, Earth's gravitational parameter
RE = 6371.0        # km, Earth mean radius


def circular_velocity(r_km):
    """
    Speed needed to stay in a circular orbit of radius r_km.
    WHY: comes directly from setting gravitational force = centripetal force and solving for v.
    Derive it on paper once — v = sqrt(mu/r) — before trusting this function.
    """
    return math.sqrt(MU / r_km)


def hohmann_transfer(alt1_km, alt2_km):
    radius_lower_orbit = RE + alt1_km
    radius_higher_orbit = RE + alt2_km
    v_lower_orbit = circular_velocity(radius_lower_orbit)
    v_higher_orbit = circular_velocity(radius_higher_orbit)
    a_transfer_ellipse = (radius_lower_orbit + radius_higher_orbit) / 2
#     speed using vis-viva
    v_transfer_ellipse_1 = math.sqrt(MU * (2/radius_lower_orbit - 1/a_transfer_ellipse))
    v_transfer_ellipse_2 = math.sqrt(MU * (2/radius_higher_orbit - 1/a_transfer_ellipse))
#     delta-v for burns
    dv1 = v_transfer_ellipse_1 - v_lower_orbit
    dv2 = v_higher_orbit - v_transfer_ellipse_2
    print(radius_lower_orbit, radius_higher_orbit)
    print(v_lower_orbit, v_higher_orbit)
    print(v_transfer_ellipse_1, v_transfer_ellipse_2)
    print(dv1, dv2)
    transfer_time = math.pi * math.sqrt(a_transfer_ellipse**3 / MU)
    return {
        "dv1_kms": dv1,
        "dv2_kms": dv2,
        "total_dv_kms": abs(dv1) + abs(dv2),
        "transfer_time_hours": transfer_time / 3600
    }
    """
    Compute the two burns of a Hohmann transfer between two circular orbits.

    STEPS TO IMPLEMENT:
    1. r1 = RE + alt1_km, r2 = RE + alt2_km
    2. v1 = circular_velocity(r1), v2 = circular_velocity(r2)
    3. Transfer ellipse semi-major axis: a_t = (r1 + r2) / 2
    4. Speed on the transfer ellipse AT r1 (vis-viva equation):
         v_t1 = sqrt(mu * (2/r1 - 1/a_t))
    5. Speed on the transfer ellipse AT r2:
         v_t2 = sqrt(mu * (2/r2 - 1/a_t))
    6. dv1 = v_t1 - v1   (burn to leave the starting circular orbit)
       dv2 = v2 - v_t2   (burn to circularize into the target orbit)
    7. Transfer time = half the transfer ellipse's period:
         t = pi * sqrt(a_t^3 / mu)
    8. Return {"dv1_kms": dv1, "dv2_kms": dv2, "total_dv_kms": abs(dv1)+abs(dv2),
               "transfer_time_hours": t/3600}

    Once implemented, sanity check: transferring 400km -> 1200km altitude should cost roughly
    ~0.14 km/s per burn, ~0.28 km/s total, and take a bit under an hour. If you're wildly off,
    check your units (km vs m) before anything else — this is the #1 bug source here.
    """


if __name__ == "__main__":
    alt1 = float(input("Enter starting orbit altitude (km): "))
    alt2 = float(input("Enter target orbit altitude (km): "))
    # Example: chaser in a 400km parking orbit, target object (debris) at 1200km
    result = hohmann_transfer(alt1_km=alt1, alt2_km=alt2)
    print(f"burn 1 delta-v: {result['dv1_kms']:.3f} km/s")
    print(f"burn 2 delta-v: {result['dv2_kms']:.3f} km/s")
    print(f"total delta-v: {result['total_dv_kms']:.3f} km/s")
    print(f"transfer time: {result['transfer_time_hours']:.3f} hours")
