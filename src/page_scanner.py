import cv2
from tqdm import tqdm
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

    def extract_page(self, frame, output_path):
        try:
            file_name = os.path.join(output_path, f'page_frame_{self.frame_number:05d}.jpg')
            cv2.imwrite(file_name, frame)
        except Exception as e:
            print(f"Failed to save frame {self.frame_number}: {e}")


    def process_video(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        self.frame_skip = max(1, int(self.fps / 2))  # Skip to process approximately 2 frames per second
        self.frame_number = 0
        self.total_frames = self.frame_count
        
        print('Video Upload FRAME COUNT = ', self.frame_count)

        with tqdm(total=self.total_frames) as pbar:
            while self.cap.isOpened():
                # Set the frame position to the current frame number
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
                ret, frame = self.cap.read()
                if not ret:
                    break

                # Extract and save the current frame
                self.extract_page(frame, output_path)

                # Increment frame number by the skip value
                self.frame_number += self.frame_skip

                # Update progress bar
                remaining_frames = self.total_frames - self.frame_number
                pbar.update(min(self.frame_skip, remaining_frames))

        self.cap.release()
        print(f"Frames saved to directory: {output_path}")

