1 - Como apenas o ítem 3 da proposta de desafio contem a diretiva: (Não use IA, queremos validar a Lógica),
deduzi que se está buscando uma solução que não envolva técnicas de IA ou mesmo serviços de IA de terceiros.

Instruções para deploy:

1 - Criar o usuário IAM na AWS com as seguintes permissões:
 - ...

2 - Instale o aws CLI;

3 - Adicionar as credenciais da AWS:
 - AWS_ACCESS_KEY_ID
 - AWS_SECRET_ACCESS_KEY
 - AWS_REGION

4 - Criar a branch "main-deploy" e fazer o push (se ainda não existir);

5 - Testar o projeto.

6 - delete project: stack-name: jota-app

sam deploy --guided


7 - Para limpar tudo:
1 - Por segurança, você deverá acessar o console da AWS, identificar o bucket que está sendo utilizado, e limpa-lo completamente.
Apagando todos os itens que houver.

2 - Depois, execute o script [] para apagar todos os outros serviços (incluindo este bucket).

Comandos SAM:
aws --version
aws configure

sam validate --template workshop/deploy.yml --lint
sam build --template workshop/deploy.yml

sam deploy
sam deploy --guided
aws cloudformation describe-stacks --stack-name name