#!/usr/bin/env bash

set -e

for f in public/art/*.jpg; do
    convert "$f" "public/art/$(basename "${f%.jpg}").png"
done

rm -r public/art/thumbnails
mkdir -p public/art/thumbnails

for f in public/art/*.png; do
    echo $f
    convert "$f" -resize x512\> "public/art/thumbnails/$(basename "${f%.*}").webp"
done