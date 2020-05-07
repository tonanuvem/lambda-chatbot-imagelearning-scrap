source venv/bin/activate
echo "Aparecerá um link para vc logar no site serverless.com e abrir a url fornecida:"
sls login
sls deploy
serverless invoke -f scrap --log
