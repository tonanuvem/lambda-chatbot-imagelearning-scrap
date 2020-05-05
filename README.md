# OLY: Assistente Virtual imersivo

[Demonstração do assistente virtual](http://bit.ly/eq28olist)

[Vídeo do pitch](https://www.youtube.com/watch?v=-5I-7OoBm6Y)

[Github Mobile App](https://github.com/patrickbattisti/olist-augmented-reality) 


## **Topologia da solução:**

![Alt Text](Megahack.jpg)

A solução utiliza as melhores práticas de divisão de responsabilidades em microserviços.

O backend foi construído em arquitetura REST e executado por funções Lambdas.

O Mobile App para Realidade Aumentada foi desenvolvido em react native por outro integrante da equipe.

---

## **Tecnologias e Stacks utilizadas:**

`Twilio: integração com o WhatsApp para receber solicitações e posterior resposta.`

`Sumerian: criação da interface 3D do assistente virtual.`

`Dialogflow: motor do chatbot utilizado para respostas de dúvidas.`

`Python Backend serverless: funções responsáveis pelas funcionalidades da solução.`

---

## **Microserviços da solução **

>`Reconhecimento de imagens:`

```Descrição: O microserviço de reconhecimento de imagens possibilita que além de identificar os componentes da imagem, seja possivel sugerir as categorias e também recortar na foto somente o elemento que esteja sendo vendido.
```

>`Scrap:`

```Descrição: Após o usuário informar o link de um produto parecido, o assistente irá analisar a página e obter os diversos campos do produto, além da lista de perguntas. Essas informações terão 2 objetidos:
Campos do produto podem ser utilizados pelo vendedor para ajustar algo específico sem precisar digitar tudo do zero.
Lista de perguntas poderá ser utilizada para treinamento automático do Chatbot.
```

>`Chatbot:`

```Descrição: A criação do ChatBot foi feita para identificar trechos das frases relacionadas a "entidade produto" e a "entidade duvida". Após essa identificação, conseguiremos ter recebido uma entrada com dados não estruturados e teremos identificado os componentes de maneira estruturada para possibilitar a pesquisa no Banco de Dados. Um dos principais desafios da construção de robôs que utilizam NPU (Natural Language Understanding) é o treinamento do modelo com diversos exemplos para que o mecanismo de ML (machine learning) utilizado pelo motor do Chatbot consiga ter exemplos significativos de cada "entidade". 
```

>`Treinamento automatizado do Chatbot:`

```Descrição: Com base nas perguntas que o microserviço Scrap tiver coletado, poderá ser disparado o treinamento automático do motor do Chatbot. Esse é um dos principais desafios, pois o Dialogflow não possui em sua API uma chamada simples de treinamento onde pudesse ser definido a frase de treinamento para ser incorporada ao que já existe. Esse ponto ainda está em desenvolvimento.
```

>`Comunicação do Assistente em diversos canais: Whatsapp, Facebook, Twitter`

```Descrição: A ferramenta utilizada como Dialogflow permite que o Chatbot seja utilizado em diversos canais. Dessa forma, o cadastro de produtos por um Vendedor poderia ocorrer também por Facebook, por exemplo. Da mesma forma, dúvidas de compradores poderiam ser recebidas por outros canais, Twitter por exemplo.
```

>`Armazenamento das imagens:`

```Descrição: Esse componente da solução é responsável por armazenar no Bucket as imagens recebidas durante o processo de reconhecimento de imagens.
```

---
### **Demonstrativo da aplicação Chatbot:**

[Demonstração do módulo Chatbot utilizado pelo OLY](https://bot.dialogflow.com/tonanuvem)

![Alt Text](chatbot-motor.png)

---

### ** Repositorio do projeto 3D:**

[Projeto assistente-3d](https://github.com/tonanuvem/assistente-3d)

![Alt Text](assistente-3d/tela-projeto-3d.png)

---
