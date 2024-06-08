# Delphi
A smart page scanner for video to text extraction

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


