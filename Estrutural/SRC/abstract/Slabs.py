import numpy as np
import abc
import ifcopenshell.util.element
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_footprint_perimeter
import pandas as pd
import numpy as np

class Slabs(abc.ABC):   
    
        
    """Essa é uma classe abstrata que armazena os atributos 'gerais' de objetos de fundação(Sapatas, Baldrames,
        Estacas e Blocos), como volume de concreto, volume de concreto magro, area da forma, area de impermeabilização
        nivel/elevação, coordenadas relativas e fase do projeto
    )"""

    @property
    @abc.abstractmethod
    def _id(self):
        pass

    @_id.setter
    @abc.abstractmethod
    def _id(self,object):
        pass

    #Esse método obtém todos os psets de um elemento como um data frame 1 x n e informações como volume de concreto

    def getPsets(self,object):
        element = ifcopenshell.util.element
        placement = object.ObjectPlacement
        dic = (element.get_psets(object))
        
        psets = pd.DataFrame(dic).drop('id').T
        
        for col in psets.columns:
            try:  
                psets[col] =psets[col].astype('float64').round(decimals=2)
            except:
                pass

        psets['id'] = self._id
        psets['Nível'] = ifcopenshell.util.element.get_container(object).Name
        points = placement.RelativePlacement.Location.Coordinates
        points = tuple(round(x,2) for x in points)
        coord = ",".join(map(str, points))
        psets['Coordenada Relativa'] = coord
        psets = psets.groupby('id',as_index=False).first()
        return(psets)
    


   