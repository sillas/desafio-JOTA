#!/bin/bash
set -e # Encerra o script se houver erro

# --- Configuração ---
STACK_NAME="jota-app"
REGION="us-east-1"
LOCAL_MODELS_PATH="models/"

echo "Passo 1: SAM Build..."
sam build

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