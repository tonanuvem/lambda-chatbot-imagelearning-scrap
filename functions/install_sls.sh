#!/bin/bash
echo "Instalando as dependencias"
npm install -g serverless
serverless --version
chmod +x scrap/sls_config.sh
#CONFIGURAR
echo "Configurando as dependencias"
cd scrap
sls_config.sh
cd ..
#INSTALAR
echo "Deseja instalar (y/N)": 
read INSTALAR
if ($INSTALAR=="y");
then
  cd scrap
  sls_exec.sh
  cd ..
else
  echo "Escolhido não instalar"
fi
