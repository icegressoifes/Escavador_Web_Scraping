from persistent_storage.model import Aluno
from persistent_storage.model import Combinacao
from persistent_storage.model import Linkedin


def f_save_aluno(name=None, sex=None, birth_date=None, year_start=None, year_end=None):
    '''
    Salva os dados do aluno na tabela Aluno.\n
    Os argumentos enviados como None (não preenchidos) serão armazenados como "null".
    
    Parâmetro
    ----------
        name (str):
            nome do aluno.
        sex (str):
            sexo do aluno, "F" ou "M".
        birth_date (str):
            texto representado a data de nascimento do aluno no formato "AAAA-MM-DD".
        year_start (int):
            ano de início do curso na instituição. 
        year_end (int):
            ano de fim do curso na instituição.
            
    Retorno
    ----------
        (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''  

    try:
        alunos =  f_get_aluno(name=name, birth_date=birth_date)
        if ( len(alunos) == 0):
            return Aluno.create(name= name, birth_date= birth_date, sex= sex, year_start= year_start, year_end= year_end )
        return False
    except Exception as e:
        print(e)
        return False



def f_get_aluno(id=None, name=None, birth_date=None):
    '''
    Retorna os dados dos registros encontrados na tabela Aluno de acordo com os argumentos informados.\n
    Os argumentos enviados como None não serão considerados na consulta.\n
    Ainda, se nenhum argumento for informado retorna todos os registros da tabela.
    
    Parâmetro
    ----------
        id (int):
            identificador do registro
        name (str):
            nome do aluno.
        birth_date (str):
            texto representado a data de nascimento do aluno no formato AAAA-MM-DD.
            
    Retorno
    ----------
        list_aluno (list): 
            Lista com os registros dos alunos encontrados.
    '''  
       
    list_aluno = []
    try:
        aluno_result = None
        if name!=None and birth_date!=None:
            '''
                Busca com filtro por nome e data de nascimento informada.
            '''
            aluno_result = Aluno.select().where( (Aluno.name == name) & (Aluno.birth_date == birth_date) ).order_by( Aluno.id )            
        elif id != None:
            '''
                Busca com filtro por id informado.
            '''
            aluno_result =  Aluno.select().where( Aluno.id == id )
        elif name != None:
            '''
                Busca com filtro por nome informado.
            '''            
            aluno_result = Aluno.select().where( Aluno.name == name ).order_by( Aluno.id )
        elif birth_date !=  None:
            '''
                Busca com filtro por data de nascimento informada.
            '''               
            aluno_result = Aluno.select().where( Aluno.birth_date == birth_date).order_by( Aluno.id )
        else:
            '''
                Busca sem filtro.
            '''                   
            aluno_result = Aluno.select().order_by( Aluno.id )
        for row in aluno_result.dicts():
            list_aluno.append(row)
        return list_aluno
    except Exception as e:
        print(e)
        return list_aluno
 
 

def f_update_aluno(id=None, name=None, birth_date=None):
    '''
    Atualiza os dados do registro do aluno na tabela Aluno de acordo com o id informado.\n
    Os argumentos enviados como None (não preenchidos) serão armazenados como "null".
   
    
    Parâmetro
    ----------
        id (int):
            identificador do registro
        name (str):
            nome do aluno.
        birth_date (str):
            texto representado a data de nascimento do aluno no formato AAAA-MM-DD.
            
    Retorno
    ----------
        (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''  
    
    try:
        if id!=None and name!=None:
            query = Aluno.update(name= name, birth_date= birth_date).where(Aluno.id == id)
            query.execute()
            return True
        raise Exception ('O valor de id ou name não informado!')
    except Exception as e:
        print(e)
        return False
    
        

def f_save_combinacao(aluno_id=None, name=None, is_scrapered=False, quantity_found=None):
    '''
    Salva os dados da combinação de nome do aluno na tabela Combinacao.\n
    Os argumentos enviados como None (não preenchidos) serão armazenados como "null".
    
    Parâmetro
    ----------
        aluno_id (int):
            O id do registro do aluno a qual a combinação de nome pertence.
        name (str):
            uma combinação de nome do aluno.
        is_scrapered (boolean):
            True ou False indica a situação da coleta web para aquela combinação de nome.
        quantity_found (int):
            quantidade de páginas retornadas no resultado da busca.

    Retorno
    ----------
        (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''  

    try:
        combinacoes =  f_get_combinacao(aluno_id=aluno_id, name=name)
        if ( len(combinacoes) == 0):
            return Combinacao.create(aluno_id=aluno_id, name=name, is_scrapered=is_scrapered, quantity_found=quantity_found)
        return False
    except Exception as e:
        print(e)
        return False




def f_get_combinacao(id=None, aluno_id=None, name=None, is_scrapered=None, id_limit_range=[0,0]):
    '''
    Retorna os dados dos registros encontrados na tabela Combinacao de acordo com os argumentos informados.\n
    Os argumentos enviados como None não serão considerados na consulta.\n
    Ainda, se nenhum argumento for informado retorna todos os registros da tabela.
    
    Parâmetro
    ----------
        id (int):
            identificador do registro            
        aluno_id (int):
            O id do registro do aluno a qual a combinação de nome pertence.
        name (str):
            uma combinação de nome do aluno.
        is_scrapered (boolean):
            True ou False indica a situação da coleta web para aquela combinação de nome.
        id_limit_range (list):
            Intervalo do IDs dos registros que serão considerados, índice 0 deve receber o valor do ID mínimo e índice 1 deve receber o valor do índice máximo.

            
    Retorno
    ----------
        list_combinacao (list): 
            Lista com os registros de combinacao encontrados.
    '''    
    list_combinacao = []
    try:
        combinacao_result = None
        if aluno_id!=None and is_scrapered!=None:
            '''
                Busca com filtro por id do aluno e situação de web scraping.
            '''
            combinacao_result = Combinacao.select().where( (Combinacao.aluno_id == aluno_id) & (Combinacao.is_scrapered == is_scrapered) ).order_by( Combinacao.id )
        elif aluno_id!=None and name!=None:
            '''
                Busca com filtro por id do aluno e nome da combinação.
            '''            
            combinacao_result = Combinacao.select().where( (Combinacao.aluno_id == aluno_id) & (Combinacao.name == name) ).order_by( Combinacao.id )            
        elif id!=None:
            '''
                Busca com filtro por id da combinação.
            '''            
            combinacao_result =  Combinacao.select().where( Combinacao.id == id )
        elif name!=None:
            '''
                Busca com filtro por nome da combinação.
            '''               
            combinacao_result = Combinacao.select().where( Combinacao.name == name ).order_by( Combinacao.id )
        elif aluno_id!=None:
            if id_limit_range != [0,0]:
                '''
                    Busca com filtro por id do aluno e intervalo de id combinacao.
                '''     
                combinacao_result = Combinacao.select().where( (Combinacao.aluno_id == aluno_id) & (Combinacao.id >= id_limit_range[0]) & (Combinacao.id <= id_limit_range[1]) ).order_by( Combinacao.id )        
            else:
                '''
                    Busca com filtro por id do aluno.
                '''     
                combinacao_result = Combinacao.select().where( Combinacao.aluno_id == aluno_id ).order_by( Combinacao.id )
        elif is_scrapered!=None:
            if id_limit_range != [0,0]:
                '''
                    Busca com filtro por situação do web scraping e intervalo de id combinacao.
                '''                    
                combinacao_result = Combinacao.select().where( (Combinacao.is_scrapered == is_scrapered ) & (Combinacao.id >= id_limit_range[0]) & (Combinacao.id <= id_limit_range[1]) ).order_by( Combinacao.id )
            else:
                '''
                    Busca com filtro por situação do web scraping.
                '''                   
                combinacao_result = Combinacao.select().where( Combinacao.is_scrapered == is_scrapered ).order_by( Combinacao.id )
        else:
            if id_limit_range != [0,0]:
                '''
                    Busca com filtro por intervalo de id combinacao.
                '''                  
                combinacao_result = Combinacao.select().where( (Combinacao.id >= id_limit_range[0]) & (Combinacao.id <= id_limit_range[1]) ).order_by( Combinacao.id )    
            else:    
                combinacao_result = Combinacao.select().order_by( Combinacao.id )
        list_combinacao = []
        for row  in combinacao_result.dicts():
            list_combinacao.append(row)
        return list_combinacao
    except Exception as e:
        print(e)
        return list_combinacao  



def f_update_combinacao(id=None, aluno_id=None, name=None, is_scrapered=False, quantity_found=None):
    '''
    Atualiza os dados do registro da combinacao na tabela Combinacao de acordo com o id informado.\n
    Os argumentos enviados como None (não preenchidos) serão armazenados como "null".
   
    
    Parâmetro
    ----------
        id (int):
            identificador do registro
        name (str):
            nome do aluno.
        birth_date (str):
            texto representado a data de nascimento do aluno no formato AAAA-MM-DD.
            
    Retorno
    ----------
        (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''      
    
    try:
        if id!=None and aluno_id!=None and name!=None and is_scrapered in [False, True]:
            query = Combinacao.update(aluno_id= aluno_id, name= name, is_scrapered= is_scrapered, quantity_found=quantity_found).where(Combinacao.id == id)
            query.execute()
            return True
        raise Exception ('O valor de  id, aluno_id, name ou is_scrapered não foi informado!')
    except Exception as e:
        print(e)
        return False




def f_save_linkedin(combinacao_id=None, aluno_id=None, profile_name=None, profile_url=None, date=None, profile_page=None, profile_json=None):
    '''
    Salva os dados de web scraping na tabela Linkedin.\n
    Os argumentos enviados como None (não preenchidos) serão armazenados como "null".
    
    Parâmetro
    ----------
        combinacao_id (int):
            O id do registro da combinacao a qual a página do LinkedIn está relacionada.        
        aluno_id (int):
            O id do registro do aluno a qual a página do LinkedIn pertence.
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
            
            
    Retorno
    ----------
        (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''      
    
    try:
        perfis = f_get_linkedin(profile_url= profile_url)
        if ( len(perfis) == 0):
            linkedin =  Linkedin.create(combinacao_id= combinacao_id, aluno_id= aluno_id, profile_name= profile_name,  profile_url= profile_url, date= date, profile_page= profile_page, profile_json= profile_json )
            return linkedin
        return False
    except Exception as e:
        print(e)
        return False
    
    



def f_get_linkedin(id=None, profile_url=None, date=None, profile_json=""):
    '''
    Retorna os dados dos registros encontrados na tabela Linkedin de acordo com os argumentos informados.\n
    Os argumentos enviados como None não serão considerados na consulta.\n
    Ainda, se nenhum argumento for informado retorna todos os registros da tabela.
    
    Parâmetro
    ----------
        id (int):
            identificador do registro        
        profile_url (str):
            endereço da página de perfil.
        date (date):
            data da realização da coleta web.
        profile_json (str):
            conteúdo no formato JSON dos dados processados e extraído da página web.
                        
    Retorno
    ----------
        list_aluno (list): 
            Lista com os registros de web scraping do linkedin encontrados.
    ''' 
    list_linkedin = []    
    try:
        linkedin_result = None
        if id!=None:
            linkedin_result = Linkedin.select().where( Linkedin.id == id ).order_by( Linkedin.id )            
        elif profile_url != None:
            linkedin_result = Linkedin.select().where( Linkedin.profile_url == profile_url ).order_by( Linkedin.id )    
        elif date != None:
            linkedin_result = Linkedin.select().where( Linkedin.date == date ).order_by( Linkedin.id )
        elif profile_json != "":
            linkedin_result = Linkedin.select().where( Linkedin.profile_json == profile_json ).order_by( Linkedin.id )
        else:
            linkedin_result = Linkedin.select().order_by( Linkedin.id )    
        
        for row  in linkedin_result.dicts():
            list_linkedin.append(row)
        return list_linkedin
    except Exception as e:
        print(e)
        return list_linkedin




def f_update_linkedin(id=None, aluno_id=None, profile_url=None, date=None, profile_page=None, profile_json=None):
    '''
    Atualiza os dados do registro da combinacao na tabela Linkedin de acordo com o id informado.\n
    Os argumentos enviados como None (não preenchidos) serão armazenados como "null".
   
    Parâmetro
    ----------
        id (int):
            identificador do registro
        profile_url (str):
            endereço da página de perfil.
        date (date):
            data da realização da coleta web.
        profile_page (str):
            conteúdo da página web de perfil.
        profile_json (str):
            conteúdo no formato JSON dos dados processados e extraído da página web.
            
            
    Retorno
    ----------
        (boolean): 
            True indica que foi concluído, False indica que não foi concluído.
    '''    
    
    try:
        if id!=None and profile_url!=None and date!=None:
            query = Linkedin.update( profile_url= profile_url, aluno_id= aluno_id, date= date, profile_page= profile_page, profile_json= profile_json).where(Linkedin.id == id)
            query.execute()
            return True
        raise Exception ('O valor id, profile_url ou date não foram informado!')
    except Exception as e:
        print(e)
        return False

