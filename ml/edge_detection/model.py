from .teed.model import edge_detection as edge_detection_teed
from .canny.model import edge_detection as edge_detection_canny


def edge_detection(f: bytes, mode="medium"):
    """
    Edge detection based on modes.

    For easy and hard, uses canny edge detection

    For medium, uses teed.
    """

    if mode == "easy":
        return edge_detection_canny(f, 200, 400)
    elif mode == "medium":
        return edge_detection_teed(f)
    elif mode == "hard":
        return edge_detection_canny(f, 100, 200)
    else:
        return NotImplementedError()
