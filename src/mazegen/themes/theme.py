from ..enums import COLOR

"""
    Helper variable to store the fixed themes.
"""


THEMES: list[tuple[str, dict[str, COLOR]]] = [
    ("nostromo",  {
        "background": COLOR.NOS_BG,
        "walls": COLOR.NOS_PRIMARY,
        "solution": COLOR.NOS_LIGHT_BLUE,
        "entry": COLOR.MAGENTA,
        "exit": COLOR.RED,
        "pattern": COLOR.WHITE
    }),
    ("nautilus",  {
        "background": COLOR.NAU_BG,
        "walls": COLOR.NAU_PRIMARY,
        "solution": COLOR.NAU_LIGTH_GREEN,
        "entry": COLOR.MAGENTA,
        "exit": COLOR.RED,
        "pattern": COLOR.WHITE
    }),
    ("magrathea",  {
        "background": COLOR.MAG_BG,
        "walls": COLOR.MAG_PRIMARY,
        "solution": COLOR.MAG_LIGTH_YELLOW,
        "entry": COLOR.MAGENTA,
        "exit": COLOR.RED,
        "pattern": COLOR.WHITE
    }),
    ]
