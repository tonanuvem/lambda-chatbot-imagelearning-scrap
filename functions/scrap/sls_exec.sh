source venv/bin/activate
echo "Aparecerá um link para vc logar no site serverless.com e abrir a url fornecida:"
sls login
sls deploy
serverless invoke -f scrap --log

echo "exemplo de chamada:"
echo "curl -H "Content-Type: application/json" -X POST https://20k55s857c.execute-api.us-east-1.amazonaws.com/prod \
echo "-d '{"url": "https://produto.mercadolivre.com.br/INSERIR_LINK"}'
# -d '{"url": "https://produto.mercadolivre.com.br/MLB-787170692-lego-minifigures-71012-disney-mr-incredible-sr-incrivel-_JM?quantity=1#reco_item_pos=8&reco_backend=promotions-sorted-by-score-mlb&reco_backend_type=low_level&reco_client=seller-promotions&reco_id=6321007d-0530-4607-9c59-75753ff3e1c5&deal_print_id=1d73c720-8fde-11ea-9c46-d3304499f6f0&model_version=release-2.0.1-bacalao&promotion_type=LIGHTNING_DEAL"}'
