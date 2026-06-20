import cv2
import pytesseract
import numpy as np

def preprocess(img):
    # 1. Convert to Grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # 2. Check if the image has a dark background
    # If the average pixel value is low (< 127), it's a dark slide.
    # Inverting it makes it black text on white background, which OCR loves.
    if np.mean(gray) < 127:
        gray = cv2.bitwise_not(gray)

    # 3. Upscale for better small text recognition
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC # Better than LINEAR for text upscaling
    )

    # 4. Light Denoising
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # 5. Clean Otsu Thresholding (More reliable for digital graphics than Adaptive)
    _, clean_img = cv2.threshold(
        gray, 
        0, 
        255, 
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return clean_img


def extract_text(image):
    img = preprocess(image)

    # PSM 3 (Fully automatic page segmentation) is generally much better 
    # than PSM 6 for standard reading blocks like presentation slides.
    config = (
        "--oem 3 "
        "--psm 3 "
        "-l eng"
    )

    text = pytesseract.image_to_string(
        img,
        config=config
    )

    return text