
from SCR.Sapatas import *

import ifcopenshell.util.element


model = ifcopenshell.open('IFC_CONC_RESTAURANTE.IFC')

footings = model.by_type('IfcFooting')
element = ifcopenshell.util.element
df = pd.DataFrame()

for sapata in footings:
        if element.get_predefined_type(sapata) == 'PAD_FOOTING':
            Sapatas(sapata)
            sapatadf = pd.concat([df, Sapatas(sapata).get_psets(sapata)], ignore_index=True)
            df = sapatadf

sapatadf = pd.DataFrame(sapatadf)

sapatadf.to_csv('./sapatateste.csv', sep=';', encoding='latin1',index=False)
    
