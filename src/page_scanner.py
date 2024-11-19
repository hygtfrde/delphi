import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

class BookPageScanner:
    def __init__(self, video_path, config=None):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open video: {video_path}")

        self.config = {
            'edge_lower': 50,
            'edge_upper': 150,
            'min_page_area': 10000,
            'noise_threshold': 1000,
            'frame_skip': 2,
            'quality_threshold': 0.8,
            'similarity_threshold': 0.8
        }
        if config:
            self.config.update(config)

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  # Get FPS for frame skipping
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.last_captured_frame = None

    def is_duplicate(self, frame, previous_frame):
        if previous_frame is None:
            return False

        # Resize to ensure compatible dimensions
        frame_resized = cv2.resize(frame, (previous_frame.shape[1], previous_frame.shape[0]))
        similarity = cv2.matchTemplate(frame_resized, previous_frame, cv2.TM_CCOEFF_NORMED).max()
        return similarity > self.config['similarity_threshold']

    def process_video(self):
        frame_skip = max(1, int(self.fps / 2))
        frame_number = 0
        from tqdm import tqdm
        total_frames = self.frame_count

        with tqdm(total=total_frames) as pbar:
            while self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = self.cap.read()
                if not ret:
                    break
                # Process the frame (placeholder for your logic)
                frame_number += frame_skip
                remaining_frames = total_frames - frame_number
                pbar.update(min(frame_skip, remaining_frames))

        self.cap.release()
