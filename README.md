# Delphi
An extractor for video files to text

## Software Components

### Page Extractor (Scanner)
- Utilize motion detection to recognize a full page
  -- Extract the still frame
- Increment and count prefixes and page numbers

### Text Extractor
- Feed in the raw pages as image files and generate text pages
  -- Utilize Tesseract OCR

### Main.py
- Entry point to run program

## Set Up

### Venv
- Start your Venv or Conda environment before downloading <br>
`conda create --name delphi`
`conda activate delphi`
### Pip
- Then use Pip to install dependencies <br>
`pip install -r requirements.txt`
### Running
- Before extracting pages from a video, add your video file in `test` directory.
- Change the name of the Video Path in `main.py`:
```
    # Video Path
    video_path = 'test/test-scan.mov'
```
- Alternatively, set a custom Video Path for your liking


