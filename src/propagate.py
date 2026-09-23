"""
DAY 2 — Propagation: turning "orbital elements at one instant" into "position over time."

WHY THIS STEP EXISTS:
A TLE only tells you where an object was at one specific epoch. Everything SSA cares about —
will it hit something, when does it cross a given point — requires projecting that forward in
time. That projection is called propagation. For TLEs specifically, the standard model is SGP4
(a simplified perturbation model that accounts for drag, oblateness, etc.) — Orekit implements
this as TLEPropagator, so you don't need to hand-derive SGP4, but you DO need to understand what
it's doing conceptually: not "the orbit is fixed," but "the orbit decays and shifts over time,
and this model predicts how."

TODO(you): implement propagate_object() below. Reference:
https://www.orekit.org/site-orekit-python/  (search "TLEPropagator")
"""

from setup_check import fetch_tles, DEBRIS_URL
import orekit
orekit.initVM()
from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir()
from org.orekit.propagation.analytical.tle import TLE , TLEPropagator
from org.orekit.frames import FramesFactory

def propagate_object(tle_line1, tle_line2, duration_hours=24, step_minutes=5):
    """
    Propagate a single TLE forward in time and return a list of (time, position_km) samples.

    STEPS TO IMPLEMENT (this is the actual learning — don't skip to an answer):
    1. Build an orekit TLE object from tle_line1/tle_line2.
    2. Build a TLEPropagator from it.
    3. Starting at the TLE's epoch, step forward every `step_minutes` for `duration_hours`.
    4. At each step, call propagator.propagate(date) and extract the PVCoordinates
       (position/velocity) in an inertial frame (e.g. EME2000 / GCRF).
    5. Return a list of dicts: {"t_seconds": ..., "position_km": [x, y, z]}

    WHY EME2000/inertial frame specifically: Earth is rotating underneath the orbit. If you
    propagate in an Earth-fixed frame you'll get nonsense — orbital mechanics equations of motion
    are derived in an inertial (non-rotating) frame. This trips up almost everyone the first time.
    """
    tle = TLE(tle_line1, tle_line2)
    propagator = TLEPropagator.selectExtrapolator(tle)
    start_date = tle.getDate()

    results = []
    t=0
    while t <= duration_hours * 3600:
        current_date = start_date.shiftedBy(float(t))
        state = propagator.propagate(current_date)
        pv = state.getPVCoordinates(FramesFactory.getEME2000())
        pos=pv.getPosition()
        x_km = pos.getX() / 1000.0
        y_km = pos.getY() / 1000.0
        z_km = pos.getZ() / 1000.0
        results.append({"t_seconds": t, "position_km": [x_km, y_km, z_km]})
        t=t + step_minutes * 60
    return results      
def period_minutes_from_altitude(altitude_km, earth_radius_km=6371.0, mu=398600.4418):
    """
    Quick sanity-check formula (no Orekit needed) — use this to sanity-check your propagator's
    output period against the textbook formula:

        T = 2*pi*sqrt(a^3 / mu)

    If your propagated orbit's period doesn't roughly match this, something's wrong upstream.
    """
    import math
    a = earth_radius_km + altitude_km
    return 2 * math.pi * math.sqrt(a ** 3 / mu) / 60.0


if __name__ == "__main__":
    objs = fetch_tles(DEBRIS_URL)
    target = objs[0]
    print(f"Propagating: {target['name']}")

    track = propagate_object(target["line1"], target["line2"])
    print(f"Got {len(track)} position samples")
    print("First sample:", track[0])
    print("Last sample:", track[-1])
