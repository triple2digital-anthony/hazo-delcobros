import cv2

def display_frame(window_name, frame):
    cv2.imshow(window_name, frame)

def save_frame(frame, output_path):
    cv2.imwrite(output_path, frame)
