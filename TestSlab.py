
import tkinter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPart import View2D3D, PythonPart

import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import GeometryValidate as GeometryValidate
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties

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
        python_part = self.create_slab(build_ele)

        return(python_part, self.handle_list)

### "Name" in .pyp file is reference to parameter when create an element

    def create_slab(self, build_ele):

        model_ele_list = []
        reinf_list = []
        thickness = build_ele.Thickness.value
        length = build_ele.Length.value
        width = build_ele.Width.value

        balcony = AllplanGeo.Polyhedron3D.CreateCuboid(width, length, thickness)
        mirror_pol = AllplanGeo.Polygon3D()
        mirror_pol += AllplanGeo.Point3D(width / 2, 0, 0)
        mirror_pol += AllplanGeo.Point3D(width / 2, length, 0)
        mirror_pol += AllplanGeo.Point3D(width / 2, 0, thickness)
        err, mirror_plane = AllplanGeo.Polygon3D.GetPlane(mirror_pol)

        if build_ele.sl_height.value > 0:
            slope = self.slope(build_ele, thickness, length, width)
            err, balcony = AllplanGeo.MakeUnion(balcony, slope)

        if build_ele.is_front.value == True:
            front_drip = self.drip_front(build_ele, width, length)
            err, balcony = AllplanGeo.MakeSubtraction(balcony,front_drip)

        left_drip, right_drip = self.drip_side(build_ele, width, length, mirror_plane)

        if build_ele.is_side.value == True:
            err, balcony = AllplanGeo.MakeSubtraction(balcony, left_drip)
            err, balcony = AllplanGeo.MakeSubtraction(balcony, right_drip)

        if build_ele.ws_height.value > 0 and build_ele.ws_length.value > 0 and 4 < build_ele.ws_angle.value < 90:
            waterstop = self.waterstop(build_ele, width, length, thickness, build_ele.sl_height.value)
            err, balcony = AllplanGeo.MakeUnion(balcony, waterstop)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        slab_obiect = AllplanBasisElements.ModelElement3D(com_prop, balcony)
        model_ele_list.append(slab_obiect)

        if build_ele.bottom_checkbox.value:
            self.bottom_mesh(build_ele, reinf_list)
        if build_ele.top_checkbox.value:
            self.main_mesh(build_ele, reinf_list)
        if build_ele.side_ubars_checkbox.value:
            self.side_ubars(build_ele, reinf_list)
        if build_ele.front_ubars_checkbox.value:
            self.front_ubars(build_ele, reinf_list)
        if build_ele.back_ubars_checkbox.value:
            self.back_ubars(build_ele, reinf_list)

        views = [View2D3D (model_ele_list)]

        pythonpart = PythonPart("TestSlab",
                                parameter_list=build_ele.get_params_list(),
                                hash_value=build_ele.get_hash(),
                                python_file=build_ele.pyp_file_name,
                                views=views,
                                reinforcement = reinf_list)
        return pythonpart.create()

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
        ws_pol += AllplanGeo.Point3D(0, ws_length + ws_sl_length, slab_thickness)
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

    def drip_side(self, build_ele, width, length, mirror_plane):
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



        err, left_drip = AllplanGeo.CreatePolyhedron(drip_pol, drip_path)

        right_drip = AllplanGeo.Mirror(left_drip,mirror_plane)


        return left_drip, right_drip

    def bottom_mesh(self, build_ele, reinf_list):

        bottom_concrete_cover = build_ele.bottom_down_ConcreteCover.value
        side_concrete_cover = build_ele.bottom_side_ConcreteCover.value
        steel_grade = build_ele.bottom_SteelGrade.value
        f_diameter = build_ele.bottom_first_diameter.value
        s_diameter = build_ele.bottom_second_diameter.value

        # First placement

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints([
                                 (AllplanGeo.Point2D(0, 0), side_concrete_cover),
                                 (AllplanGeo.Point2D(build_ele.Width.value, 0), side_concrete_cover),
                                 side_concrete_cover])

        shape = shape_builder.CreateShape(f_diameter, -1, steel_grade, -1,
                                          AllplanReinf.BendingShapeType.LongitudinalBar)

        start_point = AllplanGeo.Point3D(0, f_diameter/2 + 20, bottom_concrete_cover + f_diameter/2)
        end_point = AllplanGeo.Point3D(0, build_ele.Length.value - side_concrete_cover - side_concrete_cover - f_diameter/2 - 20, bottom_concrete_cover + f_diameter/2)

        reinf_list.append(LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, shape, start_point, end_point,
                    bottom_concrete_cover, bottom_concrete_cover, build_ele.bottom_first_spacing.value,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance, True))

        # Secondary placement

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints([(AllplanGeo.Point2D(0, 0), side_concrete_cover),
                                 (AllplanGeo.Point2D(0, build_ele.Length.value), side_concrete_cover), side_concrete_cover])

        shape = shape_builder.CreateShape(s_diameter, -1, steel_grade, -1,
                                          AllplanReinf.BendingShapeType.LongitudinalBar)

        start_point = AllplanGeo.Point3D(side_concrete_cover + side_concrete_cover + s_diameter/2 + 20, 0, bottom_concrete_cover + f_diameter + s_diameter/2)
        end_point = AllplanGeo.Point3D(build_ele.Width.value - s_diameter/2 - 20, 0, bottom_concrete_cover + f_diameter + s_diameter/2)


        reinf_list.append(LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, shape,
                    start_point, end_point, bottom_concrete_cover, bottom_concrete_cover, build_ele.bottom_second_spacing.value,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance, True))


    def main_mesh(self, build_ele, reinf_list):

        concrete_cover = build_ele.up_ConcreteCover.value
        steel_grade = build_ele.up_SteelGrade.value
        f_diameter = build_ele.up_first_diameter.value
        s_diameter = build_ele.up_second_diameter.value
        height = build_ele.Thickness.value + build_ele.sl_height.value

        # First Placement
        addition = (build_ele.sl_height.value * (concrete_cover + s_diameter / 2 + 20)) / build_ele.Length.value  # difference between height at the start of placement and max height of slope

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints([(AllplanGeo.Point2D(0,0), concrete_cover),
                                 (AllplanGeo.Point2D(0,build_ele.Length.value), concrete_cover), (concrete_cover)])

        shape = shape_builder.CreateShape(f_diameter, -1, steel_grade, -1, AllplanReinf.BendingShapeType.LongitudinalBar)
        angle = math.degrees(math.atan(build_ele.sl_height.value/build_ele.Length.value))

        shape.Rotate(RotationAngles(-angle, 0, 0))
        print(angle)
        start_point = AllplanGeo.Point3D(concrete_cover + f_diameter/2 + 20, 0, height - f_diameter/2 - concrete_cover)
        end_point = AllplanGeo.Point3D(build_ele.Width.value - concrete_cover - f_diameter/2 - 20, 0, height - f_diameter/2 - concrete_cover)

        reinf_list.append(LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, shape, start_point, end_point,
                    concrete_cover, concrete_cover, build_ele.up_first_spacing.value,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance, True))


        # Secondary Placement

        addition = (build_ele.sl_height.value * (concrete_cover + s_diameter/2 + 20))/build_ele.Length.value  #difference between height at the start of placement and max height of slope
        add2 = f_diameter * build_ele.sl_height.value / build_ele.Length.value
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints([(AllplanGeo.Point2D(0,0), concrete_cover),
                                 (AllplanGeo.Point2D(build_ele.Width.value,0), concrete_cover), (concrete_cover)])

        shape = shape_builder.CreateShape(s_diameter, -1, steel_grade, -1, AllplanReinf.BendingShapeType.LongitudinalBar)

        start_point = AllplanGeo.Point3D(0, concrete_cover + s_diameter/2 + 20, height - s_diameter/2 - f_diameter - concrete_cover - addition - add2)
        end_point = AllplanGeo.Point3D(0, build_ele.Length.value - concrete_cover - s_diameter/2 - 20, build_ele.Thickness.value - s_diameter/2 - concrete_cover - f_diameter + addition - add2)

        reinf_list.append(LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, shape, start_point, end_point,
                    concrete_cover, concrete_cover, build_ele.up_second_spacing.value,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance, True))

    def side_ubars(self, build_ele, reinf_list):
        top_cover         = build_ele.side_ubars_top_cover.value
        bottom_cover      = build_ele.side_ubars_bottom_cover.value
        side_cover        = build_ele.side_ubars_side_cover.value
        steel_grade       = build_ele.side_ubars_SteelGrade.value
        diameter          = build_ele.side_ubars_diameter.value
        spacing           = build_ele.side_ubars_spacing.value
        ends_length       = build_ele.side_ubars_ends_length.value
        count             = int(build_ele.Length.value / spacing) + 1
        height            = build_ele.Thickness.value
        height_with_slope = build_ele.Thickness.value + build_ele.sl_height.value
        start_hook_angle  = build_ele.side_ubars_start_hook_angle.value
        end_hook_angle    = build_ele.side_ubars_end_hook_angle.value
        f_diameter        = build_ele.up_first_diameter.value
        tan_a             = build_ele.sl_height.value / build_ele.Length.value
        addition          = (side_cover + diameter/2) * tan_a
        bending_roller    = self.bending_roller(diameter)
# set start/end hook to -1 if checkbox false
        if build_ele.side_ubars_hook_checkbox == True:
            start_hook = build_ele.side_ubars_start_hook.value
            end_hook = build_ele.side_ubars_end_hook.value
        else:
            start_hook = -1
            end_hook = -1
        concrete_cover_props = ConcreteCoverProperties.all(0)

###   LEFT SIDE UBARS   ###

        model_angles = RotationAngles(0, 90, -90)

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, -1, AllplanReinf.BendingShapeType.OpenStirrup)

        shape_higher = GeneralShapeBuilder.create_open_stirrup(height_with_slope - top_cover - bottom_cover - diameter - f_diameter/2 - addition,
                                                               ends_length + diameter/2, model_angles, shape_props,
                                                               concrete_cover_props, start_hook,end_hook,
                                                               start_hook_angle, end_hook_angle)

        shape_higher.Move(AllplanGeo.Vector3D(side_cover + diameter/2, 2*side_cover + diameter/2, height_with_slope - top_cover - diameter/2 - f_diameter/2 - addition))


        shape_lower = GeneralShapeBuilder.create_open_stirrup(height - top_cover - bottom_cover - diameter - f_diameter/2 + addition,
                                                              ends_length, model_angles, shape_props, concrete_cover_props,
                                                              start_hook, end_hook, start_hook_angle, end_hook_angle)

        shape_lower.Move(AllplanGeo.Vector3D(side_cover + diameter/2, build_ele.Length.value - 2*side_cover - diameter/2, height - top_cover - diameter/2 - f_diameter/2 + addition))

        reinf_list.append(AllplanReinf.BarPlacement(1, count, shape_higher, shape_lower))

###   RIGHT SIDE UBARS   ###

        r_model_angles = RotationAngles(0, 90, 90)

        r_shape_higher = GeneralShapeBuilder.create_open_stirrup(height_with_slope - top_cover - bottom_cover - diameter - f_diameter/2 - addition,
                                                                 ends_length + diameter/2, r_model_angles, shape_props,
                                                                 concrete_cover_props, start_hook,end_hook,
                                                                 start_hook_angle, end_hook_angle)

        r_shape_higher.Move(AllplanGeo.Vector3D(build_ele.Width.value - side_cover - diameter/2, 2*side_cover + diameter/2,
                                                height_with_slope - top_cover - diameter/2 - f_diameter/2 - addition))

        r_shape_lower = GeneralShapeBuilder.create_open_stirrup(height - top_cover - bottom_cover - diameter - f_diameter/2 + addition,
                                                                ends_length, r_model_angles, shape_props, concrete_cover_props,
                                                                start_hook, end_hook, start_hook_angle, end_hook_angle)

        r_shape_lower.Move(AllplanGeo.Vector3D(build_ele.Width.value -side_cover + diameter/2,
                                               build_ele.Length.value - 2*side_cover - diameter/2, height - top_cover - diameter/2 - f_diameter/2 + addition))

        reinf_list.append(AllplanReinf.BarPlacement(1, count, r_shape_higher, r_shape_lower))

    def front_ubars(self, build_ele, reinf_list):

        top_cover = build_ele.front_ubars_top_cover.value
        bottom_cover = build_ele.front_ubars_bottom_cover.value
        side_cover = build_ele.front_ubars_side_cover.value
        steel_grade = build_ele.side_ubars_SteelGrade.value
        diameter = build_ele.front_ubars_diameter.value
        spacing = build_ele.front_ubars_spacing.value
        ends_length = build_ele.front_ubars_ends_length.value
        bending_roller = self.bending_roller(diameter)
        count = int(build_ele.Length.value / spacing) + 1
        height            = build_ele.Thickness.value
        height_with_slope = build_ele.Thickness.value + build_ele.sl_height.value
        start_hook_angle = build_ele.front_ubars_start_hook_angle.value
        end_hook_angle = build_ele.front_ubars_end_hook_angle.value
        f_diameter = build_ele.up_first_diameter.value
        tan_a = build_ele.sl_height.value / build_ele.Length.value
        addition = (side_cover + diameter / 2) * tan_a

        # set start/end hook to -1 if checkbox false
        if build_ele.side_ubars_checkbox == True:
            start_hook = build_ele.side_ubars_start_hook.value
            end_hook = build_ele.side_ubars_end_hook.value
        else:
            start_hook = -1
            end_hook = -1
        concrete_cover_props = ConcreteCoverProperties.all(0)
        model_angles = RotationAngles(0, 90, 180)

        ###   FIRST UBARS   ###

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.OpenStirrup)

        shape_first = GeneralShapeBuilder.create_open_stirrup(
            height - top_cover - bottom_cover - diameter, ends_length + diameter / 2,
            model_angles, shape_props, concrete_cover_props, start_hook, end_hook, start_hook_angle, end_hook_angle)

        shape_first.Move(AllplanGeo.Vector3D(2*side_cover + diameter / 2,
                                             build_ele.Length.value - side_cover - diameter / 2,
                                             height - top_cover - f_diameter + diameter + addition))

        ###   LAST UBARS   ###
        shape_last = GeneralShapeBuilder.create_open_stirrup(
            height - top_cover - bottom_cover - diameter, ends_length + diameter / 2,
            model_angles, shape_props, concrete_cover_props, start_hook, end_hook, start_hook_angle, end_hook_angle)

        shape_last.Move(AllplanGeo.Vector3D(build_ele.Width.value - 2*side_cover - diameter / 2,
                                            build_ele.Length.value - side_cover - diameter / 2,
                                            height - top_cover + diameter - f_diameter + addition))

        reinf_list.append(AllplanReinf.BarPlacement(1, count, shape_first, shape_last))

    def back_ubars(self, build_ele, reinf_list):

        top_cover = build_ele.back_ubars_top_cover.value
        bottom_cover = build_ele.back_ubars_bottom_cover.value
        side_cover = build_ele.back_ubars_side_cover.value
        steel_grade = build_ele.side_ubars_SteelGrade.value
        diameter = build_ele.back_ubars_diameter.value
        spacing = build_ele.back_ubars_spacing.value
        ends_length = build_ele.back_ubars_ends_length.value
        bending_roller = self.bending_roller(diameter)
        count = int(build_ele.Length.value / spacing) + 1
        height_with_slope = build_ele.Thickness.value + build_ele.sl_height.value
        start_hook_angle = build_ele.back_ubars_start_hook_angle.value
        end_hook_angle = build_ele.back_ubars_end_hook_angle.value
        f_diameter = build_ele.up_first_diameter.value
        tan_a = build_ele.sl_height.value / build_ele.Length.value
        addition = (side_cover + diameter / 2) * tan_a

        # set start/end hook to -1 if checkbox false
        if build_ele.side_ubars_checkbox == True:
            start_hook = build_ele.side_ubars_start_hook.value
            end_hook = build_ele.side_ubars_end_hook.value
        else:
            start_hook = -1
            end_hook = -1
        concrete_cover_props = ConcreteCoverProperties.all(0)
        model_angles = RotationAngles(0, 90, 0)

        ###   FIRST UBARS   ###

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.OpenStirrup)

        shape_first = GeneralShapeBuilder.create_open_stirrup(
            height_with_slope - top_cover - bottom_cover - diameter, ends_length + diameter / 2,
            model_angles, shape_props, concrete_cover_props, start_hook, end_hook, start_hook_angle, end_hook_angle)

        shape_first.Move(AllplanGeo.Vector3D(2*side_cover + diameter / 2,
                                             side_cover + diameter / 2,
                                             height_with_slope - top_cover - f_diameter + diameter + addition))

        ###   LAST UBARS   ###
        shape_last = GeneralShapeBuilder.create_open_stirrup(
            height_with_slope - top_cover - bottom_cover - diameter, ends_length + diameter / 2,
            model_angles, shape_props, concrete_cover_props, start_hook, end_hook, start_hook_angle, end_hook_angle)

        shape_last.Move(AllplanGeo.Vector3D(build_ele.Width.value - 2*side_cover - diameter / 2,
                                            side_cover + diameter / 2,
                                            height_with_slope - top_cover + diameter - f_diameter + addition))

        reinf_list.append(AllplanReinf.BarPlacement(1, count, shape_first, shape_last))


    def bending_roller(self, diameter):
        if diameter > 16:
            bending_roller = 7
        else:
            bending_roller = 4
        return bending_roller
########################################################################################################################
# window = tkinter.Tk()
# window.title("Non-crashed")
# info = tkinter.Label(window, text='Jeśli widzisz to okno to wszystko raczej działa')
# info.grid(column=0, row=0)
# window.mainloop()