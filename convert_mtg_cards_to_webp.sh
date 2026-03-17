#!/usr/bin/env bash

set -e

echo "Converting .jpg files in public/mtg to .png"

if ls public/mtg/*.jpg >/dev/null 2>&1; then
  mogrify -format png "public/mtg/*.jpg"
fi

echo "Clearing public/mtg/thumbnails"

rm -r public/mtg/thumbnails
mkdir -p public/mtg/thumbnails

for f in public/mtg/*.png; do
    echo "Converting $f to public/mtg/thumbnails/$(basename "${f%.*}").webp"
    convert "$f" -resize x724\> "public/mtg/thumbnails/$(basename "${f%.*}").webp"
done