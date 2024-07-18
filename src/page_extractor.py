import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

class BookPageExtractor:
    def __init__(self, video_path):
        try:
            self.video_path = video_path

            # store the video capture object
            self.cap = cv2.VideoCapture(video_path)
            
            if not self.cap.isOpened():
                raise ValueError(f"Error: Could not open video {video_path}")
            
            # set CAP_PROP_FOURCC to 'MJPG' to ensure no audio is loaded
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            
            # retrieve the total number of frames in the video file
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print('FRAME COUNT: ', self.frame_count)

            self.frame_number = 0
            
            # To store the last captured frame
            self.last_captured_frame = None

            # Background subtractor for noise detection
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        except Exception as e:
            print(f'Error: {e}, \ninitializing BookPageExtractor and video_path: {video_path}')

    def are_pages_visible(self, frame):
        # convert to greyscale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Edge Detection:
        edges = cv2.Canny(gray, 50, 150)
        
        # detect contours (boundaries) and hierarchy
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
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
    
    # Validation step
    def are_pages_unique():
        pass

    def is_noise_detected(self, frame, noise_threshold=5000):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply background subtractor
        fg_mask = self.background_subtractor.apply(gray)

        # Find contours in the foreground mask
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the area of all detected contours
        noise_area = sum(cv2.contourArea(contour) for contour in contours)

        # If the area of the noise is above the threshold, consider it noise
        if noise_area > noise_threshold:
            return True
        return False
    
    def are_pages_unique(self, frame, threshold=0.9):
        if self.last_captured_frame is None:
            # If there's no last frame, this is the first one, so it's unique
            self.last_captured_frame = frame
            return True
        
        # Convert current frame to grayscale
        gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Convert the last captured frame to grayscale
        gray_last = cv2.cvtColor(self.last_captured_frame, cv2.COLOR_BGR2GRAY)
        
        # Compute Structural Similarity Index (SSIM) between the current and last frame
        similarity, _ = ssim(gray_current, gray_last, full=True)
        
        # Determine if the current frame is unique
        is_unique = similarity < threshold
        
        if is_unique:
            self.last_captured_frame = frame
        
        return is_unique

    def extract_page(self, frame, output_path):
        file_name = os.path.join(output_path, f'page_frame_{self.frame_number}.jpg')
        cv2.imwrite(file_name, frame)
        print(f'Frame {self.frame_number} saved as {file_name}')


    def process_video(self, output_path):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.are_pages_visible(frame) and self.are_pages_unique(frame):
                self.extract_page(frame, output_path)
            self.frame_number += 1

        self.cap.release()

