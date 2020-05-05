# modulo

def scrape(url, phone_number):
    if not url.startswith('https://produto.mercadolivre.com.br'):
         retorno = 'Ainda não sei analisar muitos marketplaces. O link a ser analisado deve iniciar com: *https://* seguido por *produto.mercadolivre.com.br*'
         return enviar_statuszap(retorno, phone_number)

    e = Extractor.from_yaml_file('oly_scrap_selectors_ml.yml')
    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # Download the page using requests
    print("Scrap: Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "Possivel bloqueio do scrap" in r.text:
            print("Pagina %s bloqueada. Usar outros proxies\n"%url)
        else:
            print("Pagina %s bloqueada com status code : %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    data = e.extract(r.text)
    print(print_data_json(data))
    # se der erro, tentar o outro template de pagina que o mercado livre usa:
    if not data.get('nome'):
        e = Extractor.from_yaml_file('oly_scrap_selectors_2.yml')
        data = e.extract(r.text)
        print(print_data_json(data))
    
    if phone_number.startswith('whatsapp'):
        # from format: 'whatsapp:+490001112223'
        user_phone_number = phone_number.split(':+')[1]
        # mascaramento no numero
        user_phone_number = user_phone_number[:5]+'_'+user_phone_number[9:]
    #json_string = json.dumps(data, ensure_ascii=False, indent=4).encode('utf8')
    # , indent=4
    enviar_statuszap('Análise realizada: '+print_data_json(data), phone_number)
    # salvar arquivo no S3

    if data:
        try:
            file_name = 'file_name' # TODO: ajustar essa variavel
            output_remoto = f'{user_phone_number}/{file_name}.'+'json'
            output_local = 'output_txt/'+file_name+'.json'
            print('arquivo json do scrap: '+ output_local)
            with open(output_local,'w', encoding='utf8') as outfile:
                json.dump(data,outfile,ensure_ascii=False,indent=4)#, sort_keys=True)
                outfile.write("\n")
                outfile.close()
                status_json=upload_file(output_local, bucket,output_remoto)
        except Exception as e:
            print('Erro ao gerar o arquivo da análise')
            logging.error(e)

def print_data_json(data_completo):
    # excluir só na hora de imprimir. ao salvar tem que aparecer.
    data = dict(data_completo)
    del data['perguntas']
    json_string = json.dumps(data, ensure_ascii=False, indent=4).encode('utf8')
    return json_string.decode()