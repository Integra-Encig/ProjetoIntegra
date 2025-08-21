import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import math
# from bonsai.bim.ifc import IfcStore



model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
element = ifcopenshell.util.element

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


def append_Element(list, element, type, col, row, boolean):
    list.append(element.get_psets(type, qtos_only=boolean)[col][row])
    return list

def get_parallelepiped_heigth(shape):
    verts = shape.geometry.verts


    z_coords = [verts[i] for i in range(2,len(verts),3)]
    z_unique = sorted(set(round(z,6) for z in z_coords))

    if len(z_unique) <2:
        return None
    z_base = z_unique[0]
    z_top_block = z_unique[1]

    return z_top_block - z_base

footings = model.by_type('IfcFooting')
sapatas = []
sapatas_name = []
sapatas_altura, sapatas_largura, sapatas_volume, sapatas_id = [], [], [], []
sapatas_classe_concreto, sapatas_cobrimento = [], []
sapatas_area_lateral, sapatas_perimetro, sapatas_laterais = [], [], []

for sapata in footings:
    if element.get_predefined_type(sapata) == 'PAD_FOOTING':
        sapatas.append(sapata)
        sapatas_name.append(sapata.Name)  

for i, sapata in enumerate(sapatas):  
    shape = create_shape(settings,sapata)  
    append_Element(sapatas_id, element, sapata, 'Qto_FootingBaseQuantities', 'id',True)
    sapatas_altura.append(round(float(get_parallelepiped_heigth(shape)),2))
    append_Element(sapatas_largura, element, sapata, 'Qto_FootingBaseQuantities', 'Length',True)
    append_Element(sapatas_volume, element, sapata, 'Qto_FootingBaseQuantities', 'NetVolume',True)
    sapatas_volume[i] = round(sapatas_volume[i],2)
    append_Element(sapatas_classe_concreto, element, sapata, 'AltoQi_Eberick_Padrão', 'Classe de concreto',False)

    append_Element(sapatas_cobrimento, element, sapata, 'AltoQi_Eberick_Padrão', 'Cobrimento',False)
    sapatas_area_lateral.append(round(get_side_area(shape.geometry),2))
    sapatas_perimetro.append(round(float(get_footprint_perimeter(shape.geometry)),2))
    sapatas_laterais.append(round(sapatas_perimetro[i]*sapatas_altura[i],2))

dic = {
    'ID':sapatas_id,
    'Nome':sapatas_name,
    'Altura':sapatas_altura,
    'Largura':sapatas_largura,
    'Volume':sapatas_volume,
    'Área Lateral':sapatas_area_lateral,
    'Cobrimento':sapatas_cobrimento,
    'Classe do concreto':sapatas_classe_concreto,
    'Perimetro':sapatas_perimetro,
    'Laterais':sapatas_laterais
}

dic = pd.DataFrame(dic)
dic.to_csv('./sapatas.csv', sep=';',encoding='latin1',index=False)