import pyautogui
import time
from text_finder import find_text_coordinates

subject_coords = find_text_coordinates("Subject")
saved_subject_coords = subject_coords
pyautogui.click(saved_subject_coords[0]+50, saved_subject_coords[1])
pyautogui.write("Click recognition")
time.sleep(0.5)

pyautogui.click(saved_subject_coords[0], saved_subject_coords[1] + 30)
pyautogui.write("Hi Tahlioubeah, I got click recognition to work through a python script that utilizes a library to find text on the screen and click those coordinates.")
