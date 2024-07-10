#!/bin/bash

# Define the directories
DIR1="testing/test_output_text"
DIR2="testing/test_frames"

# Function to delete files except those ending with .md
cleanup_directory() {
  local dir=$1
  if [ -d "$dir" ]; then
    find "$dir" -type f ! -name "*.md" -delete
    echo "Cleaned up $dir except for .md files."
  else
    echo "Directory $dir does not exist."
  fi
}

# Cleanup both directories
cleanup_directory "$DIR1"
cleanup_directory "$DIR2"
