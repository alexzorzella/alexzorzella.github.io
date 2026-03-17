#!/usr/bin/env bash

set -e

echo "Converting .jpg files in public/art to .png"

for f in public/art/*.jpg; do
    convert "$f" "public/art/$(basename "${f%.jpg}").png"
done

echo "Clearing public/art/thumbnails"

rm -r public/art/thumbnails
mkdir -p public/art/thumbnails

for f in public/art/*.png; do
    echo "Converting $f"
    convert "$f" -resize x512\> "public/art/thumbnails/$(basename "${f%.*}").webp"
done