# Rasa Chatbot Project

Este projeto utiliza o [Rasa Open Source](https://rasa.com/) para criar um chatbot personalizável e integrado com um servidor de ações customizadas. Toda a infraestrutura foi criada para ser executada em containers Docker e gerenciada por Kubernetes, permitindo escalabilidade e facilidade de implantação.

---

## Estrutura do Projeto

### Arquivos e Pastas Principais

#### 1. **actions/**

Contém o código para ações personalizadas que o chatbot pode executar.

- **`actions.py`**: Arquivo principal onde as ações são implementadas. Cada classe neste arquivo define uma ação personalizadas que o chatbot pode executar.
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

Define a configuração dos containers Docker. Este arquivo facilita a execução do chatbot e do servidor de ações com comandos simples. (Devido o projeto ter mudado para Kubernetes, esse arquivo só será utilizado caso seja necessário rodar algum teste local sem a utilização do Kubernetes)

#### **8. k8s/**

Arquivos de configuração para Kubernetes:

- **`actions-deployment.yml`**: Configuração do deployment para o servidor de ações, que gerencia ações personalizadas definidas no arquivo `actions.py`.
- **`ingress.yml`**: Configuração do Ingress para expor o serviço do Rasa externamente, facilitando a integração com outros sistemas.
- **`kind-cluster-config.yml`**: Configuração usada para criar um cluster local com o Kind (Kubernetes in Docker), permitindo o gerenciamento e a execução dos containers Rasa e ações.
- **`rasa-deployment.yml`**: Configuração do deployment para o Rasa Core, que gerencia o modelo do chatbot.
- **`rasa-namespace.yml`**: Cria o namespace `rasa-namespace` para isolar os recursos do projeto dentro do cluster Kubernetes.
- **`rasa-service-local.yml`**: Configuração do serviço do Rasa utilizando o tipo **NodePort**, utilizado para testes locais e acessos internos ao cluster Kubernetes.
- **`rasa-service-prod.yml`**: Configuração do serviço do Rasa utilizando o tipo **LoadBalancer**, usado para expor o Rasa em ambientes de produção. (Provavelmente, esse será o arquivo a ser usado quando forem colocar o Rasa em produção em algum serviço de hospedagem)

#### 9. **.gitignore**

Lista de arquivos e pastas a serem ignorados no repositório Git, como arquivos de configuração local, modelos treinados e outras pastas geradas dinamicamente.

---

## Como Configurar e Rodar o Projeto

### 1. Executar com Kubernetes

#### Configurar o Cluster

1. Certifique-se de que **Kind** e **kubectl** estão instalados.
2. Crie o cluster Kubernetes com Kind:
   ```bash
   kind create cluster --config k8s/kind-cluster-config.yml
   ```
3. Aplique os manifests:
   ```bash
   kubectl apply -f k8s/rasa-namespace.yml
   kubectl apply -f k8s/rasa-deployment.yml
   kubectl apply -f k8s/rasa-service-local.yml
   kubectl apply -f k8s/actions-deployment.yml
   kubectl apply -f k8s/actions-service.yml
   ```

#### Verificar os Pods e Serviços

Verifique se os pods estão rodando:

```bash
kubectl get pods -n rasa-namespace
```

#### Obs.: É com esse comando que vemos os nomes dos pods que serão usados para testes e logs

Liste os serviços para confirmar o NodePort:

```bash
kubectl get svc -n rasa-namespace
```

### 2. Acessar o Rasa

Use o NodePort configurado (ex.: `30005`) e o IP do nó para acessar o chatbot:

```bash
curl -X POST http://<NODE-IP>:30005/webhooks/rest/webhook -H "Content-Type: application/json" -d '{"sender": "user", "message": "Hello"}'
```

### 3. Treinar o Modelo

Dentro do pod do Rasa, execute:

```bash
kubectl exec -it <rasa-pod-name> -n rasa-namespace -- rasa train
```

### 4. Debug e Logs

- Logs do Rasa:
  ```bash
  kubectl logs <rasa-pod-name> -n rasa-namespace
  ```
- Logs do servidor de ações:
  ```bash
  kubectl logs <actions-pod-name> -n rasa-namespace
  ```

---

## Personalização

### Adicionar Novos Intents

1. Edite `data/nlu.yml` e adicione exemplos.
2. Atualize `domain.yml` para incluir intents e respostas.
3. Treine o modelo novamente.

### Criar Novas Ações

1. Adicione novas classes no `actions.py`.
2. Atualize `domain.yml` para incluir as novas ações.
3. Reinicie o servidor de ações.

### Adicionar Novas Histórias

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

## Solução de Problemas

- **O serviço não responde:**  
  Verifique se os pods e serviços estão ativos:

  ```bash
  kubectl get pods -n rasa-namespace
  kubectl get svc -n rasa-namespace
  ```

- **Porta NodePort não acessível:**  
  Certifique-se de que o firewall permite acesso à porta.

---
