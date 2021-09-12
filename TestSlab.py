
import tkinter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPart import View2D3D, PythonPart

import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import GeometryValidate as GeometryValidate

import math

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

        thickness = build_ele.Thickness.value
        length = build_ele.Length.value
        width = build_ele.Width.value
        slab = AllplanGeo.Polyhedron3D.CreateCuboid(width, length, thickness)


        slope = self.slope(build_ele, thickness, length, width)
        err, balcony = AllplanGeo.MakeUnion(slab, slope)

        if build_ele.is_front.value == True:
            front_drip = self.drip_front(build_ele, width, length)
            err, balcony = AllplanGeo.MakeSubtraction(balcony,front_drip)

        left_drip, right_drip = self.drip_side(build_ele, width, length)

        if build_ele.is_side.value == True:
            err, balcony = AllplanGeo.MakeSubtraction(balcony, left_drip)
            err, balcony = AllplanGeo.MakeSubtraction(balcony, right_drip)

        waterstop = self.waterstop(build_ele, width, length, thickness, build_ele.sl_height.value)

        err, balcony = AllplanGeo.MakeUnion(balcony, waterstop)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        slab_obiect = AllplanBasisElements.ModelElement3D(com_prop, balcony)

        return self.model_ele_list.append(slab_obiect)

    def slope(self, build_ele, thickness, length, width):

        sl_height = build_ele.sl_height.value
        slope_pol = AllplanGeo.Polygon3D()
        slope_pol += AllplanGeo.Point3D(0, 0, thickness)
        slope_pol += AllplanGeo.Point3D(0, 0, thickness + sl_height)
        slope_pol += AllplanGeo.Point3D(0, length, thickness)
        slope_pol += AllplanGeo.Point3D(0, 0, thickness)

        slope_path = AllplanGeo.Polyline3D()
        slope_path += AllplanGeo.Point3D(0, 0, thickness)
        slope_path += AllplanGeo.Point3D(width, 0, thickness)

        err, slope = AllplanGeo.CreatePolyhedron(slope_pol, slope_path)
        return slope

    def waterstop(self, build_ele, slab_width, slab_length, slab_thickness, slope_height):

        ws_height = build_ele.ws_height.value
        ws_length = build_ele.ws_length.value
        ws_angle = build_ele.ws_angle.value

        r_angle = math.radians(ws_angle)
        ctg = 1 / math.tan(r_angle)
        ws_sl_length = (slope_height + ws_height) * ctg

        ws_pol = AllplanGeo.Polygon3D()
        ws_pol += AllplanGeo.Point3D(0, 0, slab_thickness + slope_height)
        ws_pol += AllplanGeo.Point3D(0, 0, slab_thickness + slope_height + ws_height)
        ws_pol += AllplanGeo.Point3D(0, ws_length, slab_thickness + slope_height + ws_height)
        ws_pol += AllplanGeo.Point3D(0, ws_length + ws_sl_length , slab_thickness)
        ws_pol += AllplanGeo.Point3D(0, 0, slab_thickness + slope_height)

        ws_path = AllplanGeo.Polyline3D()
        ws_path += AllplanGeo.Point3D(0, 0, slab_thickness + slope_height)
        ws_path += AllplanGeo.Point3D(slab_width, 0, slab_thickness + slope_height)

        err, waterstop = AllplanGeo.CreatePolyhedron(ws_pol, ws_path)

        return waterstop

    def drip_front(self, build_ele, width, length):
        drip_height = build_ele.drip_height.value
        drip_width = build_ele.drip_width.value
        drip_offset = build_ele.drip_offset.value

        drip_pol = AllplanGeo.Polygon3D()
        drip_pol += AllplanGeo.Point3D(drip_offset, length - drip_offset, 0)
        drip_pol += AllplanGeo.Point3D(drip_offset, length - drip_offset - drip_width, 0)
        drip_pol += AllplanGeo.Point3D(drip_offset, length - drip_offset - drip_width/2, drip_height)
        drip_pol += AllplanGeo.Point3D(drip_offset, length - drip_offset, 0)

        drip_path = AllplanGeo.Polyline3D()
        drip_path += AllplanGeo.Point3D(drip_offset, 0, 0)
        drip_path += AllplanGeo.Point3D(width - drip_offset, 0, 0)

        err, front_drip = AllplanGeo.CreatePolyhedron(drip_pol, drip_path)

        return front_drip

    def drip_side(self, build_ele, width, length):
        '''Creates and returns two drip polyhedrons, one on each side'''
        drip_height = build_ele.drip_height.value
        drip_width = build_ele.drip_width.value
        drip_offset = build_ele.drip_offset.value
        drip_start = build_ele.drip_start.value

        drip_pol = AllplanGeo.Polygon3D()
        drip_pol += AllplanGeo.Point3D(drip_offset, drip_start, 0)
        drip_pol += AllplanGeo.Point3D(drip_offset + drip_width, drip_start, 0)
        drip_pol += AllplanGeo.Point3D(drip_offset + drip_width/2, drip_start, drip_height)
        drip_pol += AllplanGeo.Point3D(drip_offset, drip_start, 0)

        drip_path = AllplanGeo.Polyline3D()
        drip_path += AllplanGeo.Point3D(drip_offset, drip_start, 0)
        drip_path += AllplanGeo.Point3D(drip_offset, length - drip_offset, 0)

        mirror_pol = AllplanGeo.Polygon3D()
        mirror_pol += AllplanGeo.Point3D(width/2, 0, 0)
        mirror_pol += AllplanGeo.Point3D(width/2, length, 0)
        mirror_pol += AllplanGeo.Point3D(width/2, 0, drip_height)
        err, mirror_plane = AllplanGeo.Polygon3D.GetPlane(mirror_pol)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(mirror_plane)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        err, left_drip = AllplanGeo.CreatePolyhedron(drip_pol, drip_path)

        right_drip = AllplanGeo.Mirror(left_drip,mirror_plane)


        return left_drip, right_drip



########################################################################################################################
window = tkinter.Tk()
window.title("Non-crashed")
info = tkinter.Label(window, text='Jeśli widzisz to okno to wszystko raczej działa')
info.grid(column=0, row=0)
window.mainloop()