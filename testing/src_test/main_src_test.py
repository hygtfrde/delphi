import sys
import os
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.insert(0, src_path)
from text_extractor import TextExtractor

def main():
    test_frames_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_frames'))
    absolute_test_frames_dir = os.path.abspath(test_frames_dir)
    test_text_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_output_text'))
    absolute_test_text_dir = os.path.abspath(test_text_dir)
    
    scanned_frames = os.listdir(absolute_test_frames_dir)
    extractor_test = TextExtractor(absolute_test_text_dir)
    for frame in scanned_frames:
        extractor_test.extract_text(f'{test_frames_dir}/{frame}')
    return

if __name__ == '__main__':
    main()
