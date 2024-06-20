# Delphī
<img src="image_assets/delphi_logo.svg" alt="Delphī" width="300" height="200">

![Contributions Welcome](image_assets/contributors_welcome.svg)

A Python extractor program for video files to raw text

## Software Components in `src`

### Page Extractor
- Utilize motion detection to recognize a full page, scanning its contents
  - Extract the still frame
- Increment and count prefixes and page numbers

### Text Extractor
- Feed in the raw pages as image files and generate text pages
  - Utilize Tesseract OCR

## Set Up and Installation

### Virtual Enviornment
- Start your Conda environment before downloading any modules with Pip <br>
  - `conda create --name delphi`
  - `conda activate delphi`
  - Turn it off: `conda deactivate`
- For `venv` from Python Standard Library
  - Create a new Venv: `python -m venv delphi`
  - Windows: `.\delphi\Scripts\activate`
  - Mac/Linux: `source delphi/bin/activate`
  - Turn it off: `deactivate`

### Pip
- Then use Pip to install dependencies <br>
`pip install -r requirements.txt`

## Running
- Before extracting pages from a video, add your video file in `test` directory.
- Change the name of the Video Path in `main.py`:
```python
    # Video Path
    video_path = 'test/test-scan.mov'
```
- Alternatively, set a custom Video Path for your liking

### Main.py
- Entry point to run program: `python main.py`
- Images will be extracted into a `output_frames` folder
- Text file will be saved as ..... WIP


