# Escavador_Web_Scraping
Escavador Web Scraping

## Instalação e Configuração do Ambiente Linux

### Instalação do Python 3.x
```
sudo apt-get install python3
```

### Instalação do gerenciador de pacotes (pip)
```
sudo apt-get update
sudo apt-get install python3-pip
```
### Instalação Setuptools
```
sudo apt-get install python3-setuptools
```

### Instalação de binários necessários para o Peewee
```
sudo apt-get update
sudo apt-get install -y build-essential python3-dev libpq-dev
```

### Instalação do Gerenciador de Ambiente Virtual (virtualenv)
```
sudo apt-get install virtualenv
```

### Criação do Ambiente Virtual
```
virtualenv env
```
Obs.: É preciso abrir o terminal dentro da pasta do programa. <br>
Só é necessário executar esse comando se a pasta  env não existir dentro da pasta do programa.

### Ativação do Ambiente Virtual
```
source env/bin/activate
```
Obs.: É preciso abrir o terminal dentro da pasta do programa, mas fora da pasta env. <br>
O ambiente está ativado quando é apresentado `(env)`.

### Instalação dos pacotes necessários
```
pip3 install -r requirements.txt
```
Obs.: É preciso que o terminal esteja aberto na pasta do programa e o ambiente esteja ativado. <br>
