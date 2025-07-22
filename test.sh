#!/bin/bash
set -e # Encerra o script se houver erro

mkdir python

echo "Get numpy"
pip install -t python numpy --platform manylinux2014_aarch64 --only-binary=:all:
cd python
rm -rf *dist-info
cd ..
echo "Zip numpy"
python -m zipfile -c numpy_layer.zip python
echo "Move numpy to /layers"
mv numpy_layer.zip src/layers
rm -rf python/

echo "Spacy Model"
mkdir work_dir

echo "Unzip to workdir"
cp ./fragm/pt_core_news_sm-dist-info.zip ./work_dir
cd work_dir
unzip ./pt_core_news_sm-dist-info.zip

echo "Get pt_core"
curl -L -o ./pt_core_news_sm.tar.gz https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.8.0/pt_core_news_sm-3.8.0.tar.gz
tar -xzf pt_core_news_sm.tar.gz

echo "Create new zip"
powershell.exe Compress-Archive -Path pt_core_news_sm-3.8.0.dist-info,pt_core_news_sm-3.8.0/pt_core_news_sm -DestinationPath pt_core_news_sm.zip
echo "Move to /models"
cd ..
mkdir models
mv work_dir/pt_core_news_sm.zip models/
rm -rf work_dir
echo "Finish"