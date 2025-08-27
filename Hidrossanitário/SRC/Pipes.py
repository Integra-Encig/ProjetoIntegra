import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from PipeSegments import *

class Pipes:
    def Pipes(cano):
        model = ifcopenshell.open('25-060-CRECHE PORTO DOS GAÚCHOS-HID.ifc')
        pipe_segments = model.by_type('IfcPipeSegment')
        canos = []
        element = ifcopenshell.util.element

        for pipe in pipe_segments:

            if (element.get_psets(pipe)['Identificação_Elemento']['Rede'] == f'{cano}'):
                canos.append(pipe)

        dic = PipeSegments.get_PipeDic(canos)
        
        dic.to_csv(f'./results/{cano}.csv', sep = ';', encoding= 'latin1')
