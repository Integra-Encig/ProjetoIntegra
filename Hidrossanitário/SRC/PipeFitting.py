import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

model = ifcopenshell.open('25-060-CRECHE PORTO DOS GAÚCHOS-HID.ifc')
element = ifcopenshell.util.element


pipe_fitting = model.by_type('IfcPipeFitting')
tipos, ind = [], []


for joelhos in pipe_fitting:
    tipos.append(element.get_psets(joelhos)['Identificação_Elemento']['Tipo'])
    ind.append(element.get_psets(joelhos)['AltoQi_Builder']['Indicação'])

dic = {
    'Tipo': tipos,
    'Indicação':ind

}

dic = pd.DataFrame(dic)
dic = dic.groupby(['Tipo','Indicação']).value_counts()
dic = pd.DataFrame(dic)
dic.to_csv(f'./results/Acessorios.csv', sep = ';', encoding= 'latin1')




# {'AltoQi_Builder':
#     {'Indicação': '100 mm', 'Posição': 'Direta',},
# 'Identificação_Elemento':
#     {'Aplicação': 'Conexão', 'Descrição': 'Joelho 90º Serie R desce', 'Nome': '100 mm', 'Classe': 'PVC Esgoto - série Reforçada', 'Tipo': 'Joelho 90º Serie R - desce', 'Rede': 'Pluvial',},
# 'Pset_PipeFittingTypeCommon':
#     {'Reference': 'Joelho 90º Serie R - desce', }}