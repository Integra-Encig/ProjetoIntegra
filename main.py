from SCR.Colunas import *
from SCR.Estacas import *
from SCR.Lajes import *
from SCR.Sapatas import *
from SCR.VigasBaldrame import *
from SCR.VigasLajeCobertura import *
from SCR.VigasPlatibanda import *
from tqdm import tqdm

pbar = tqdm((range(8)))

executeColunas()
pbar.update()
executeCobertura()
pbar.update()
executeEstacas()
pbar.update()
executeLajes()
pbar.update()
executeSapatas()
pbar.update()
executeBaldrame()
pbar.update()
executeCobertura()
pbar.update()
executePlatibanda()
pbar.update()