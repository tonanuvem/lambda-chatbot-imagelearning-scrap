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
#INSTALAR
echo "Deseja instalar (y/N)": 
read INSTALAR
if ("$INSTALAR"=="y");
then
  cd scrap
  ./sls_exec.sh
  cd ..
else
  echo "Escolhido não instalar"
fi
