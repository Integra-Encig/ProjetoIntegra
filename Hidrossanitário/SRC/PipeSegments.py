import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

class PipeSegments():
    
    def get_PipeDic(list):
        element = ifcopenshell.util.element
        ind, comp = [], [],[],[],[],[]

        # comp_max, diam_int, diam, espess, 
        # nome, classe, tipo, aplicacao = [], [], [], []

        for pipe in list:
                # comp_max.append(element.get_psets(pipe)['AltoQi_Builder']['Comprimento máximo'])
                # # diam_int.append(element.get_psets(pipe)['AltoQi_Builder']['Diâmetro interno'])
                # diam.append(element.get_psets(pipe)['AltoQi_Builder']['Diâmetro'])
                # espess.append(element.get_psets(pipe)['AltoQi_Builder']['Espessura'])

                ind.append(element.get_psets(pipe)['AltoQi_Builder']['Indicação'])
                comp.append(round(float(element.get_psets(pipe)['AltoQi_Builder']['Comprimento']),2))

                # nome.append(element.get_psets(pipe)['Identificação_Elemento']['Nome'])
                # classe.append(element.get_psets(pipe)['Identificação_Elemento']['Classe'])
                # tipo.append(element.get_psets(pipe)['Identificação_Elemento']['Tipo'])
                # aplicacao.append(element.get_psets(pipe)['Identificação_Elemento']['Aplicação'])

        dic ={
            'Diâmetro':ind,
            'Comprimento m':comp,
        }

        dic = pd.DataFrame(dic)

        dic = dic[['Diâmetro', 'Comprimento m']]
        dic = dic.groupby('Diâmetro').sum()
        dic['Comprimento m'] = dic['Comprimento m']/100
        dic['Comprimento m'] = round(dic['Comprimento m'],2)


        return dic