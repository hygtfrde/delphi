#!/bin/bash

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DIR1="$SCRIPT_DIR/../testing/test_output_text"
DIR2="$SCRIPT_DIR/../testing/test_frames"


cleanup_directory() {
  local dir=$1
  if [ -d "$dir" ]; then
    find "$dir" -type f ! -name "*.md" -delete
    echo "Cleaned up $dir except for .md files."
  else
    echo "Directory $dir does not exist."
  fi
}


cleanup_directory "$DIR1"
cleanup_directory "$DIR2"
