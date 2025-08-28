import numpy as np
import abc
import ifcopenshell.util.element
from ifcopenshell.geom import create_shape
from ifcopenshell.util.shape import get_footprint_perimeter
import pandas as pd

class Footings():   
    """Essa é uma classe abstrata que armazena os atributos 'gerais' de objetos de funcação(Sapatas, Baldrames,
        Estacas e Blocos), como volume de concreto, volume de concreto magro, area da forma, area de impermeabilização
        nivel/elevação, coordenadas relativas e fase do projeto
    )"""

    #Esse método utiliza o objeto espacial para definir seu volume, não nescessário se essa informação existe no pset
    @abc.abstractmethod
    def set_volume(self,shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        espessura = xmax - xmin
        largura = ymax - ymin
        altura = zmax - zmin

        self.concrete_volume = round(espessura*largura*altura,2)
    #Esse método utiliza o objeto espacial para definir seu volume de massa magra, não nescessário se essa informação existe no pset
    @abc.abstractmethod
    def set_lean_volume(self,shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        espessura = xmax - xmin
        largura = ymax - ymin
        altura = zmax - zmin

        self.lean_concrete_volume = round(espessura*largura*0.05,2)
    #Esse método define o ID com base no ID do IFC
    @abc.abstractmethod
    def set_identificador(self,object):
        self._identificador = object

    #Esse método utiliza o objeto espacial para definir sua área de impermeabilização, não nescessário se essa informação existe no pset
    @abc.abstractmethod
    def set_waterproofing(self,shape):
        verts = shape.geometry.verts
        xs = verts[0::3]
        zs = verts[2::3]

        verts = np.array(shape.geometry.verts).reshape(-1,3)

        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        width = xmax - xmin

        bw = max(xs) - min(xs)
        h = max(zs) - min(zs)
        
        waterproofing = (2*(h + bw)* width)

        self.waterproofing_area = round(waterproofing,2)
    
    #Esse método utiliza o objeto espacial para definir sua área de forma, não nescessário se essa informação existe no pset
    @abc.abstractmethod
    def set_shape_area(self,shape):
        
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        altura = zmax - zmin

        self.shape_area =  round(get_footprint_perimeter(shape.geometry)*altura,2)



    @abc.abstractmethod
    #Esse método utiliza o objeto espacial para definir a altura da área de forma caso náo seja paralelepipeda, não nescessário se essa informação existe no pset
    def get_parallelepiped_heigth(self):
        verts = self.shape.geometry.verts

        z_coords = [verts[i] for i in range(2,len(verts),3)]
        z_unique = sorted(set(round(z,6) for z in z_coords))

        if len(z_unique) <2:
            return None
        z_base = z_unique[0]
        z_top_block = z_unique[1]

        return z_top_block - z_base

    #Esse método utiliza o objeto espacial para definir sua largura, não nescessário se essa informação existe no pset
    @abc.abstractmethod
    def get_length(self):
        verts = np.array(self.shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        largura = ymax - ymin


        return round(largura,2)
    #Esse método utiliza o objeto espacial para definir seu comprimento, não nescessário se essa informação existe no pset
    def get_width(self, shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        espessura = xmax - xmin

        return round(espessura,2)
    #Esse método utiliza o objeto espacial para definir sua altura, não nescessário se essa informação existe no pset
    def get_height(self,shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        altura = zmax - zmin

        return round(altura,2)
    
    
    #Esse método obtém todos os psets de um elemento como um data frame 1 x n
    @abc.abstractmethod
    def get_psets(self,object):
        element = ifcopenshell.util.element
        psets = pd.DataFrame(element.get_psets(object)).drop('id').T
        psets['id'] = self._identificador
        
        psets = psets.groupby('id',as_index=False).first()
        return(psets)