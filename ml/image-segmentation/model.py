def image_segmentation(f: bytes, tl: tuple[int, int], br: tuple[int, int]) -> bytes:
    """
    Convert a full-color image into a single mask based on the bounding boxes
    specified by tl and br.

    Args:
        f: binary file representing an image JPG or PNG
        tl: top-left coordinate of the bounding box mask
        br: bottom-right coordinate of the bounding box mask

    Returns:
        A binary file representing an image JPG or PNG
    """
