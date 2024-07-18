import cv2
import numpy as np
from scipy import ndimage

class QualityRating:
    def __init__(self, image_path=None, frame=None):
        if image_path:
            self.frame = cv2.imread(image_path)
        elif frame is not None:
            self.frame = frame
        else:
            raise ValueError("Either image_path or frame must be provided.")
    
    def sharpness(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var
    
    def brightness(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        return brightness
    
    def contrast(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        contrast = gray.std()
        return contrast
    
    def noise(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        noise = np.var(gray - ndimage.median_filter(gray, size=3))
        return noise
    
    def quality_score(self):
        sharpness_score = self.sharpness()
        brightness_score = self.brightness()
        contrast_score = self.contrast()
        noise_score = self.noise()
        
        # Normalize and combine scores (this is a basic method, you can refine it)
        sharpness_weight = 0.4
        brightness_weight = 0.2
        contrast_weight = 0.2
        noise_weight = 0.2
        
        total_score = (sharpness_score * sharpness_weight) - (brightness_score * brightness_weight) + (contrast_score * contrast_weight) - (noise_score * noise_weight)
        return total_score
    
    def print_scores(self):
        print(f"Sharpness: {self.sharpness()}")
        print(f"Brightness: {self.brightness()}")
        print(f"Contrast: {self.contrast()}")
        print(f"Noise: {self.noise()}")
        print(f"Quality Score: {self.quality_score()}")
        
    def curviness():
        return
    
    def rotation():
        return 
    
    
    

