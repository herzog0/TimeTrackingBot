#!/bin/sh

RED='\033[0;31m'
DIR=deps
echo "Initializing"

if ! command -v python3.8 > /dev/null 2>&1
then
    echo "${RED}Warning: You must have python3.8 installed!"
    exit
fi

python3.8 -m pip install --ignore-installed --target="$DIR" -r requirements.txt

echo "Building dist"
[ -d dist ] && rm -r dist
mkdir dist
cp -R "$DIR/." dist
cp -R "src" dist
cp lambda_handler.py dist

echo "Building deployment package"
cd dist || { echo "${RED}Dist folder not found!!"; exit 1; }
zip -r -q -9 -T deployment .
mv deployment.zip ../
