import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import numpy as np
from SCR.Product import *
import math
# from bonsai.bim.ifc import IfcStore
from tqdm import tqdm


def executeSapatas():
    model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
    element = ifcopenshell.util.element

    product = Product()

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)






    footings = model.by_type('IfcFooting')
    
    pbar = tqdm(total = len(footings),leave= False)
    
    sapatas = []
    sapatas_name = []
    sapatas_altura, sapatas_largura, sapatas_volume,sapatas_comprimento= [], [], [], []
    sapatas_classe_concreto, sapatas_cobrimento = [], []
    sapatas_area_lateral, sapatas_perimetro, sapatas_laterais = [], [], []
    base_concreto_magro = []

    for sapata in footings:
        if element.get_predefined_type(sapata) == 'PAD_FOOTING':
            sapatas.append(sapata)
            sapatas_name.append(sapata.Name)  

    sapatas_name.append('TOTAL')

    for i, sapata in enumerate(sapatas):  
        shape = create_shape(settings,sapata)  

        sapatas_altura.append(round(float(product.get_parallelepiped_heigth(shape)),2))
        sapatas_largura.append(product.get_length(shape))
        sapatas_comprimento.append(product.get_width(shape))
        sapatas_volume.append(product.get_volume(shape))


        product.append_Element(sapatas_classe_concreto, element, sapata, 'AltoQi_Eberick_Padrão', 'Classe de concreto',False)
        product.append_Element(sapatas_cobrimento, element, sapata, 'AltoQi_Eberick_Padrão', 'Cobrimento',False)
        sapatas_perimetro.append(round(float(get_footprint_perimeter(shape.geometry)),2))
        sapatas_laterais.append(round(sapatas_perimetro[i]*sapatas_altura[i],2))
        base_concreto_magro.append(round((sapatas_largura[i]*sapatas_comprimento[i])*0.05,2))
        pbar.update()

    sapatas_altura.append(round(sum(sapatas_altura),2))
    sapatas_largura.append(round(sum(sapatas_largura),2))
    sapatas_comprimento.append(round(sum(sapatas_comprimento),2))
    sapatas_volume.append(round(sum(sapatas_volume),2))
    sapatas_perimetro.append(round(sum(sapatas_perimetro),2))
    sapatas_laterais.append(round(sum(sapatas_laterais),2))
    base_concreto_magro.append(round(sum(base_concreto_magro),2))
    sapatas_classe_concreto.append('')
    sapatas_cobrimento.append('')


    dic = {

        'Nome':sapatas_name,
        'Altura m':sapatas_altura,
        'Largura m':sapatas_largura,
        'Comprimento m':sapatas_comprimento,
        'Volume m³':sapatas_volume,
        'Cobrimento':sapatas_cobrimento,
        'Classe do concreto':sapatas_classe_concreto,
        'Perimetro²':sapatas_perimetro,
        'Formas m²':sapatas_laterais,
        'Base Concreto Magro m³':base_concreto_magro
    }

    dic = pd.DataFrame(dic)
    dic.to_csv('./results/sapatas.csv', sep=';',encoding='latin1',index=False)