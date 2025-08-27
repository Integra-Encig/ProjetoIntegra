import ifcopenshell
import ifcopenshell.util.element
import pandas as pd
from PipeSegments import *
from Calhas import *

class Pluvial:
    def Pluvial():
        model = ifcopenshell.open('25-060-CRECHE PORTO DOS GAÚCHOS-HID.ifc')
        pipe_segments = model.by_type('IfcPipeSegment')
        calha = []
        element = ifcopenshell.util.element

        for pipe in pipe_segments:

            if (element.get_psets(pipe)['Identificação_Elemento']['Rede'] == f'{'Pluvial'}'):
                calha.append(pipe)
        Calhas.Calhas(calha)    

    