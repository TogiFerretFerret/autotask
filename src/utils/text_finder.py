import cv2
import pytesseract
import numpy as np
import math
from PIL import Image, ImageGrab
import platform

def fortege(cv2_image, target_text, cluster_distance_thresh=50):
    """
    Finds the center coordinates (in pyautogui coordinate space) of the specified target text within a cv2 image.
    
    This function downsizes the image (by half) for faster OCR processing (the downscaled coordinates correspond to
    pyautogui coordinates, given that cv2 coordinates are typically double on high-DPI screens) and then uses pytesseract 
    to extract detailed data for each recognized word from the original RGB image. It supports an arbitrary number of 
    target words by finding all recognized words that match any of the words in the target_text (case-insensitive), 
    then clustering the matched words based on spatial proximity. The cluster with the most matches is chosen, and its 
    combined bounding box center is returned.
    
    Args:
        cv2_image (numpy.ndarray): Input image in cv2 BGR format.
        target_text (str): Target text to find (can consist of multiple words, e.g., "Compose Email").
        cluster_distance_thresh (int, optional): Distance threshold (in pixels on the downscaled image) for clustering
                                                 recognized words. Default is 50.
        
    Returns:
        tuple or None: (x, y) coordinates representing the center of the matched cluster in pyautogui coordinates,
                       or None if no matching region is found.
    """
    # Downscale the image by 2 for speed. (Coordinates in the downscaled image correspond to pyautogui coordinates.)
    height, width, _ = cv2_image.shape
    small = cv2.resize(cv2_image, (width // 2, height // 2))
    # Convert from BGR to RGB; Tesseract works better with RGB.
    small_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    
    # Use pytesseract to extract detailed OCR data.
    data = pytesseract.image_to_data(small_rgb, config="--psm 6", output_type=pytesseract.Output.DICT)
    
    # Prepare target words list (lowercase, stripped)
    target_words = [word.strip() for word in target_text.lower().split()]
    if not target_words:
        return None

    # Collect recognized words (only non-empty entries) with their bounding box and midpoints.
    matched_words = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        word_text = data['text'][i].strip().lower()
        if not word_text:
            continue
        if word_text in target_words:
            left = data['left'][i]
            top = data['top'][i]
            width_box = data['width'][i]
            height_box = data['height'][i]
            mid_x = left + width_box / 2
            mid_y = top + height_box / 2
            matched_words.append({
                'text': word_text,
                'left': left,
                'top': top,
                'right': left + width_box,
                'bottom': top + height_box,
                'mid_x': mid_x,
                'mid_y': mid_y
            })
    
    if not matched_words:
        return None

    # Cluster the matched words using a simple greedy algorithm based on Euclidean distance between centers.
    clusters = []  # each cluster is a list of words (dictionaries)
    
    for word in matched_words:
        added = False
        for cluster in clusters:
            # Compute the current cluster center (average of word centers in the cluster)
            avg_x = sum(w['mid_x'] for w in cluster) / len(cluster)
            avg_y = sum(w['mid_y'] for w in cluster) / len(cluster)
            distance = math.hypot(word['mid_x'] - avg_x, word['mid_y'] - avg_y)
            if distance < cluster_distance_thresh:
                cluster.append(word)
                added = True
                break
        if not added:
            clusters.append([word])
    
    # Select the cluster with the most words; if tie, choose the one with the smallest bounding box area.
    best_cluster = None
    for cluster in clusters:
        if best_cluster is None or len(cluster) > len(best_cluster):
            best_cluster = cluster
        elif len(cluster) == len(best_cluster):
            # Compare bounding box areas.
            def bbox_area(cl):
                l = min(w['left'] for w in cl)
                t = min(w['top'] for w in cl)
                r = max(w['right'] for w in cl)
                b = max(w['bottom'] for w in cl)
                return (r - l) * (b - t)
            if bbox_area(cluster) < bbox_area(best_cluster):
                best_cluster = cluster

    # Compute the combined bounding box of the best cluster.
    if best_cluster:
        combined_left = min(w['left'] for w in best_cluster)
        combined_top = min(w['top'] for w in best_cluster)
        combined_right = max(w['right'] for w in best_cluster)
        combined_bottom = max(w['bottom'] for w in best_cluster)
        center_x = combined_left + (combined_right - combined_left) // 2
        center_y = combined_top + (combined_bottom - combined_top) // 2
        return (center_x, center_y)
    
    return None
    
def find_text_coordinates(target_text):
    image= ImageGrab.grab()
    image_np = np.array(image)
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    coords = fortege(img, target_text)
    return coords

def is_macos():
    return platform.system() == "Darwin"
