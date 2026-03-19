#!/usr/bin/env bash

set -e

echo "Converting .jpg files in public/art to .png"

if ls public/art/*.jpg >/dev/null 2>&1; then
  mogrify -format png "public/art/*.jpg"
fi

echo "Clearing public/art/thumbnails"

rm -r public/art/thumbnails
mkdir -p public/art/thumbnails

for f in public/art/*.png; do
    echo "Converting $f to public/art/thumbnails/$(basename "${f%.*}").webp"
    convert "$f" -resize x512\> "public/art/thumbnails/$(basename "${f%.*}").webp"
done