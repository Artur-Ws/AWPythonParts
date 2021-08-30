import os
import tkinter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

def check_allplan_version(build_ele, version):

    return True

def create_element(build_ele, doc):

    element = Slab(doc)

    return element.create(build_ele)

print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


class Slab():

    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self,build_ele):
        self.create_slab(build_ele)
        return(self.model_ele_list, self.handle_list)

### "Name" in .pyp file is reference to parameter when create an element

    def create_slab(self, build_ele):

        slab = AllplanGeo.Polyhedron3D.CreateCuboid(1000,1000,1000)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        slab_obiect = AllplanBasisElements.ModelElement3D(com_prop, slab)

        return self.model_ele_list.append(slab_obiect)




########################################################################################################################
window = tkinter.Tk()
window.title("Non-crashed")
info = tkinter.Label(window, text='Jeśli widzisz to okno to wszystko raczej działa')
info.grid(column=0, row=0)
window.mainloop()