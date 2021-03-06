#!/bin/bash
echo "Instalando as dependencias"
npm install -g serverless
serverless --version
chmod +x scrap/sls_config.sh
#CONFIGURAR
echo "Configurando as dependencias"
cd scrap
chmod +x sls_config.sh
./sls_config.sh
chmod +x sls_exec.sh
cd ..
# CONFIGURAR BUCKET e IAM
# CONFIGURAR IAM
echo "Criando Bucket chamado megahack"
aws s3api create-bucket --bucket megahack --region us-east-1 --create-bucket-configuration LocationConstraint=us-east-1
echo "Configurando as AWS IAM. Será preciso ajustar o arquivo serverless.yaml com ARN:"
aws iam create-role --role-name s3lambda --assume-role-policy-document file://s3lambda.json
echo "Após ajustar o ARN no arquivo serverless.yml de cada function, digite qualquer tecla para continuar."
read CONTINUAR
#INSTALAR
echo "Deseja instalar (y/N) : " 
read INSTALAR
if [ $INSTALAR == y ];
then
  cd scrap
  ./sls_exec.sh
  cd ..
else
  echo "Escolhido não instalar"
fi
