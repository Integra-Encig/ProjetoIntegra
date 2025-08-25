import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.util.element
import ifcopenshell.api
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import pandas as pd
from SCR.Product import *
from SCR.Vigas import *

def executePlatibanda():
    model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
    vigas_class = Vigas()

    element = ifcopenshell.util.element

    beams = model.by_type('IfcBeam')

    vigas = []


    for viga in beams:
        if element.get_container(viga).Name == 'Platibanda':
            vigas.append(viga)
            
    dic = vigas_class.getAtributes(vigas)

    dic = pd.DataFrame(dic)
    dic.to_csv('./results/vigasplatibanda.csv', sep=';',encoding='latin1',index=False)




