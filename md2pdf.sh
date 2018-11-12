#!/bin/bash

if [ "$1" == "" ]; then
	echo "Converts a Markdown file into PDF using:"
	echo "https://www.markdowntopdf.com"
	echo ""
	echo "Usage: md2pdf <md file>"
	exit 1
fi

if [ "$(which curl)" == "" ]; then
	echo "The progran curl is not available, install it"
	exit 1
fi

if [ "$(which jq)" == "" ]; then
	echo "The progran jq is not available, install it"
	exit 1
fi

URL="https://www.markdowntopdf.com"
F=$1
OUT="${F%.*}.pdf"

RES=$(curl -sF "file=@$F" "$URL/app/upload")

FN=$(echo "$RES" | jq -r '.urlfilename')
FOLDER=$(echo "$RES" | jq -r '.foldername')

curl "$URL/app/download/$FOLDER/$FN" -o "$OUT"
