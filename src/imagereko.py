# modulo

#@app.route('/image', methods=['POST'])
def imagem(request):
    num_media = int(events['NumMedia'])
    media = events.get('MediaContentType0', '')
    phone_number = events['From']
    if phone_number.startswith('whatsapp'):
        # from format: 'whatsapp:+490001112223'
        user_phone_number = phone_number.split(':+')[1]
        # mascaramento no numero
        user_phone_number = user_phone_number[:5]+'_'+user_phone_number[9:]

    resp = MessagingResponse()
    reply = "Qualquer dúvida estou aqui."

    if num_media > 0:
        if media.startswith('image/'):
            file_url = events['MediaUrl0']
            lista = file_url.split('/')
            id_message = lista[7]
            id_media = lista[9]
            print('lista = '+str(lista))
            print('id_message = '+id_message)
            print('id_media = '+id_media)

            print('media content type = '+media)
            extension = media.split('/')[1]
            file_name = file_url[file_url.rfind('/')+1:]
            file_path = f'{user_phone_number}/{file_name}.{extension}'
            print('fileurl  = '+file_url)
            print('filename = '+file_name)
            print('filepath = '+file_path)
            arquivo = 'img_resize/download_'+user_phone_number+file_name+'.'+extension

            try:
                enviar_statuszap("Salvando a imagem na nuvem. Só um minutinho.", phone_number)
                save_img_local(file_url, arquivo)
                status=upload_file(arquivo, bucket,file_path)
            except Exception as e:
                print('Erro ao salvar a imagem e enviar para nuvem')
                logging.error(e)
            
            if status:
                try:
                    enviar_statuszap("Analisando a imagem para enviar minhas sugestões. Um momento.", phone_number)
                    caracteristicas = detect_labels(file_path, bucket)
                    if len(caracteristicas) == 0:
                        caracteristicas.add('Não foi possível identificar')
                    enviar_statuszap("Categorias sugeridas: *" +str(caracteristicas)+'*', phone_number)
                    #cores = get_cor_proxima()
                except Exception as e:
                    print('Erro ao analisar a image : detect_labels')
                    logging.error(e)

                enviar_statuszap('Imagem salva e processada! Obrigado. *Link para acessar*: https://megahack.s3.amazonaws.com/'+user_phone_number+'/', phone_number)
                #salvar txt com as caracteristicas e cores

                try:
                    output_remoto = f'{user_phone_number}/{file_name}.'+'txt'
                    output_local = 'output_txt/'+file_name+'.txt'
                    print('arquivo txt caracteristicas: '+ output_local)
                    with open(output_local,'w', encoding='utf8') as outfile:
                        outfile.write(str(caracteristicas))
                        outfile.close()
                        status_json=upload_file(output_local, bucket,output_remoto)
                except Exception as e:
                    print('Erro ao gerar o arquivo json com as características')
                    logging.error(e)

                enviar_statuszap("Se houver Produto *semelhante no Mercado Livre, envie o link* que irei capturar as informações visando agilidade no preenchimento.", phone_number)
            else:
                reply = 'Erro ao salvar a imagem na nuvem. Informar ao suporte. ID = '+id_message #URL : '+file_url
        else:
            reply = 'Sorry, favor enviar somente imagens.'
    else:
        user_message = events['Body'].lower()
        if 'save' in user_message:
            reply = (
                f"Vamos começar! A partir de agora, salvarei as fotos que você enviar. \n"
                "Para ver fotos, envie-me uma mensagem com a palavra *see*"
                )
        #elif 'see' in user_message:
            #all_pics_url = files_folder_from(user_phone_number)
            #reply = f'Imagens salvas: {all_pics_url}'
    resp.message(reply)
    return str(resp)

def save_img_local(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: Local File to upload
    :param bucket: Bucket to upload to
    :param object_name: remote S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    print('S3: salvando o arquivo '+file_name)
    if object_name is None:
        object_name = file_name
    # Upload
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        #print(response)
    except Exception as e:
        print('\tErro ao salvar o arquivo no S3')
        logging.error(e)
        return False
    return True

def traduzir(texto):
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    result = translate.translate_text(Text=texto, 
                SourceLanguageCode="en", TargetLanguageCode="pt")
    return result.get('TranslatedText')

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')
    
    caracteristicas = set()

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    print('Detectar labels : ' + photo) 
    print('AWS reconheceu: '+ str(response['Labels']))   
    for label in response['Labels']:
        if (label['Confidence']) > 80:
            nome = traduzir(label['Name'])
            caracteristicas.add(nome)
            print ("Label: " + traduzir(label['Name']))
            print ("Confidence: " + str(label['Confidence']))
            # recortar e salvar com outro nome
            print ("Instances:")
            # onera muito o tempo. avaliar fazer em outro microserviço.
            #for instance in label['Instances']:
            #    save_cropped_image(photo, instance)
            # inserir tambem as caracteristicas mais gerais
            for parent in label['Parents']:
                nome_similar = traduzir(parent['Name'])
                print ("   " + nome_similar)
                caracteristicas.add(nome_similar)
            print ()
    return caracteristicas

def save_cropped_image(arquivo_local, instance, nome):
    # Imagem: width , height
    imagem = Image.open(open(arquivo_local,'rb'))
    width, height = imagem.size
    # Setting the points for cropped image 
    # https://docs.aws.amazon.com/rekognition/latest/dg/images-displaying-bounding-boxes.html
    left = instance['BoundingBox']['Left'] * width
    top = instance['BoundingBox']['Top'] * height
    right = left + (instance['BoundingBox']['Width'] * width)
    bottom = top + (instance['BoundingBox']['Height'] * height)
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    # https://www.geeksforgeeks.org/python-pil-image-crop-method/
    cropped = imagem.crop((left, top, right, bottom))
    # cropped = img.crop( ( Left*width, Top, Left + Width, Top + Height ) ) 
    arquivo_local_resize = 'img_resize/resize_'+nome
    cropped.save(arquivo_local_resize)
    return arquivo_local_resize

# https://stackoverflow.com/questions/27292145/python-boto-list-contents-of-specific-dir-in-bucket
def files_folder_from(phone_number):
    path = f'/{phone_number}'
    folder_url = None
    '''try:
        link = dbx.sharing_create_shared_link_with_settings(path)
        folder_url = link.url
    except dropbox.exceptions.ApiError as exception:
        if exception.error.is_shared_link_already_exists():
            link = dbx.sharing_get_shared_links(path)
            folder_url = link.links[0].url
    return folder_url'''
    #s3 = boto3.resource('s3')
    #my_bucket = s3.Bucket('my_bucket_name')
    #for object_summary in bucket.objects.filter(Prefix=path):
        #print(object_summary.key)
    # https://www.zabana.me/notes/flask-tutorial-upload-files-amazon-s3
    '''Get all buckets attached to your account
    buckets         = s3.list_buckets()
    List all objects (files) in a bucket
    # Both are valid
    objects         = s3.list_objects(Bucket=S3_BUCKET)
    objects         = s3.list_objects_v2(Bucket=S3_BUCKET)
    Access the files in a bucket
    all_files       = objects["Contents"]
    Get the total number of files in a bucket
    # If you used client.list_objects_v2
    number_of_files = objects["KeyCount"]
    # Else
    number_of_files = len(all_files)
    Extract all file names
    file_names      = [file["Key"] for file in objects["Contents"]]'''



def hash(photo):
    md5hash = hashlib.md5(Image.open(photo).tobytes())
    return str(md5hash.hexdigest())

# https://webcolors.readthedocs.io/en/1.11.1/contents.html#webcolors.HTML4_HEX_TO_NAMES
#chamada a ser colocada se for utilizar:
#colors, pixel_count = extcolors.extract("adesivo-para-geladeira-escovado-grafite-0-61m-adesivos-para-parede.jpg")
#print(colors)
#rgb = colors[0][0]
#print(rgb)
#nome_cor = get_cor_proxima(rgb)
#print(nome_cor)
#def get_cor_proxima(rgb_triplet, tipo_cores=2):
def get_cor_proxima(photo_local, tipo_cores=2):
    colors, pixel_count = extcolors.extract(photo_local)
    min_colours = {}
    if tipo_cores == 3:
        dic_tipo_cores = webcolors.HTML4_HEX_TO_NAMES.items()
    elif tipo_cores == 4:
        dic_tipo_cores = webcolors.CSS3_HEX_TO_NAMES.items()
    else:
        dic_tipo_cores = webcolors.CSS21_HEX_TO_NAMES.items()
    for key, name in dic_tipo_cores:
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        #rd = (r_c - rgb_triplet[0]) ** 2
        #gd = (g_c - rgb_triplet[1]) ** 2
        #bd = (b_c - rgb_triplet[2]) ** 2
        #min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

