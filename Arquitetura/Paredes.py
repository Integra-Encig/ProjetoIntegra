import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_area
import numpy as np
from tqdm import tqdm

class Paredes:
    model = ifcopenshell.open('250304_PORTO DOS GAUCHOS_CRECHE_R03.ifc')

    walls = model.by_type('IfcWall')

    element = ifcopenshell.util.element

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    pbar = tqdm(total=len(walls))
    tipo = []
    area_lateral_bruta, volume_bruto = [],[]
    area_lateral_liquida, volume_liquido = [],[]
    altura, largura, espessura = [], [], []

    for wall in walls:
        tipo.append(element.get_type(wall).Name)
        area_lateral_bruta.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['GrossSideArea'],2))
        area_lateral_liquida.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['NetSideArea'],2))
        volume_bruto.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['GrossVolume'],2))
        volume_liquido.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['NetVolume'],2))
        altura.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['Height'],2))
        largura.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['Length'],2))
        espessura.append(round(element.get_psets(wall,qtos_only= False)['Qto_WallBaseQuantities']['Width'],2))
        pbar.update()

    dic = {
        'Tipo':tipo,
        'Área lateral bruta': area_lateral_bruta,
        'Área lateral liquida': area_lateral_liquida,
        'Volume Bruto': volume_bruto,
        'Volume Liquido': volume_liquido,
        'Altura':altura,
        'Largura':largura,
        'Espessura': espessura
    }

    dic = pd.DataFrame(dic)

    dic.to_csv('./results/Paredes.csv', sep=';', encoding='latin1')