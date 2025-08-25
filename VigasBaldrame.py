import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.util.element
import ifcopenshell.api
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import pandas as pd
from Product import *

model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
product = Product()

placement = ifcopenshell.util.placement
element = ifcopenshell.util.element
api = ifcopenshell.api


settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


beams = model.by_type('IfcBeam')

vigas = []
vigas_name = []
vigas_elevacao, vigas_secaobw, vigas_secaoh,vigas_taxaarmadura = [], [], [], []
vigas_classe_concreto, vigas_cobrimento = [], []
vigas_area_lateral, vigas_perimetro, vigas_laterais = [], [], []
vigas_altura, vigas_largura, vigas_volume,vigas_comprimento= [], [], [], []
vigas_forma = []
vigas_impermeabilizante = []

for viga in beams:
    if element.get_container(viga).Name == 'Baldrame':
        vigas.append(viga)
        vigas_name.append(viga.Name)



for i, viga in enumerate(vigas):
    shape = create_shape(settings, viga)

    vigas_altura.append(product.get_height(shape))
    vigas_largura.append(product.get_length(shape))
    vigas_comprimento.append(product.get_width(shape))

    vigas_volume.append(product.get_volume(shape))
    
    vigas_area_lateral.append(round(get_side_area(shape.geometry),2))
    vigas_perimetro.append(round(float(get_footprint_perimeter(shape.geometry)),2))
    vigas_laterais.append(round(vigas_perimetro[i]*vigas_altura[i],2))



    product.append_Element(vigas_elevacao, element, viga, 'AltoQi_Eberick_Elemento', 'Elevação', False)
    product.append_Element(vigas_secaobw, element, viga, 'AltoQi_Eberick_Elemento', 'Seção_bw', False)
    product.append_Element(vigas_secaoh, element, viga, 'AltoQi_Eberick_Elemento', 'Seção_h', False)
    product.append_Element(vigas_taxaarmadura, element, viga, 'AltoQi_Eberick_Elemento', 'Taxa de armadura', False)
    product.append_Element(vigas_classe_concreto, element, viga, 'AltoQi_Eberick_Padrão', 'Classe de concreto', False)
    product.append_Element(vigas_cobrimento, element, viga, 'AltoQi_Eberick_Padrão', 'Cobrimento', False)

    vigas_forma.append(round(((2*vigas_secaoh[i])+(vigas_secaobw[i]))*vigas_comprimento[i],2))
    vigas_impermeabilizante.append(round((2*(vigas_secaoh[i]+vigas_secaobw[i]))*vigas_comprimento[i],2))


    
dic = {
    'Altura m': vigas_altura,
    'Largura m':vigas_largura,
    'Comprimento m':vigas_comprimento,
    'Volume m³':vigas_volume,
    'Área Lateral m²':vigas_area_lateral,
    'Perímetro m²':vigas_perimetro,
    'Laterais':vigas_laterais,
    'Elevacao':vigas_elevacao,
    'Seção Bw':vigas_secaobw,
    'Seção H':vigas_secaoh,
    'Taxa de armadura':vigas_taxaarmadura,
    'Classe de concreto':vigas_classe_concreto,
    'Cobrimento':vigas_cobrimento,
    'Área forma m²':vigas_forma,
    'Impermeabilizante m²':vigas_impermeabilizante
}

dic = pd.DataFrame(dic)
dic.to_csv('./vigasbaldrame.csv', sep=';',encoding='latin1',index=False)






# AltoQi_Eberick_Elemento
    # Elevação
    # Seção_bw
    # Seção_h
    # Taxa de armadura


# AltoQi_Eberick_Padrão
    # Classe de concreto
    # Cobrimento
# Pset_ConcreteElementGeneral