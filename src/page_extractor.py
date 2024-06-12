import cv2
import numpy as np
import os

class BookPageExtractor:
    def __init__(self, video_path):
        self.video_path = video_path

        # store the video capture object
        self.cap = cv2.VideoCapture(video_path)
        
        # set CAP_PROP_FOURCC to 'MJPG' to ensure no audio is loaded
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        # retrieve the total number of frames in the video file
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def are_pages_visible(self, frame):
        # Logic to detect if both pages are visible
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        page_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 10000 < area < 50000:
                page_contours.append(contour)

        if len(page_contours) == 2:
            return True
        return False
    
    # Validation step
    def are_pages_unique():
        pass

    def extract_page(self, frame, output_path, frame_number):
        # Save the frame as an image file
        file_name = os.path.join(output_path, f'page_frame_{frame_number}.jpg')
        cv2.imwrite(file_name, frame)
        print(f'Frame {frame_number} saved as {file_name}')

    def process_video(self, output_path):
        frame_number = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.are_pages_visible(frame):
                self.extract_page(frame, output_path, frame_number)
            frame_number += 1

        self.cap.release()

