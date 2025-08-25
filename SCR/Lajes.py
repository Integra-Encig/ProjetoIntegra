import ifcopenshell 
import ifcopenshell.util.element
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_footprint_area
import numpy as np 
from SCR.Product import *

def executeLajes():
    model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
    element = ifcopenshell.util.element

    product = Product()

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    slabs = model.by_type('IfcSlab')

    lajes = []
    lajes_name = []
    classe_concreto, cobrimento = [], []
    altura, largura, comprimento = [],[],[]
    area, volume = [],[]
    perimetro = []

    for i, laje in enumerate(slabs):
        shape = create_shape(settings, laje)
        lajes_name.append(laje.Name)
        product.append_Element(classe_concreto, element, laje, 'AltoQi_Eberick_Padrão', 'Classe de concreto',False)
        product.append_Element(cobrimento, element, laje, 'AltoQi_Eberick_Padrão', 'Cobrimento',False)
        altura.append(round(product.get_height(shape),2))
        largura.append(round(product.get_length(shape),2))
        comprimento.append(round(product.get_width(shape),2))
        area.append(round(largura[i]*comprimento[i],2))
        volume.append(round(largura[i]*comprimento[i]*altura[i],2))
        perimetro.append(round(float(get_footprint_area(shape.geometry)),2))

    lajes_name.append('TOTAL')
    classe_concreto.append('')
    cobrimento.append('')
    altura.append(round(sum(altura),2))
    largura.append(round(sum(largura),2))
    comprimento.append(round(sum(comprimento),2))
    area.append(round(sum(area),2))
    volume.append(round(sum(volume),2))
    perimetro.append(round(sum(perimetro),2))

    dic = {
        'Nome':lajes_name,
        'Classe de concreto':classe_concreto,
        'Cobrimento':cobrimento,
        'Altura m':altura,
        'Largura m':largura,
        'Comprimento m':comprimento,
        'Area m²':area,
        'Volume m³':volume,
        'Perimetro m ²':perimetro
    }

    df = pd.DataFrame(dic)

    df.to_csv('./results/lajes.csv', sep=';',encoding='latin1',index=False)







