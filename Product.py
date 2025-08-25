import numpy as np


class Product:
    
    def append_Element(self, list, element, type, col, row, boolean):
        list.append(element.get_psets(type, qtos_only=boolean)[col][row])
        return list
    def get_parallelepiped_heigth(self, shape):
        verts = shape.geometry.verts


        z_coords = [verts[i] for i in range(2,len(verts),3)]
        z_unique = sorted(set(round(z,6) for z in z_coords))

        if len(z_unique) <2:
            return None
        z_base = z_unique[0]
        z_top_block = z_unique[1]

        return z_top_block - z_base

    def get_length(self, shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        largura = ymax - ymin


        return round(largura,2)
    def get_width(self, shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        espessura = xmax - xmin

        return round(espessura,2)
    def get_height(self,shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        altura = zmax - zmin

        return round(altura,2)
    def get_volume(self,shape):
        verts = np.array(shape.geometry.verts).reshape(-1,3)
        
        xmin, ymin, zmin= verts.min(axis=0)
        xmax,ymax, zmax= verts.max(axis=0)

        espessura = xmax - xmin
        largura = ymax - ymin
        altura = zmax - zmin

        return round(espessura*largura*altura,2)