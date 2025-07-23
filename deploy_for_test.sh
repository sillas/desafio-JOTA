#!/bin/bash
set -e # Encerra o script se houver erro

# --- Configuração ---
STACK_NAME="classification-app"
REGION="us-east-1"
LOCAL_MODELS_PATH="models/"

echo "Passo 0: preparando as camadas do Lambda"

mkdir python

echo "Numpy arch64"
pip install -t python numpy --platform manylinux2014_aarch64 --only-binary=:all:
cd python
rm -rf *dist-info
cd ..
python -m zipfile -c numpy_layer.zip python
rm -rf python/*
mv -r numpy_layer.zip src/layers

echo "Spacy Model"
mkdir work_dir
curl -L -o ./work_dir/pt_core_news_sm.tar.gz https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.8.0/pt_core_news_sm-3.8.0.tar.gz
unzip work_dir/pt_core_news_sm-dist-info.zip -d ./work_dir/
tar -xzf models/pt_core_news_sm.tar.gz -C ./work_dir
powershell.exe Compress-Archive -Path work_dir/pt_core_news_sm-3.8.0.dist-info,work_dir/pt_core_news_sm-3.8.0/pt_core_news_sm -DestinationPath work_dir/pt_core_news_sm.zip
mv -r work_dir/pt_core_news_sm.zip models/
rm -rf work_dir


echo "Passo 1: SAM Build..."
sam build --template cloud_formation_deploy.yml

echo "Passo 2: Deploy da infraestrutura..."
sam deploy \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 # Garante que o SAM use um bucket para artefatos

echo "Passo 3: Obtendo o nome do bucket de modelos criado pelo CloudFormation..."

MODEL_BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query "Stacks[0].Outputs[?OutputKey=='NomeDoBucketS3'].OutputValue" \
  --output text \
  --region "${REGION}")

if [ -z "${MODEL_BUCKET_NAME}" ]; then
  echo "ERRO: Não foi possível encontrar o nome do bucket de modelos no output da stack."
  exit 1
fi

echo "Bucket de modelos encontrado: ${MODEL_BUCKET_NAME}"

echo "Passo 4: Sincronizando arquivos de modelos grandes para o S3..."
aws s3 sync "${LOCAL_MODELS_PATH}" "s3://${MODEL_BUCKET_NAME}/" --region "${REGION}"

echo "Deploy e sincronização de modelos concluídos com sucesso!"