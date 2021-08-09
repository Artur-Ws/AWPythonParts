"""
Script for GetObjectAttributesInteractor
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import os
from BuildingElementService import BuildingElementService
from BuildingElementPaletteService import BuildingElementPaletteService
from TraceService import TraceService

print('Load GetObjectAttributesInteractor.py')


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    """
    Creation of element (only necessary for the library preview)

    Args:
        build_ele: the building element.
        doc:       input document
    """

    del build_ele
    del doc

    return (None, None, None)


def create_interactor(coord_input, pyp_path, show_pal_close_btn, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return GetObjectAttributesInteractor(coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list)


class GetObjectAttributesInteractor():
    """
    Definition of class GetObjectAttributesInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
        """
        Initialization of class GetObjectAttributesInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input        = coord_input
        self.pyp_path           = pyp_path
        self.str_table_service  = str_table_service
        self.attribute_function = None
        self.element_filter     = None

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Click the button, output is shown in the trace window"))

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             "Attributes",
                                                             control_props_list, pyp_path + "\\GetObjectAttributesInteractor")

        self.palette_service.show_palette("GetObjectAttributesInteractor")


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True


    def process_mouse_msg(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        if not self.attribute_function:
            return True

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter)

        element = self.coord_input.GetSelectedElement()

        if element.IsNull():
            return True

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        self.attribute_function(element)

        return True


    def on_control_event(self, event_id):
        """
        On control event

        Args:
            event_id: event id of control.
        """

        if event_id == 1001:
            print("fgsdfgfsgtrhsryh hfd shtrgregrea rae  ger e")
            self.get_attributes()
            self.PrintToTxt()


            return

        if event_id == 1002:
            self.get_reinforcement_bars_fixture_attributes()
            return

        if event_id in [1003, 1004]:
            type_query = AllplanIFW.QueryTypeID(AllplanElementAdapter.WallTier_TypeUUID)

            sel_query = AllplanIFW.SelectionQuery(type_query)

            self.element_filter = AllplanIFW.ElementSelectFilterSetting(sel_query, True)

            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select the wall, output is shown in the trace window"))

            self.attribute_function = self.get_wall_attributes if event_id == 1003 else self.get_precast_element_attributes

            return


    def print_attributes(self, element, separator):
        """
        print the attributes
        """

        attributes = AllplanBaseElements.ElementsAttributeService.GetAttributes(element)

        if not attributes:
            return

        if separator:
            print("----------------------------------------------------------------------")

        TraceService.trace_1(str(element))

        print()

        # Get userprofile path (ex. C:\Users\Example_Username\)
        userProfile = os.environ['USERPROFILE']

        # Where the txt file would be saved
        savePath = userProfile + '\\desktop\\PythonParts\\ATTRIBUTES'

        # Check whether directory exists, if not create it
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        # name and extension of the file
        fileName = 'ExampleFileName.txt'
        fullName = os.path.join(savePath, fileName)
        workFile = open(fullName, "a", errors="ignore")
        attributeList = []
        for id, value in attributes:

# TUTAJ !!!!!!!!
            temporaryAttr = str(AllplanBaseElements.AttributeDataManager.GetAttributeName(id) + "(" + str(id) + "): " + str(value) + "\n")
            attributeList.append(temporaryAttr)
            print("####### START #######")
            print(temporaryAttr)
            print("####### STOP #######")

            #workFile.write(temporaryAttr)
            TraceService.trace_1(AllplanBaseElements.AttributeDataManager.GetAttributeName(id) + "(" + str(id) + "): " + str(value))

        attributeString = ''.join(attributeList)
        print(attributeString)
        print("\n--------------------------\n")
        print(type(attributeString))
        print(attributeString.encode())
        print("\n--------------------------\n")

        #print()
        workFile.write(str(attributeString))
        workFile.close()

        print(fullName)


    def get_attributes(self):
        """
        Get the attributes from all objects
        """

        for element in AllplanBaseElements.ElementsSelectService.SelectAllElements(self.coord_input.GetInputViewDocument()):
            self.print_attributes(element, True)


    def get_reinforcement_bars_fixture_attributes(self):
        """
        Get the attributes from reinforcement bars fixture attributes
        """

        for element in AllplanBaseElements.ElementsSelectService.SelectAllElements(self.coord_input.GetInputViewDocument()):
            if element == AllplanElementAdapter.BarsDefinition_TypeUUID:
                print("----------------------------------------------------------------------")
                print(element, "Pos.-Nr.=",AllplanElementAdapter.ReinforcementPropertiesReader.GetPositionNumber(element))
                print(element.GetGeometry())

                def trace_point_fixtures(childs):
                    for child in childs:
                        print("    ", child)

                        if child == AllplanElementAdapter.PointFixture_TypeUUID:
                            self.print_attributes(child, False)

                        elif child == AllplanElementAdapter.BarsLinearPlacement_TypeUUID:
                            print("placement")
                            placement_childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(child)

                            trace_point_fixtures(placement_childs)

                            print("-----------------------------------------")


                childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(element)

                trace_point_fixtures(childs)


    def get_wall_attributes(self, wall_tier):
        """
        Get the attributes from a wall
        """

        wall = AllplanElementAdapter.BaseElementAdapterParentElementService.GetParentElement(wall_tier)

        self.print_attributes(wall, True)

        wall_childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(wall)

        for wall_child in wall_childs:
            if wall_child == AllplanElementAdapter.WallTier_TypeUUID:
                self.print_attributes(wall_child, True)


    def get_precast_element_attributes(self, wall_tier):
        """
        Get the attributes from a wall
        """

        wall = AllplanElementAdapter.BaseElementAdapterParentElementService.GetParentElement(wall_tier)

        self.print_attributes(wall, True)

        wall_childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(wall)

        for wall_child in wall_childs:
            if wall_child == AllplanElementAdapter.PrecastElement_TypeUUID:
                self.print_attributes(wall_child, True)

                print("Mark number:      ", AllplanElementAdapter.PrecastPropertiesService.GetPositionNumber(wall_child))
                print("Mark number pure: ", AllplanElementAdapter.PrecastPropertiesService.GetPositionNumberPure(wall_child))
                print("Type description: ", AllplanElementAdapter.PrecastPropertiesService.GetPrecastElementTypeDescription(wall_child))
                print()

    def PrintToTxt(self):
        # Get userprofile path (ex. C:\Users\Example_Username\)
        userProfile = os.environ['USERPROFILE']

        # Where the txt file would be saved
        savePath = userProfile + '\\desktop\\PythonParts\\TXT'

        # Check whether directory exists, if not create it
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        # name and extension of the file
        fileName = 'ExampleFileName.txt'

        point = '§'

        # -------------------------------------------------------------------------------------

        arg1 = '1'  # E  # Nazwa rysunku
        arg2 = '2'  # G  # Numer ryunku
        arg3 = '3'  # H  # Data utworzenia rysunku
        arg4 = '4'  # I  # Ostatnia Rewizja
        arg5 = '5'  # J  # Data ostatniej rewizji
        arg6 = '6'  # M  # Ilość sztuk danego elementu
        arg7 = '7'  # N  # Objtość elementu netto
        arg8 = '8'  # AI # Klasa betonu
        arg9 = '9'  # AH # Minimalna wytrzymałość betonu przy rozformowaniu
        arg10 = '10'  # R  # Stal zbrojeniowa - masa zbrojenia [kg]
        arg11 = '11'  # X  # Stal sprężająca - dół / ILOŚĆ strun w dolnej części elementu
        arg12 = '12'  # Y  # Stal sprężająca - dół / ŚREDNICA strun w dolnej części elementu
        arg13 = '13'  # Z  # Stal sprężająca – dół/NACIĄG – siła naciągu strun w dolnej części elementu [kN]
        arg14 = '14'  # AA # Stal sprężająca – góra/ILOŚĆ strun w górnej części elementu
        arg15 = '15'  # AB # Stal sprężająca – góra/ŚREDNICA strun w dolnej części elementu
        arg16 = '16'  # AC # Stal sprężająca – góra/NACIĄG – siła naciągu strun w dolnej części elementu [kN]
        arg17 = '17'  # AF # Odporność ogniowa
        arg18 = '18'  # AG # Klasa expozycji
        arg19 = '19'  # AJ # strun w dolnej części elementu [mm]
        arg20 = '20'  # AK # Szerokość elementu – określa szerokość elementu [mm]
        arg21 = '21'  # AL # Wysokość elementu – określa wysokość elementu [mm]
        arg22 = '22'  # K  # Status – status rysunku (zgodnie z określoną listą)
        arg23 = '23'  # L  # nazwa fabryki
        arg24 = '24'  # T  # Siatki zbrojeniowe – masa siatek zbrojeniowych [kg]
        arg25 = '25'  # W  # Masa elementów – masa stalowych elementów [kg]
        # ------------ BE do BU - masa stali zbrojeniowej danej średnicy [kg] ------------ #
        arg26 = 'fi 4'  # BE # fi 4
        arg27 = 'fi 5'  # BF # fi 5
        arg28 = 'fi 6'  # BG # fi 6
        arg29 = 'fi 8'  # BH # fi 8
        arg30 = 'fi 10'  # BI # fi 10
        arg31 = 'fi 12'  # BJ # fi 12
        arg32 = 'fi 14'  # BK # fi 14
        arg33 = 'fi 16'  # BL # fi 16
        arg34 = 'fi 18'  # BM # fi 18
        arg35 = 'fi 20'  # BN # fi 20
        arg36 = 'fi 22'  # BO # fi 22
        arg37 = 'fi 25'  # BP # fi 25
        arg38 = 'fi 28'  # BQ # fi 28
        arg39 = 'fi 32'  # BR # fi 32
        arg40 = 'fi 40'  # BS # fi 40
        arg41 = 'fi 42'  # BT # fi 42
        arg42 = 'fi 45'  # BU # fi 45
        # -------------------------------------------------------------------------------------------------------------------- #
        arg43 = '27'  # BB # Występuje – parametr dla akcesoriów stalowych, dający informacje w jakich elementach występuje
        arg44 = '28'  # Q  # Sztuki tab. zbrojeniowa – ilość sztuk całego zbrojenia dla danego elementu
        arg45 = '29'  # V  # Sztuki tab. stal – ilość elementów stalowych
        # ------- HS do IP - Rev_... – rewizja elementu, pobiera takie dane jak: symbol rewizji, opis, data, użytkownik ------ #
        arg46 = 'REV1'  # HS #
        arg47 = 'REV2'  # HT ##
        arg48 = 'REV3'  # HU ###
        arg49 = 'REV4'  # HV ####
        arg50 = 'REV5'  # HW #####
        arg51 = 'REV6'  # HX ###### Prawdopodobnie nieaktualne i zawsze puste
        arg52 = 'REV7'  # HY ####
        arg53 = 'REV8'  # HZ ###
        arg54 = 'REV9'  # IA ##
        arg55 = 'REV10'  # IB #
        # -------------------------------------------------------------------------------------------------------------------- #
        arg56 = '31'  # S  # Sztuki tab. siatki – ilość sztuk siatek dla zbrojenia danego elementu
        arg57 = '32'  # O  # Masa – masa elementu (netto) [kg]
        arg58 = '33'  # P  # Masa montażowa – masa montażowa elementu [kg]
        arg59 = '34'  # BC # Symbol z oferty – nieaktualne
        arg60 = '35'  # AM # Powierzchnia po obrysie [m2]

        arg61 = '§$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$'  # REWIZJE # Rozdzielone '|' rewizje. Pobiera takie informacje jak: symbol rewizji, komentarz, datę rewizji i użytkownika.

        arg62 = '37'  # A   # Nazwa – nazwa elementu
        arg63 = '38'  # B   # Typ – typ elementu (zgodnie z określoną listą)
        arg64 = '39'  # C   # Zakres – określa miejsce występowania elementu
        arg65 = '40'  # D   # Część – określa czy element ma orientację poziomą czy pionową
        arg66 = '41'  # D1  # Indeks kontraktu
        arg67 = '42'  # D2  # Nazwa pliku dwg
        arg68 = '43'  # D3  # Nazwa użytkownika wykonującego funkcje „pref”-export danych
        arg69 = '44'  # D4  # Typ formy (tylko na dźwigarów „w tej chwili”)
        arg70 = '45'  # D5  # Lista pkt POLX (czyli obwiednia elementu)
        arg71 = '46'  # D6  # Wykończenie (tekst w postaci Malowanie, Paint, Tynkowanie,Plastering, Cegla, Brick)
        arg72 = '47'  # D7  # Rysunek wykończenia (tekst w postaci WS_001M)
        arg73 = '48'  # D8  # Wysokość stron dół  (dla plyt HC)
        arg74 = '49'  # D9  # Wysokość strun góra (dla płyt HC)
        arg75 = '50'  # D10 # Wymiar całkowity długość
        arg76 = '51'  # D11 # Wymiar całkowity szerokośc
        arg77 = '52'  # D12 # Wymiar całkowity wysokość
        arg78 = '53'  # D13 # objętość warstwy elewacyjnej
        arg79 = '54'  # D14 # Objętośc warstwy konstrukcyjnej

        content = ''
        for i in range(79):
            value = "arg" + str(i + 1)
            content += point + eval(value)  # get value of an expression
            print(content)

        fullName = os.path.join(savePath, fileName)

        workFile = open(fullName, "w")
        workFile.write(content)
        workFile.close()

        print(fullName)

