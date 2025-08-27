import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

class Loucas:
    model = ifcopenshell.open('250304_PORTO DOS GAUCHOS_CRECHE_R03.ifc')

    distribuicoes = model.by_type('IfcDistributionElement')
    element = ifcopenshell.util.element
    tipo = []

    for distribuicao in distribuicoes:
        tipo.append(element.get_type(distribuicao).Name)

        
    tipo = {
        'Item': tipo
    }
    tipo = pd.DataFrame(tipo)
    tipo.to_csv('./results/LoucasEMetais.csv', sep=';', encoding='utf-8')
