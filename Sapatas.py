import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import numpy as np
from Product import *
import math
# from bonsai.bim.ifc import IfcStore




model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
element = ifcopenshell.util.element

product = Product()

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)






footings = model.by_type('IfcFooting')
sapatas = []
sapatas_name = []
sapatas_altura, sapatas_largura, sapatas_volume,sapatas_espessura= [], [], [], []
sapatas_classe_concreto, sapatas_cobrimento = [], []
sapatas_area_lateral, sapatas_perimetro, sapatas_laterais = [], [], []

for sapata in footings:
    if element.get_predefined_type(sapata) == 'PAD_FOOTING':
        sapatas.append(sapata)
        sapatas_name.append(sapata.Name)  

for i, sapata in enumerate(sapatas):  
    shape = create_shape(settings,sapata)  

    sapatas_altura.append(round(float(product.get_parallelepiped_heigth(shape)),2))
    sapatas_largura.append(product.get_length(shape))
    sapatas_espessura.append(product.get_width(shape))
    sapatas_volume.append(product.get_volume(shape))


    product.append_Element(sapatas_classe_concreto, element, sapata, 'AltoQi_Eberick_Padrão', 'Classe de concreto',False)
    product.append_Element(sapatas_cobrimento, element, sapata, 'AltoQi_Eberick_Padrão', 'Cobrimento',False)
    sapatas_area_lateral.append(round(get_side_area(shape.geometry),2))
    sapatas_perimetro.append(round(float(get_footprint_perimeter(shape.geometry)),2))
    sapatas_laterais.append(round(sapatas_perimetro[i]*sapatas_altura[i],2))
    

dic = {

    'Nome':sapatas_name,
    'Altura m':sapatas_altura,
    'Largura m':sapatas_largura,
    'Comprimento m': sapatas_espessura,
    'Volume m³':sapatas_volume,
    'Área Lateral²':sapatas_area_lateral,
    'Cobrimento':sapatas_cobrimento,
    'Classe do concreto':sapatas_classe_concreto,
    'Perimetro²':sapatas_perimetro,
    'Laterais p/ caixote m³':sapatas_laterais
}

dic = pd.DataFrame(dic)
dic.to_csv('./sapatas.csv', sep=';',encoding='latin1',index=False)