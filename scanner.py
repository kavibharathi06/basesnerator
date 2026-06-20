import cv2
import numpy as np


def order_points(points):

    rect = np.zeros((4, 2), dtype="float32")

    s = points.sum(axis=1)

    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)

    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]

    return rect



def warp_document(image, points):

    rect = order_points(points)

    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)

    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)

    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth, 0],
        [maxWidth, maxHeight],
        [0, maxHeight]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(
        rect,
        dst
    )

    return cv2.warpPerspective(
        image,
        M,
        (maxWidth, maxHeight)
    )



# scanner.py

# ... (keep your existing order_points and warp_document functions)

def scan_document(image):
    original = image.copy()
    
    # Calculate total area of the resized image for fallback thresholding
    resized_height = 500
    resized_width = int(image.shape[1] * resized_height / image.shape[0])
    total_area = resized_height * resized_width

    resized = cv2.resize(image, (resized_width, resized_height))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    document = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            # FIX: Ensure the detected contour isn't just a tiny piece of text or artifact
            if cv2.contourArea(c) > (total_area * 0.15): 
                document = approx
                break

    if document is not None:
        warped = warp_document(
            original,
            document.reshape(4, 2) * ratio
        )
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    else:
        # Fallback to full image if no large 4-cornered object is found
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding
    scanned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,
        10
    )

    return scanned