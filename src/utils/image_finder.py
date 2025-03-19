import time
start = time.time()
from PIL import ImageGrab, Image
import cv2
import pytesseract
from math import floor
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import CLIPProcessor, CLIPModel
import torch
import os
from tqdm import tqdm, trange
import torch._logging as logging
import platform

logging.set_logs(all=0)
print(f"Imports took {time.time() - start} seconds.")  # Dummy timing print

# Choose device (GPU if available, else CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

start = time.time()
# Load the CLIP model and processor globally
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name).to(device)
model.eval()
processor = CLIPProcessor.from_pretrained(model_name)
print(f"Model and processor loaded in {time.time() - start} seconds.")

def cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    """
    Computes cosine similarity between two 1D torch tensors.
    """
    return torch.nn.functional.cosine_similarity(a, b, dim=0).item()

def get_text_embedding(query: str) -> torch.Tensor:
    """
    Process the text query to obtain its embedding.
    """
    text_inputs = processor(text=query, images=None, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        text_features = model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features[0]

def score_region(cv2_image, text_embedding):
    """
    Scores a single image (region) against the text embedding.
    
    Args:
        cv2_image (np.array): Input region image in cv2 format.
        text_embedding (torch.Tensor): Precomputed text embedding.
    
    Returns:
        float: Cosine similarity score for the image region.
    """
    # Convert the cv2 image to a PIL image.
    image = Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    inputs = processor(text=None, images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        image_embedding = image_features[0]
    score = cosine_similarity(text_embedding, image_embedding)
    return score

def process_box(box_line, img, text_embedding):
    """
    Process a single pytesseract bounding box line.
    
    Draws the bounding box on the image and returns the score.
    """
    parts = box_line.split(' ')
    char, x, y, w, h, _ = parts
    x, y, w, h = int(x), int(y), int(w), int(h)
    # pytesseract bounding boxes are given with origin at the bottom-left.
    # We need to adjust for cv2 image which has origin at top-left.
    height = img.shape[0]
    # Crop region from cv2 image using proper coordinate conversion.
    # Note: In cv2, img[y1:y2, x1:x2] where y1 is top and y2 is bottom.
    # For pytesseract, y is bottom coordinate, and h is top coordinate.
    roi = img[height - h: height - y, x:w]
    score = score_region(roi, text_embedding)
    # Draw rectangle on original image (convert y coordinates accordingly)
    cv2.rectangle(img, (x, height - y), (w, height - h), (0, 255, 0), 1)
    return (score,roi, floor(x/2), floor((height-y)/2), floor(w/2), floor((height - h)/2))
def get_described_image_coords(query):
    start = time.time()
    text_embedding = get_text_embedding(query)
    print(f"Text embedding obtained in {time.time() - start} seconds.")
    print("Text embedding obtained successfully.")

    # Grab screenshot using PIL's ImageGrab and convert to cv2 format
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot.convert('RGB')), cv2.COLOR_RGB2BGR)
    img2=img
    
    # Get bounding boxes using pytesseract
    box = pytesseract.image_to_boxes(img)
    box2 = pytesseract.image_to_boxes(img)
    boxes=0
    if len(box)>len(box2):
        boxes=box
    else:
        boxes=box2
    for b in tqdm(boxes.splitlines()):
        b = b.split(' ')
        img2 = cv2.rectangle(img2, (int(b[1]), img.shape[0] - int(b[2])), (int(b[3]), img.shape[0] - int(b[4])), (0, 255, 0), 1)
    print(f"Bounding boxes obtained in {time.time() - start} seconds.")
    cv2.imwrite('bb.png', img2)
    # Process each bounding box concurrently using ThreadPoolExecutor
    scores = []
    count = 0
    start = time.time()
    print("Box Count:",len(boxes.splitlines()))
    max_score = 0
    max_score_img = None
    max_score_box = None
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for b in tqdm(boxes.splitlines()):
            futures.append(executor.submit(process_box, b, img, text_embedding))
        with tqdm(total=len(futures)) as pbar:
            for future in as_completed(futures):
                try:
                    count += 1
                    pbar.update(1)
                    score = future.result()[0]
                    scores.append(score)
                    if score>max_score:
                        max_score=score
                        max_score_img=future.result()[1]
                        max_score_box=future.result()[2:]
                except Exception as e:
                    pass
    tx=(max_score_box[0]+max_score_box[2])/2
    ty=(max_score_box[1]+max_score_box[3])/2
    tx=floor(tx)
    ty=floor(ty)
    return (tx,ty)

def is_macos():
    return platform.system() == "Darwin"
