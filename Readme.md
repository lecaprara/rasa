# Rasa Chatbot Project

Este projeto utiliza [Rasa Open Source](https://rasa.com/) para construir um chatbot personalizável. O projeto está estruturado com containers Docker para facilitar o desenvolvimento e a execução. Este documento explica a estrutura do projeto, como configurá-lo e como começar a usar e personalizar o chatbot.

---

## Estrutura do Projeto

### Arquivos e Pastas Principais

#### 1. **actions/**
Contém o código para ações personalizadas que o chatbot pode executar.  
- **`actions.py`**: Arquivo principal onde as ações são implementadas. Cada classe neste arquivo define uma ação que pode ser chamada pelo Rasa.  
- **`Dockerfile`**: Configuração do Docker para o servidor de ações. Ele instala dependências do Python e executa o servidor.  
- **`requirements.txt`**: Dependências de Python necessárias para as ações personalizadas.

#### 2. **data/**
Contém os dados de treinamento do chatbot.  
- **`nlu.yml`**: Contém exemplos de entrada do usuário classificados por intents.  
- **`stories.yml`**: Define histórias que descrevem os fluxos de conversa.  
- **`rules.yml`**: Define regras para comportamentos específicos, como acionamento de respostas.

#### 3. **models/**
Pasta onde os modelos treinados do Rasa são salvos. Esses modelos contêm todas as configurações e dados necessários para o chatbot funcionar.

#### 4. **config.yml**
Configurações de pipeline para processamento de linguagem natural (NLU) e políticas de diálogo (Core). É aqui que você define as etapas para processar mensagens e prever respostas.

#### 5. **domain.yml**
Define a "memória" do chatbot. Inclui intents, entidades, slots, ações e respostas que o bot pode usar durante as conversas.

#### 6. **endpoints.yml**
Configura os endpoints externos, como o servidor de ações ou APIs.  
- **`action_endpoint`**: URL do servidor de ações, que é essencial para executar ações personalizadas.

#### 7. **docker-compose.yml**
Define a configuração dos containers Docker. Este arquivo facilita a execução do chatbot e do servidor de ações com comandos simples.

#### 8. **.gitignore**
Lista de arquivos e pastas a serem ignorados no repositório Git, como arquivos de configuração local, modelos treinados e outras pastas geradas dinamicamente.

---

## Como Configurar e Rodar o Projeto

### 1. Construir e Iniciar os Containers
Use o `docker-compose` para configurar e rodar o projeto:

```bash
docker-compose up --build
```
- Este comando inicializa dois serviços:
    - Rasa Core (rasa): O backend principal do chatbot.
    - Servidor de Ações (action-server): Onde as ações personalizadas são processadas

---

### 2. Treinar o modelo
Dentro do container do Rasa, execute o comando:

```
docker exec -it <nome-do-container-rasa> rasa train
```
Este comando usa os dados em `data/` e as configurações em `config.yml` para treinar o modelo e gera arquivos na em `models` com os arquivos `*.tar.gz` que é o resultado do treinamento do modelo.

---

### 3. Testar o Chatbot
#### 3.1 Rodar o Shell do Rasa
Para testar interativamente:

Entre no container com o comando abaixo:

```
docker exec -it <nome-do-container-rasa> /bin/bash
```
Execute o `rasa shell`:
```
rasa shell --port 5006
```

Estamos usando a porta 5006 já que a 5005 está sendo usada no Rasa Core.

#### 3.2 Rodar o Shell do Rasa em modo debug:
Para ver logs detalhados enquanto interage com o bot:
```
rasa shell --port 5006 --debug
```

---

### 3. Adicionar Novas Histórias
Para criar histórias de treinamento:

1. Edite o arquivo data/stories.yml.
2. Adicione uma nova sequência de interação, como:

```
stories:
- story: Conversa com saudação
  steps:
  - intent: greet
  - action: utter_greet
  - intent: ask_question
  - action: action_do_something
```

3. Treine novamente o modelo.


---

### Estrutura dos Serviços Docker
#### Serviço Rasa (rasa)
- Responsável por gerenciar o modelo do chatbot.
- Configurado para rodar no modo API com suporte a CORS para integração com frontends.
- Porta: 5005
#### Serviço Action Server (action-server)
- Gerencia ações personalizadas definidas no actions.py.
- Porta: 5055

---

### Personalização
- **Adicionar Intents**: Edite nlu.yml e adicione exemplos de entrada.
- **Adicionar Respostas**: Atualize domain.yml para incluir novas respostas.
- **Criar Ações Personalizadas**: Adicione novas classes em `actions/actions.py`.