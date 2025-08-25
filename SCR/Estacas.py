
import ifcopenshell
import ifcopenshell.util.element
from SCR.Product import *
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_footprint_area
import numpy as np

def executeEstacas():
    model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
    element = ifcopenshell.util.element

    product = Product()

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)


    piles = model.by_type('IfcPile')

    colunas = []
    coluna_name = []
    coluna_area_forma = []
    classe_concreto, cobrimento = [], []

    for coluna in piles:
        shape = create_shape(settings,coluna)
        coluna_name.append(coluna.Name)
        product.append_Element(classe_concreto, element, coluna, 'Pset_ConcreteElementGeneral','StrengthClass',False)
        product.append_Element(cobrimento, element, coluna, 'Pset_ConcreteElementGeneral','ConcreteCover',False)
        coluna_area_forma.append(round(product.get_height(shape),2))
    coluna_name.append('TOTAL')
    classe_concreto.append('')
    cobrimento.append('')
    coluna_area_forma.append(round(sum(coluna_area_forma),2))

    dic = {
        'Nome': coluna_name,
        'Classe de concreto': classe_concreto,
        'Cobrimento': cobrimento,
        'Altura m': coluna_area_forma 
    }

    df = pd.DataFrame(dic)
    df.to_csv('./results/estacas.csv', sep=';',encoding='latin1',index=False)
