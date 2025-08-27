import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

class PipeSegments():
    
    def get_PipeDic(list):
        element = ifcopenshell.util.element

        comp_max, diam_int, diam, espess, ind, comp = [], [],[],[],[],[]
        nome, classe, tipo, aplicacao = [], [], [], []
        for pipe in list:
                comp_max.append(element.get_psets(pipe)['AltoQi_Builder']['Comprimento máximo'])
                # diam_int.append(element.get_psets(pipe)['AltoQi_Builder']['Diâmetro interno'])
                diam.append(element.get_psets(pipe)['AltoQi_Builder']['Diâmetro'])
                espess.append(element.get_psets(pipe)['AltoQi_Builder']['Espessura'])
                ind.append(element.get_psets(pipe)['AltoQi_Builder']['Indicação'])
                comp.append(round(float(element.get_psets(pipe)['AltoQi_Builder']['Comprimento']),2))

                nome.append(element.get_psets(pipe)['Identificação_Elemento']['Nome'])
                classe.append(element.get_psets(pipe)['Identificação_Elemento']['Classe'])
                tipo.append(element.get_psets(pipe)['Identificação_Elemento']['Tipo'])
                aplicacao.append(element.get_psets(pipe)['Identificação_Elemento']['Aplicação'])

        dic ={
            # 'Nome':nome,
            # 'Comprimento máximo': comp_max,
            # 'Diâmetro interno':diam_int,
            # 'Diâmetro':diam,
            # 'Diâmetro':espess,
            'Diâmetro':ind,
            'Comprimento m':comp,
            # 'Classe':classe,
            # 'Tipo':tipo,
            # 'Aplicação':aplicacao
        }
        


        dic = pd.DataFrame(dic)



        dic = dic[['Diâmetro', 'Comprimento m']]
        dic = dic.groupby('Diâmetro').sum()
        dic['Comprimento m'] = round(dic['Comprimento m'],2)


        return dic