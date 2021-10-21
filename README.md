codepay project
===============

Antecipation System Payment(Sistema de Antecipação de Pagamento)

Este sistema foi criado para realizar o cadastrado de boletos e fornecedores para possibilitar a implantação de um plano
de pagamento de forma adiantada quando solicitado pelo fornecedor gerando um melhor fluxo de caixa para o mesmo e rentabilizando o
caixa da empresa com um desconto no valor baseado na quantidade de dias restantes para o vencimento da fatura.

```
NOVO_VALOR = VALOR_ORIGINAL - (VALOR_ORIGINAL * ((3% / 30) * DIFERENCA_DE_DIAS))
```


Setup do servidor de produção
-----------------------------

### Criando os usuários

```
adduser deployment sudo
```

### Docker

```
sudo apt-get update

# https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-16-04-pt
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
sudo apt-get update
sudo apt-get install -y docker-engine
sudo groupadd docker
sudo usermod -aG docker $USER
```

### Python 3

```
sudo apt-get install -y git python-pip make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev libffi-dev

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod 0777 /usr/local/bin/docker-compose

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc

exec "$SHELL"

git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

exec "$SHELL"

pyenv install 3.7.1 -v
pyenv virtualenv 3.7.1 codepay project 


```

### Projeto

[__Antes de
tudo__: crie e insira no github uma chave de deployment)](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#generating-a-new-ssh-key)

```
cd
git clone git@github.com:LeonardoCDP/Codepay.git git
```

Copie e configure o `.env` do projeto

```
mkdir pgdata
cp env-sample .env

echo "CURRENT_UID=$(id -u):$(id -g)" >> .env
```

Setup no Heroku
---------------

```bash
heroku login
heroku create codepay_project-production

heroku config:set SECRET_KEY='---mY-SEcReT---'
heroku config:set DEBUG=false
heroku config:set ALLOWED_HOSTS=*
heroku config:set DATABASE_URL=postgres://codepay_project:codepay_project@localhost:5432/codepay_project
heroku config:set EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
heroku config:set AWS_ACCESS_KEY_ID=my-aws-key
heroku config:set AWS_SECRET_ACCESS_KEY=my-secret
heroku config:set AWS_STORAGE_BUCKET_NAME=codepay_project-static
heroku config:set DISABLE_COLLECTSTATIC=1

```

How to develop
--------------

### How to run local dependencies

- Install `docker` and `docker-compose`
- Run `make docker-compose-dev` to up containers with `postgres` and `redis`
- Run `make dev` to run development server

### How to run tests

- Install the tests dependencies with `pip install -r requirements-test.txt`
- Run tests with `make test`

### Tips

- Before commit run `make autopep8` to organize all your code

Documentação API
----------------

### Acesso a API

- A API possui a autenticação via JWT - Token do tipo = Bearer

### Links da API

- **api/rpa/** - Tipo de Acesso GET - Retorna um lista com todos os pagamentos.
- **api/rpa/<str:status>** - Tipo de Acesso GET - Enviando um filtro de status - retorna uma lista.
- **api/rpa/<str:pk>** - Tipo de Acesso GET PUT - Enviando o ID realizada a solicitação de antecipação - retorna o ID.
- **api/token/** - Tipo de Acesso POST - Enviando usuario e senha - retorna um Token Refresh com validade de 1 dia e um
  Access Token com validade de 5 mimutos.
- **api/token/refresh/** - Tipo de Acesso POST - Enviando o Refresh Token - retorna um novo Access token. 
