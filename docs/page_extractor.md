# Page Extractor

`BookPageExtractor`, extracts specific frames from a video containing book pages and saves them as individual images. It utilizes OpenCV (cv2) for video processing and image manipulation.

## How It Works

### Initialization

- The program takes the path to a video file (`video_path`) as input during initialization (`__init__`).
- It initializes a video capture object (`self.cap`) using OpenCV's `VideoCapture` class to read frames from the video.
- The video codec is set to 'MJPG' to ensure no audio is loaded (`cv2.CAP_PROP_FOURCC`).
- It retrieves the total number of frames in the video (`self.frame_count`), at the rate (FPS) specified in the video file.

### Are Pages Visible?

- The `are_pages_visible` method takes a frame from the video as input.
- Converts the frame to grayscale (`cv2.cvtColor`).
- Performs edge detection using Canny edge detector (`cv2.Canny`), with specific thresholds for edge detection.
- Detects contours in the edge-detected image (`cv2.findContours`).
- Filters out contours based on area to identify potential page boundaries (`page_contours`).
- Checks if exactly 2 page contours are detected, indicating both facing left and right pages are visible.

### Is Noise Detected?

- The `is_noise_detected` method takes a frame from the video and converts the input frame from a color image (BGR format) to a grayscale image using cv2.cvtColor. This simplifies processing by reducing the image to one intensity channel.
- The grayscale image is processed with `self.background_subtractor.apply(gray)`, which creates a foreground mask (`fg_mask`). This mask highlights areas of the image that differ from the background model, indicating potential movement or noise.
- Using cv2.findContours(`fg_mask`, `cv2.RETR_EXTERNAL`, `cv2.CHAIN_APPROX_SIMPLE)`, the function identifies the contours (boundaries) of objects in the foreground mask. It retrieves the outermost contours, which represent significant changes in the image.
- The total area of all detected contours is calculated by summing the areas of individual contours using `sum(cv2.contourArea(contour)`. This gives a measure of the total detected change or noise in the image.
- If `noise_area` exceeds `noise_threshold`, it returns True, indicating significant noise. Otherwise, it returns False, indicating no significant noise.

### Page Extraction

- The `extract_page` method saves a frame as a JPEG image.
- Takes the frame, output directory (`output_path`), and frame number (`frame_number`) as input.
- Constructs the file name using `os.path.join` and writes the frame to disk using `cv2.imwrite`.
- May require a validation step to ensure that only necessary pages are extracted, for instance not having duplicates or other noise.

### Processing the Video

- The `process_video` method iterates through all frames of the video.
- Checks if pages are visible in each frame using `are_pages_visible`.
- If pages are visible, extracts the frame using `extract_page`.
- Increments the frame number and continues until all frames are processed or no more frames are available.
- Releases the video capture object (`self.cap`) once processing is complete.

