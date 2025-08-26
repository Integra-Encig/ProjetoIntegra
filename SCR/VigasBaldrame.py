import ifcopenshell
import ifcopenshell.util.placement
import ifcopenshell.util.element
import ifcopenshell.api
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_side_area, get_footprint_area, get_footprint_perimeter
import pandas as pd
from SCR.Product import *
from SCR.Vigas import *
from tqdm import tqdm

def executeBaldrame():
    model = ifcopenshell.open('25-007-PRG-CR5-CONC-R00.IFC')
    vigas_class = Vigas()
    element = ifcopenshell.util.element
    beams = model.by_type('IfcBeam')
    pbar = tqdm(total=len(beams))
    vigas = []
    vigas_forma = []
    vigas_impermeabilizante = []

    for viga in beams:
        if element.get_container(viga).Name == 'Baldrame':
            vigas.append(viga)
    dic = vigas_class.getAtributes(vigas)

    

    


    dic = pd.DataFrame(dic)

    dic['Seção H'] = dic['Seção H'].astype(float)
    dic['Seção Bw'] = dic['Seção Bw'].astype(float)
    dic['Comprimento m'] = dic['Comprimento m'].astype(float)

    dic['Area Forma m²']= round(((2*dic['Seção H'])+ dic['Seção Bw'])*dic['Comprimento m'],2)
    dic['Impermeabilizante m²']= round((2*(dic['Seção H'] + dic['Seção Bw'])*(dic['Comprimento m'])),2)
    dic['Area Forma m²'].loc[-1] = round(dic['Area Forma m²'].sum(),2)
    # for i, record in enumerate(dic):

    #     dic['Area Forma m²'].iloc[i] = round(((2*dic['Seção H'].iloc[i])+ dic['Seção Bw'].iloc[i])*dic['Comprimento m'].iloc[i],2)
    #     dic['Impermeabilizante m²'].iloc[i] = round((2*(dic['Seção H'].iloc[i] + dic['Seção Bw'].iloc[i]))*dic['Comprimento m'].iloc[i],2)
    # dic['Area Forma'] = ((2*dic['Seção H'])+ dic['Seção Bw'])*dic['Comprimento m']
    dic.to_csv('./results/vigasbaldrame.csv', sep=';',encoding='latin1',index=False)




