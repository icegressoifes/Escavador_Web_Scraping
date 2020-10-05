# Escavador_Web_Scraping
Escavador Web Scraping

## <a name="prototipos"></a> Sumário
+ [2.2. Manual de uso do Sistema Windows](#2.2.)
+ [2.2.1. Criação do Ambiente Virtual](#2.2.1.)
+ [2.2.2. Ativação do Ambiente Virtual](#2.2.2.)
+ [2.2.3. Adiciona variável de ambiente do banco de dados](#2.2.3.)
+ [2.2.4. Execução do programa Web Scraping](#2.2.4.)
+ [2.2.4.1. Executando funcionalidade cria base](#2.2.4.1.)


## <a name="2.2."></a> 2.2. Manual de uso do Sistema Windows


### <a name="2.2.1."></a> 2.2.1. Criação do Ambiente Virtual

Digite o comando a seguir no Prompt de comando. O resultado esperado está na Figura 1.

```
virtualenv env
```

<figure>
	<img src="documentacao/image/cmd-cria-env.jpg" alt="Prompt de Comando cria env" width="600">
	<figcaption>Figura 1 - Prompt de Comando cria env</figcaption>
</figure>

Obs.: É preciso abrir o terminal dentro da pasta do programa. <br>
Só é necessário executar esse comando se a pasta  env não existir dentro da pasta do programa.

### <a name="2.2.2."></a> 2.2.2. Ativação do Ambiente Virtual
Digite o comando a seguir no Prompt de comando. O resultado esperado está na Figura 2.

```
env\Scripts\activate
```

<figure>
	<img src="documentacao/image/cmd-env-ativacao.jpg" alt="Prompt de Comando ativação env" width="600">
	<figcaption>Figura 2 - Prompt de Comando ativação env</figcaption>
</figure>

Obs.: É preciso abrir o terminal dentro da pasta do programa, mas fora da pasta env. <br>
O ambiente está ativado quando é apresentado `(env)`.

### <a name="2.2.3."></a> 2.2.3. Adiciona variável de ambiente do banco de dados

Digite o comando a seguir no Prompt de comando. O resultado esperado está na Figura 3.

```
set HOST=xxx
set DATABASE=xxx
set USER=xxx
set PASSWORD=xxx
set PORT=xxx
```

<figure>
	<img src="documentacao/image/cmd-variavel-env.jpg" alt="Prompt de Comando define variável ambiente" width="600">
	<figcaption>Figura 3 - Prompt de Comando define variável de ambiente</figcaption>
</figure>

Obs.: HOST, DATABASE, USER, PASSWORD e PORT são variáveis de ambiente para a conexão com o Banco de Dados. <br>
É preciso que o terminal esteja aberto na pasta do programa e o ambiente esteja ativado. 

### <a name="2.2.4."></a> 2.2.4. Execução do programa Web Scraping

Digite o comando a seguir no Prompt de comando para conhecer as funcionalidades do programa. O resultado esperado está na Figura 4, uma lista de argumentos que devem ser informados para ativar cada funcionalidade.

```
python main.py ajuda

```

```  
    ----------------------------------------------------------------------------
    Argumentos
    ----------------------------------------------------------------------------
    cria_base                         Cria banco de dados
    apaga_base                        Apaga banco de dados
    carrega_planilha                  Carrega os dados da planilha csv
    coleta_dados                      Inicia a coleta de dados dos egressos
    coleta_dados login                Abre navegador na página de login
    marca_dados                       Anexa rótulos nos dados coletados   
    marca_dados desfazer              Apaga rótulos nos dados coletados
    ajuda                             Mensagem de ajuda       
```
<figure>
	<img src="documentacao/image/cmd-execucao-main.jpg" alt="Prompt de Comando conhecendo as funcionalidades" width="600">
	<figcaption>Figura 4 - Prompt de Comando conhecendo a funcionalidades do programa</figcaption>
</figure>

Obs.: O programa só vai funcionar se: o ambiente virtual estiver ativo, os pacotes dependetes do programa forem instalados, e as variáveis de ambiente forem definidas para uma banco de dados existente.  

### <a name="2.2.4.1."></a> 2.2.4.1. Executando funcionalidade cria base


Digite o comando a seguir no Prompt de comando para criar as tabelas do banco de dados. O resultado esperado está na Figura 5, uma mensagem informando o sucesso na execução dessa funcionalidade.

```
python main.py cria_base

```

<figure>
	<img src="documentacao/image/programa-cria-base.jpg" alt="Funcionalidade cria base" width="600">
	<figcaption>Figura 5 - Funcionalidade cria base</figcaption>
</figure>



### <a name="2.2.4.2."></a> 2.2.4.2. Executando funcionalidade apaga base


Digite o comando a seguir no Prompt de comando para apagar as tabelas do banco de dados. O resultado esperado está na Figura 6, uma mensagem informando o sucesso na execução dessa funcionalidade.

```
python main.py apaga_base

```

<figure>
	<img src="documentacao/image/programa-apaga-base.jpg" alt="Funcionalidade apaga base" width="600">
	<figcaption>Figura 6 - Funcionalidade apaga base</figcaption>
</figure>


### <a name="2.2.4.2."></a> 2.2.4.2. Executando funcionalidade carrega planilha


Digite o comando a seguir no Prompt de comando para carregar a planilha CSV com os dados do aluno e salvar no banco de dados. Nesse funcionalidade espera-se que a planilha não tenha cabeçalho, pois o programa vai tentar armazenar a primeira linha da mesma. O resultado esperado está na Figura 7, uma janela esperando que o usuário selecione a planilha que será processada.
```
python main.py carrega_planilha

```

<figure>
	<img src="documentacao/image/programa-carrega-planilha.jpg" alt="Funcionalidade carrega planilha" width="600">
	<figcaption>Figura 7 - Funcionalidade carrega planilha </figcaption>
</figure>


A Figura 8 apresenta a mensagem de sucesso após a realização do processamento, isto é, após os dados serem salvos no banco de dados.


<figure>
	<img src="documentacao/image/programa-carrega-planilha2.jpg" alt="Funcionalidade carrega planilha" width="600">
	<figcaption>Figura 8 - Funcionalidade carrega planilha </figcaption>
</figure>

Um exemplo de planilha que o programa espera é apresentado na Figura 9, ela tem a coluna Matrícula, Nome de Aluno, Data de Nascimento, Nome do curso, Ano de Início, Período de Início, Ano de fim, Período de fim e o Sexo do aluno. Obs.: Espera-se que a planilha tenha codificação UTF e o delimitador seja uma virgula.

<figure>
	<img src="documentacao/image/programa-carrega-planilha4.jpg" alt="Funcionalidade carrega planilha" width="600">
	<figcaption>Figura 9 - Funcionalidade carrega planilha </figcaption>
</figure>