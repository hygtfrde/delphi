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
        # convert to greyscale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Edge Detection:
        # threshold1 (50): Any pixel with a gradient below this value is considered not to be an edge
        # threshold2 (150): Any pixel with a gradient above this value is considered a strong edge.
        edges = cv2.Canny(gray, 50, 150)
        
        # detect contours (boundaries) and heirarchy
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        page_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            # filter out contours that are unlikely to represent entire pages
            if 10000 < area < 50000:
                page_contours.append(contour)

        # if page contours is 2 then both full facing left and right pages are visible
        if len(page_contours) == 2:
            return True
        return False

    def extract_page(self, frame, output_path, frame_number):
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

