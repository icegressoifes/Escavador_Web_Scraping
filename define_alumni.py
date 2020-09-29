# coding:utf-8
import json
import remove_caracter as rc


def f_define_alumni(json_profile="", institution_name=[], formation=[], study_area=[], period_start=""):
    """
    define_alumni(json_profile: str, institution_name: list, formation: list, study_area: list): boolean
        
    """
    dic_profile = json.loads( json_profile )
    education_list = dic_profile["academico"]
        
    result = False
    j = 0
    while (j < len(education_list)) and (not result):
        count = 0
        education = education_list[j]
        
        flag = False
        for i in range (len(institution_name) ):
            flag = is_contained(institution_name[i], education["instituicao"])
        count += 1 if flag else 0
        
        flag = False
        for i in range ( len(study_area) ):
            flag = ( flag or is_contained( study_area[i], education["curso"] ) )
            if flag: break
        count += 1 if flag else 0
        
        flag = False
        for i in range ( len(formation) ):
            flag = ( flag or is_contained( formation[i], education["titulo"] ) )
            if flag: break                 
        count += 1 if flag else 0     
        
        if ( str(period_start).isdigit() and str(education["ano_inicio"]).isdigit() ) and \
            ( int(period_start) == int(education["ano_inicio"]) ):
            count += 1
            
        if count == 4:
            result = True
        elif count >= 2:
            print("\nEducação: ", education)
            answer = input("\nÉ egresso? S ou N: ")
            result = True if (answer.strip() in "S s") else False
        else:
            result = False
            
        j += 1
        
    return result

            
def is_contained(input1, input2 ):
    input1 = rc.removerAcentosECaracteresEspeciais(input1)
    input2 = rc.removerAcentosECaracteresEspeciais(input2)
    if input1.lower() in input2.lower():
        return True
    return False

