import time
start = time.time()
from PIL import ImageGrab, Image
import cv2
import pytesseract
import numpy as np
from transformers import CLIPProcessor, CLIPModel
import torch
print(f"Imports took {time.time() - start} seconds.")
print("yes the imports took this long")
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
        # Normalize the text feature vector.
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features[0]

def score_region(cv2_image, text_embedding):
    """
    Scores a single region defined by the bounding box against the text embedding.

    Args:
        cv2_image (np.array): Input image in cv2 format.
        bbox (tuple): Bounding box (x, y, w, h).
        text_embedding (torch.Tensor): Precomputed text embedding.

    Returns:
        float: Cosine similarity score for the region.
    """
    # Convert the cv2 image to a PIL image.
    image = Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    inputs = processor(text=None, images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        # Normalize the image feature vector.
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        image_embedding = image_features[0]
    score = cosine_similarity(text_embedding, image_embedding)
    return score
start = time.time()
text_embedding = get_text_embedding("Google Chrome App Icon")
print(f"Text embedding obtained in {time.time() - start} seconds.")
print("Text embedding obtained successfully.")
screenshot = ImageGrab.grab()
img=cv2.cvtColor(np.array(ImageGrab.grab().convert('RGB')), cv2.COLOR_RGB2BGR)
box=pytesseract.image_to_boxes(img)
box2=pytesseract.image_to_boxes(img)
boxes=0
if len(box)<len(box2):
    boxes=box
else:
    boxes=box2
# omg this is so slow make it PaRaLlEl
import threading
def proc_box(b):
    b = b.split(' ')
    char, x, y, w, h, _ = b
    x, y, w, h = int(x), int(y), int(w), int(h)
    # Take the rectangle and save just that part of the image to a new file
    rect=img[y:h,x:w]
    score = score_region(rect, text_embedding)
    print(f"Score for region: {score}")
    cv2.rectangle(img, (x, img.shape[0] - y), (w, img.shape[0] - h), (0, 255, 0), 1)
for b in boxes.splitlines():
    x=threading.Thread(target=proc_box, args=(b,))
    x.start()
cv2.imwrite('img.png', img)

