
import ifcopenshell
import ifcopenshell.util.element
from SCR.Product import *
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_footprint_area
import numpy as np
from tqdm import tqdm


def executeColunas():
    model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
    element = ifcopenshell.util.element

    product = Product()

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)


    columns = model.by_type('IfcColumn')

    pbar = tqdm(total=len(columns), leave= False)

    coluna_name = []
    coluna_area_forma = []
    classe_concreto, cobrimento = [], []

    for coluna in columns:
        shape = create_shape(settings,coluna)
        coluna_name.append(coluna.Name)
        product.append_Element(classe_concreto, element, coluna, 'AltoQi_Eberick_Padrão','Classe de concreto',False)
        product.append_Element(cobrimento, element, coluna, 'AltoQi_Eberick_Padrão','Cobrimento',False)
        coluna_area_forma.append(round((get_footprint_area(shape.geometry)) * product.get_height(shape),2))
        pbar.update()
    coluna_name.append('TOTAL')
    classe_concreto.append('')
    cobrimento.append('')
    coluna_area_forma.append(round(sum(coluna_area_forma),2))

    dic = {
        'Nome': coluna_name,
        'Classe de concreto': classe_concreto,
        'Cobrimento': cobrimento,
        'Área forma m²': coluna_area_forma 
    }

    df = pd.DataFrame(dic)
    df.to_csv('./results/colunas.csv', sep=';',encoding='latin1',index=False)
