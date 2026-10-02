from enum import Enum


class COLOR(Enum):
    """
    An Enum that stores the BRGA colors to use in the render image
    function as a tuple of hexadecimal values.

    Attributes:
        WHITE: Represents the hexadecimal value of white color.
        BLACK: Represents the hexadecimal value of black color.
        RED: Represents the hexadecimal value of red color.
        GREEN: Represents the hexadecimal value of green color.
        BLUE: Represents the hexadecimal value of blue color.
        YELLOW: Represents the hexadecimal value of yellow color.
        MAGENTA: Represents the hexadecimal value of magenta color.
        CYAN: Represents the hexadecimal value of cyan color.
        GREY: Represents the hexadecimal value of grey color.
        DARK_BLUE: Represents the hexadecimal value of dark blue color.

        The next variables represents the color palette of the 42 urduliz
        coalitions.

        Nostromo:
            NOS_PRIMARY: Represents the hexadecimal value of purple color.
            NOS_BG: Represents the hexadecimal value of dark purple color.
            NOS_LIGHT_BLUE: Represents the hexadecimal
                value of light blue color.
        Nautilus:
            NAU_PRIMARY: Represents the hexadecimal value of green color.
            NAU_BG: Represents the hexadecimal value of dark green color.
            NAU_LIGHT_GREEN: Represents the hexadecimal
                value of light green color.
        Magrathea:
            MAG_PRIMARY: Represents the hexadecimal value of yellow color.
            MAG_BG: Represents the hexadecimal value of dark orange color.
            MAG_LIGHT_YELLOW: Represents the hexadecimal
                value of light yellow color.

    """
    WHITE = (0xE7, 0xD9, 0xCD, 0xFF)
    BLACK = (0x00, 0x00, 0x00, 0xFF)
    RED = (0x00, 0x00, 0xFF, 0xFF)
    GREEN = (0x00, 0xFF, 0x00, 0xFF)
    BLUE = (0xFF, 0x00, 0x00, 0xFF)
    YELLOW = (0x00, 0xFF, 0xFF, 0xFF)
    MAGENTA = (0xFF, 0x00, 0xFF, 0xFF)
    CYAN = (0xFF, 0xFF, 0x00, 0xFF)
    GREY = (0xAB, 0x92, 0x7D, 0xFF)
    DARK_BLUE = (0x24, 0x1A, 0x16, 0xFF)

    # Nostromo
    NOS_PRIMARY = (0xE2, 0x28, 0x9E, 0xFF)
    NOS_BG = (0x2A, 0x0E, 0x1D, 0xFF)
    NOS_LIGHT_BLUE = (0xE3, 0xAA, 0x62, 0xFF)

    # Nautilus
    NAU_PRIMARY = (0x83, 0x88, 0x39, 0xFF)
    NAU_LIGTH_GREEN = (0xBC, 0xBA, 0x00, 0xFF)
    NAU_BG = (0x53, 0x51, 0x04, 0xFF)

    # Magrathea
    MAG_PRIMARY = (0x40, 0xAA, 0xE3, 0xFF)
    MAG_BG = (0x22, 0x1A, 0x3F, 0xFF)
    MAG_LIGTH_YELLOW = (0x25, 0x37, 0x86, 0xFF)
