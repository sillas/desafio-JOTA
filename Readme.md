# Expeprimento com o Spacy no Lambda

## Objetivo
Desenvolver um sistema de classificação automática de notícias usando o Spacy.

O sistema deve receber notícias via webhook, e classificar entre categorias e tags apropriadas.

Arquitetura:
O sistema é dividido em três partes independentes:
- 1. Webhook + classificação de notícias;
- 2. Sincronização;
- 3. Consulta das notícias classificadas.

## 1 - Webhook e classificação de notícias
O sistema de classificação é composto pe;a seguinte cadeia de serviços:
Usuário|Sistema -> API-Gateway [POST] -> Lambda (validação) -> SQS (Fila) -> Lambda de Classificação -> DynamoDB (Banco de dados).

Esse sistema é projetado para atender uma alta demanda de solicitações únicas, guardando as notícias classificadas no DynamoDB para uso posterior.
Optou-se por utilizar o CloudFormation da AWS para organizar a estrutura e realização do deploy.

### Particularidades:
Como o sistema de classificação depende de uma biblioteca e modelos de linguagem maiores do que o Lambda permite, e o uso do Docker não se justifica neste caso,
uma vez que funções lambdas em Docker possuem um desempenho mais baixo do que o equivalente direto, foi necessário uma adaptação da Biblioteca Spacy, removendo 
componentes não utilizados para que fique dentro do limite de tamanho do Lambda.

Já o modelo de linguagem utilizado pelo Spacy para realizar a "lemmatização" de tokens, está sendo enviado direto ao S3, e baixado para a pasta temporária do Lambda para uso. Esta estratégia permite, além de utilizar o Spacy (um módulo de boa qualidade) diretamente com o lambda, o que simplifica o desenvolvimento,
Também permite persistir o modelo dentro de uma mesma instância do Lambda em sucessivas chamadas (enquanto está "quente"), o que contribui para o desempenho final.

Por causa desta particularidade e pelo tamanho do modelo, tanto a camada quanto o modelo não podem ser enviados ao Github, e consequentemente, não podem usar o Github Actions para deploy. Sendo necessário o deploy direto da máquina do desenvolvedor, ou enviar previamente estas camadas e modelos de forma independente.

Isto é uma decisão inicial, e certamente, com um pouco mais de tempo e análise, uma solução melhor pode ser encontrada para este caso em particular,
inclusive usando o Docker, embora com um desempenho mais baixo.

### Observação

Embora se esteja utilizando tecnologia serverless neste caso, existe um limite de viabilidade para este formato.
Uma outra opção seria usar tecnologias mais tradicionais, com instâncias rodando debaixo de um "load balance", ou em um sistema de orquestração de containers.

No entanto, a escolha pela tecnologia depende primariamente da demanda esperada e da frequência das requisições.
Se houver uma alta demanda mas com uma frequência pontual ou imprevisível, usar o modelo atual é o ideal.
Se houver uma demanda baixa, ainda que com frequência constante, o modelo atual ainda é o ideal.

No entanto, se a demanda cresce muito, e a frequência se mantem relativamente constante e conhecida, e acima de 20 milhões de solicitações por mês,
Neste caso, compensa migrar de arquitetura, e usar uma mais tradicional.

De qualquer maneira, inicialmente, se não se sabe como será a demanda, usar serverles ainda é o ideal, mesmo que o valor final seja mais caro.
Pois pode-se medir a demanda real por um período de testes, já que irá escalar bem. Então, com os dados valiosos, pode-se estudar uma migração futura.

## 2 - Sincronização
Esta etapa se fez necessária para fazer a sincronização entre dois ambientes distintos: 
- O webhook com alta demanda, e a consulta interna de notícias com baixa demanda.

Embora entenda que é uma exigência para demonstrar capacidade e conhecimento com estas tecnologias, a decisão de usar o Django para
a consulta interna não é a melhor escolha.

Como a consulta interna é um sistema de baixa demanda, e já se está utilizando tecnologia serverless, a melhor estrategia seria continuar
usando serverless, pela disponibilidade, facilidade de manutenção, escalabilidade imediata e custo relativamente baixo.

Este sistema consiste de um lambda que aciona uma instância "Spot" regularmente, para transferir as notícias processadas do DynamoDB para
um banco relacional (mySQL ou PostgreSQL) que será usado pelo Django para consultas internas.

O Django será executado em uma instância EC2 mais simples, uma vez que desempenho não é importante neste caso de baixa demanda.

## 3. Consulta das notícias classificadas.

Este sistema é o que irá atender a demanda interna.
Ele consiste de uma isntância EC2 executando uma API com Django Rest e um banco de dados relacional como o MySQL ou o PostgreSQL.

# Detalhes do Projeto

Como apenas o ítem 3 do documento contem a diretiva: "Não use IA, queremos validar a Lógica",
deduzi que se está buscando uma solução que não envolva técnicas de IA ou mesmo serviços de IA de terceiros para classificação.

# Instruções para Deploy

Instruções para deploy:

1. - Criar o usuário IAM na AWS com permissões de administrador:
2. - Instalar o aws CLI localmente;
3. - Configurar as credenciais da AWS:
 `$ aws --version`
 `$ aws configure`
4. Verificar se o template está correto:
 `sam validate --template cloud_formation_deploy.yml --lint`
4. - Executar o script `deploy.sh`;
    `$ chmod +x deploy.sh`
    `$ ./deploy.sh`
5. - Entrar no console da AWS e consultar o serviço da API Gateway para obter a URL do webhook e a chave de API;
6. - Verificar se os modelos de linguagem estão armazenados no S3 (conforme o script de deploy).
7. - Para limpar tudo:
     - Por segurança, você deverá acessar o console da AWS, identificar o bucket que está sendo utilizado, e limpa-lo completamente.
       Apagando todos os itens que houver.
    - [instruções para remover a stack "classification-app" do cloudFormation aqui]
