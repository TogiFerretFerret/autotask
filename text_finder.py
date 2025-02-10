import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageGrab

def fortege(small, target_text):
    """
    Finds the coordinates (center point) of the specified target text in a given cv2 image.

    This function downscales the image for faster OCR processing. It uses pytesseract to extract
    bounding box data from the image and then searches for a bounding box whose recognized text
    matches the target text (case-insensitive). Because cv2 image coordinates are typically double the
    pyautogui coordinates on high-DPI screens, this function performs a downscaling so that the OCR 
    operates on an image half the size of the original. The coordinates returned from the smaller image 
    correspond directly to pyautogui coordinates.

    Args:
        cv2_image (numpy.ndarray): Input image in cv2 (BGR) format.
        target_text (str): The text to search for (e.g., "Compose").

    Returns:
        tuple or None: (x, y) coordinates representing the center of the matched text region in 
                       pyautogui coordinates, or None if no match is found.
    """
    # Use pytesseract to extract data from the downscaled image.
    # Using --psm 6 assumes a single uniform block of text.
    data = pytesseract.image_to_data(small, config="--psm 6", output_type=pytesseract.Output.DICT)
    # PSM 6 cannot find >1 word. 
    words=target_text.split(" ")
    num_boxes = len(data['text'])
    target_text = target_text.lower().strip()
    word_locs={}
    for word in words:
        word_locs[word]=[]
    for i in range(num_boxes):
        word = data['text'][i].strip().lower()
        if word in words:
            # issue is what if it isn't near the other word? we can check by storing per-word
            left = data['left'][i]
            top = data['top'][i]
            width_box = data['width'][i]
            height_box = data['height'][i]
            # Compute the center coordinates in the downscaled image.
            center_x = left + width_box // 2
            center_y = top + height_box // 2
            word_locs[word].append((center_x//2, center_y//2))
    
    return None
def find_text_coordinates(target_text):
    image= ImageGrab.grab()
    image_np = np.array(image)
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    coords = fortege(img, target_text)
    return coords
