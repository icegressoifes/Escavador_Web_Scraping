# coding: utf-8
'''
Realiza a conexao com o banco de dados.
Cria tabelas e apaga tabelas.
'''
import os
import psycopg2
from peewee import *
import logging
import logging.config
import traceback

logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Erro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."

class BaseModel(Model):
    '''
        Classe BaseModel estabelece a conexão com o banco de dados internamente na classe Meta.\n
        As outras classes serão todas subclasses BaseModel.
    '''    
    
    class Meta:
        '''
        Classe Meta define a conexão com o banco de dados.
        '''
        namedatabase, user, password, host, port = None, None, None, None, None
        try:
            # environment variable
            host = os.environ.get('HOST').strip()
            namedatabase = os.environ.get('DATABASE').strip()
            user = os.environ.get('USER').strip()
            password = os.environ.get('PASSWORD').strip()
            port = int(os.environ.get('PORT'))
            database = PostgresqlDatabase(namedatabase, user=user, password=password, host=host, port=port) 
            # database = MySQLDatabase(namedatabase, user=user, password=password, host=host, port=3306)
        except:
            print(msg_error.format("classe BaseModel", "não foi possível estabelecer conexão com o banco  de dados"))
            logger.error( traceback.format_exc() )

class Aluno(BaseModel):
    '''
    Classe Aluno (tabela) herda a conexão do banco de dados da Classe BaseModel.
    
    Atributos
    ---------
        id (int):
            chave primária.
        name (str):
            nome do aluno.
        sex (char):
            sexo do aluno, "F" ou "M".
        birth_date (date):
            data de nascimento.
        year_start (int): 
            data de inicio do curso.
        year_end (int):
            data de fim do curso.
    ''' 
    id = AutoField() 
    name = CharField() 
    sex = FixedCharField(constraints=[Check("sex = 'F' OR sex = 'M'")], null=True, max_length=1)
    birth_date  = DateField(null=True) 
    year_start = IntegerField(null=True) 
    year_end = IntegerField(constraints=[Check("year_end >= year_start")], null=True)
    class Meta:
        # restriction
        indexes = ((('name', 'birth_date'), True), ) # unique (name, birth_date)        
        
        
class Combinacao(BaseModel):
    '''
    Classe Combinacao (tabela) herda a conexão do banco de dados da classe BaseModel.    
    
    Atributos
    ---------
        id (int):
            chave primária.
        aluno_id (int):
            chave estrangeira da tabela aluno.
        name (str):
            combinação de nome do aluno.
        is_scrapered (boolean):
            True ou False indica a situação da coleta web para aquela combinação de nome.
        quantity_found (int):
            quantidade de páginas retornadas no resultado da busca.  
    '''
    id = AutoField()  # primary key
    aluno_id = ForeignKeyField(Aluno, field='aluno_id',to_field='id')
    name = CharField() 
    is_scrapered = BooleanField(default=False)
    quantity_found = IntegerField(null=True) 
    class Meta:
        # restriction
        indexes = ((('aluno_id', 'name'), True), ) # unique (aluno_id, name)


class Escavador(BaseModel):
    '''
    Classe Escavador (tabela) herda a conexão do banco de dados da classe BaseModel.  
        
    Atributos
    ---------
        id (int):
            chave primária.
        combinacao_id (int):
            chave estrangeira da tabela combinacao.            
        aluno_id (int):
            chave estrangeira da tabela aluno.
            obs.: O valor só deve ser atribuido para os registros que foram verificados como egresso.
        profile_name (str):
            nome da página de perfil.
        profile_url (str):
            endereço da página de perfil.
        date (date):
            data da realização da coleta web.
        profile_page (str):
            conteúdo da página web de perfil.
        profile_json (str):
            conteúdo no formato JSON dos dados processados e extraído da página web. 
    '''
    id = AutoField()
    combinacao_id = ForeignKeyField(Combinacao, field='combinacao_id',to_field='id')
    aluno_id = ForeignKeyField(Aluno, field='aluno_id',to_field='id',null=True)
    profile_name = CharField()
    profile_url = CharField()
    date = DateField()
    profile_page = TextField() 
    profile_json = TextField(null=True, default=True)
    

  
def f_create_tables(if_not_exists=False):
    '''
    Cria tabelas
    
    Parâmetro
    ----------
        if_not_exists (boolean):
            argumento do banco de dados verifica antes de criar.
    
    Retorno
    ----------
        concluded (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''    
    concluded = True
    try:
        Aluno.create_table(safe=if_not_exists)
        print("Tabela 'Aluno' criada!")
        Combinacao.create_table(safe=if_not_exists)
        print("Tabela 'Combinacao' criada!")
        Escavador.create_table(safe=if_not_exists)
        print("Tabela 'Escavador' criada!")
        concluded = False
    except:
        print(msg_error.format("função f_create_tables", "não foi possível criar as tabelas"))
        logger.error( traceback.format_exc() )
    return concluded 
 
   
def f_drop_tables(if_exists=False):
    '''
    Apaga tabelas
    
    Parâmetro
    ----------
        if_exists (boolean):
            argumento do banco de dados verifica antes de apagar.
    
    Retorno
    ----------
        concluded (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''    
    
    concluded = True    
    try:
        Escavador.drop_table(safe=if_exists, cascade=True)
        print("Tabela 'Escavador' apagada!")
        Combinacao.drop_table(safe=if_exists, cascade=True)
        print("Tabela 'Combinacao' apagada!")
        Aluno.drop_table(safe=if_exists, cascade=True)
        print("Tabela 'Aluno' apagada!")
        concluded = False        
    except Exception as e:
        print(msg_error.format("função f_drop_tables", "não foi possível apagar as tabelas"))
        logger.error( traceback.format_exc() )        
    return concluded     


if __name__ == '__main__':
	print("Classe Model")