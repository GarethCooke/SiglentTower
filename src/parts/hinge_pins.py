# hinge_pins.py — the door hinge's two pins (P5: a printed Ø2.9 passes the 3.2 bores, 3.0 binds). Ø2.9 x 24 (the knuckle's
# length), standing on a Ø8 x 0.6 snap-off disc so it prints vertical without a brim; 0.4 chamfer on the free end as a
# lead-in. Black PETG (ABS is fine too; not PLA — it snaps). Glued at both ends into the DOOR leaf's segments with CA;
# the frame leaf's middle segment turns on it. Snap the disc off, dress the stub flat with a blade. v1 2026-10-20.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import PIN_HOLE_D
PIN_D, PIN_L, DISC_D, DISC_T = 2.9, 24.0, 8.0, 0.6
assert PIN_D < PIN_HOLE_D

def pin():
    p = cq.Workplane("XY").circle(DISC_D / 2).extrude(DISC_T).faces(">Z").workplane().circle(PIN_D / 2).extrude(PIN_L)
    return p.faces(">Z").chamfer(0.4)

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "door")); os.makedirs(OUT, exist_ok=True)
    two = pin().union(pin().translate((14, 0, 0)))
    path = os.path.join(OUT, "hinge-pins-v1.stl"); cq.exporters.export(two, path, tolerance=0.005, angularTolerance=0.05)
    bb = two.val().BoundingBox(); print(f"hinge-pins-v1  {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {two.val().Volume()/1000:.2f} cm3  — two pins Ø{PIN_D} x {PIN_L} on discs, standing as exported, black PETG, no brim")
    check(path, min_rest_frac=0.3, max_down_frac=0.3)
