"""
Simple (x, y) grid lookup:
 - TAG_POS maps every AprilTag ID to its (x, y) coordinate.
 - heading_lookup(frm, to) returns 'N', 'E', 'S', or 'W'.
"""

# Map each ID to a grid cordinate
TAG_POS = {
    1: (0,0),
    2: (1,0),
    3: (2,0),
    4: (2,1),
    5: (1,1),
    6: (0,1),
}

# Convert any edge to compass heading
def heading_lookup(frm, to):
    try:
        x1, y1 = TAG_POS[frm]
        x2, y2 = TAG_POS[to]
    except KeyError as e:
        raise KeyError(f"Tag {e} missing from TAG_POS dict")
    
    dx, dy = x2 - x1, y2 - y1
    if dx == 1 and dy == 0: return "E"
    elif dx == -1 and dy == 0: return "W"
    elif dx == 0 and dy == -1: return "N"
    elif dx == 0 and dy == 1: return "S"
    else:
        raise ValueError(f"Cannot infer heading for {frm} -> {to};"
                         f"dx={dx}, dy={dy}")
