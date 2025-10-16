#/usr/bin/env sh
OUT="./out"
TMP="$OUT/tmp"

# Build Cython library, will also check if the relevant build tools are available (C++ Build Tools >2014)
python setup.py build_ext --inplace

# Ensure folders are present

if [ ! -d "$OUT" ]; then
    echo "$OUT Folder missing, creating..."
    mkdir "$OUT"
fi
if [ ! -d "$TMP" ]; then
    echo "$TMP Folder missing, creating..."
    mkdir "$TMP"
fi

if command -v ffmpeg >&2; then
  echo "FFMPEG found on PATH"
else
  echo "FFMPEG not found on PATH"
  exit
fi

# Run application
./ascii.py --webcam --colour
