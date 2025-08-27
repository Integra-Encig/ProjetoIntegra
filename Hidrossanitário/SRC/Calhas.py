import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

class Calhas:
    
    def Calhas(list):
        element = ifcopenshell.util.element
        comp = []
        aplicacao = []

        for pipe in list:

                comp.append(round(float(element.get_psets(pipe)['AltoQi_Builder']['Comprimento']),2))
                aplicacao.append(element.get_psets(pipe)['Identificação_Elemento']['Aplicação'])

        dic ={
            'Aplicação':aplicacao,
            'Comprimento m':comp,
        }

        dic = pd.DataFrame(dic)

        dic = dic[['Aplicação', 'Comprimento m']]
        dic = dic.groupby('Aplicação').sum()
        dic['Comprimento m'] =  dic['Comprimento m']/100
        dic['Comprimento m'] = round(dic['Comprimento m'],2)

        dic.to_csv(f'./results/Calhas.csv', sep = ';', encoding= 'latin1')


        return dic