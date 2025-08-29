
from SCR.Sapatas import *
from SCR.Baldrame import *
from SCR.Estacas import *
from SCR.Blocos import *


import ifcopenshell.util.element


model = ifcopenshell.open('IFC_CONC_RESTAURANTE.IFC')
element = ifcopenshell.util.element
df = pd.DataFrame()


footings = model.by_type('IfcFooting')
vigas = model.by_type('IfcBeam')
colunas = model.by_type('IfcColumn')
pilares = model.by_type('IfcPile')

slabs = model.by_type('IfcSlab')



for sapata in footings:
        if element.get_predefined_type(sapata) == 'PAD_FOOTING':
            sapata_obj = Sapatas(sapata)
            sapatadf = pd.concat([df, sapata_obj.getPsets(sapata)], ignore_index=True)
            df = sapatadf
df = None
for viga in vigas:
    if(element.get_container(viga).Name == 'Baldrame'):
        viga_obj = Baldrame(viga)
        baldramedf = pd.concat([df, viga_obj.getPsets(viga)], ignore_index=True)
        df = baldramedf
# df = None
# for coluna in colunas:
#     coluna_obj = Colunas(coluna)
#     colunadf = pd.concat([df, coluna_obj.getPsets(coluna)], ignore_index=True)
#     df = colunadf
df = None
for estaca in pilares:
    estaca_obj = Estacas(estaca)
    estacadf = pd.concat([df, estaca_obj.getPsets(estaca)], ignore_index=True)
    df = estacadf
# df = None
# for slab in slabs:
#     slab_obj = Lajes(slab)
#     slabdf = pd.concat([df, slab_obj.getPsets(slab)], ignore_index=True)
#     df = slabdf



pd.set_option('display.precision',10)




sapatadf = pd.DataFrame(sapatadf)


sapatadf.to_csv('./results/sapata.csv', sep=';', encoding='latin1',index=False)
baldramedf.to_csv('./results/baldrame.csv', sep=';', encoding='latin1',index=False)
# vigacobertura.to_csv('./results/cobertura.csv', sep=';', encoding='latin1',index=False)
# colunadf.to_csv('./results/coluna.csv', sep=';', encoding='latin1',index=False)
estacadf.to_csv('./results/estaca.csv', sep=';', encoding='latin1',index=False)
estacadf.to_csv('./results/laje.csv', sep=';', encoding='latin1',index=False)
    
    
