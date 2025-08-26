import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.util.element
import ifcopenshell.api
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import pandas as pd
from SCR.Product import *
from tqdm import tqdm

class Vigas:
    def getAtributes(self, list):
        product = Product()
        
        pbar = tqdm(total = len(list), leave= False)

        element = ifcopenshell.util.element

        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)

        vigas_name = []
        vigas_elevacao, vigas_secaobw, vigas_secaoh,vigas_taxaarmadura = [], [], [], []
        vigas_classe_concreto, vigas_cobrimento = [], []
        vigas_area_lateral, vigas_perimetro, vigas_laterais = [], [], []
        vigas_altura, vigas_largura, vigas_volume,vigas_comprimento= [], [], [], []

        for i, viga in enumerate(list):
            vigas_name.append(viga.Name)
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
            pbar.update()

        vigas_name.append('TOTAL')
        vigas_altura.append(round(sum(vigas_altura,2)))
        vigas_largura.append(round(sum(vigas_largura,2)))
        vigas_comprimento.append(round(sum(vigas_comprimento,2)))
        vigas_volume.append(round(sum(vigas_volume,2)))
        vigas_area_lateral.append(round(sum(vigas_area_lateral,2)))
        vigas_perimetro.append(round(sum(vigas_perimetro,2)))
        vigas_laterais.append(round(sum(vigas_laterais,2)))
        vigas_elevacao.append('0')
        vigas_secaobw.append(round(sum(vigas_secaobw,2)))
        vigas_secaoh.append(round(sum(vigas_secaoh,2)))
        vigas_taxaarmadura.append('0')
        vigas_classe_concreto.append('0')
        vigas_cobrimento.append('0')

            
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
            'Cobrimento':vigas_cobrimento
        }

        return dic