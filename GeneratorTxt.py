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
            #self.PrintToTxt()


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


    def print_attributes(self, element, separator, fileName = 'example.txt'):
        """
        print the attributes
        """
        # Get userprofile path (ex. C:\Users\Example_Username\)
        userProfile = os.environ['USERPROFILE']

        # Where the txt file would be saved
        savePath = userProfile + '\\desktop\\PythonParts\\ATTRIBUTES\\'

        # Check whether directory exists, if not create it
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        # name and extension of the file
        #fileName = 'ExampleFileName.txt'
        fullName = os.path.join(savePath, fileName)
        workFile = open(fullName, "w", errors="ignore")
        attributeList = []

        attributes = AllplanBaseElements.ElementsAttributeService.GetAttributes(element)

        if not attributes:
            return

        if separator:
            print("----------------------------------------------------------------------")

        TraceService.trace_1(str(element))

        print()


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
        print(attributeString)
        print("\n--------------------------\n")

        #print()
        workFile.write(str(attributeString))
        workFile.close()

        print(fullName)


    def get_attributes(self):
        """
        Get the attributes from all objects
        """
        i = 0
        for element in AllplanBaseElements.ElementsSelectService.SelectAllElements(self.coord_input.GetInputViewDocument()):
            i += 1
            self.print_attributes(element, True, fileName=str(element) + str(i) + '.txt')
            self.PrintToTxt(fileName=str(element) + str(i) + '.txt')  # zmieni?? domy??lny str na nazw?? elementu

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

    def search_attribute(self, attribute_number, fileName, multiplier = 1):
        source_path = os.environ['USERPROFILE'] + '\\desktop\\PythonParts\\ATTRIBUTES\\' + str(fileName)
        txt_file = open(source_path, 'rt')
        attribute_to_search = '(' + str(attribute_number) + '): '
        attribute_value = ''
        for line in txt_file:
            if attribute_to_search in line:
                index1 = line.find(attribute_to_search)  # index of first "(" symbol of attribute_to_search
                length_of_attribute_number = len(attribute_to_search)
                index2 = index1 + length_of_attribute_number
                attribute_value = line[index2:-1]
                return attribute_value * multiplier

        if attribute_value == '':
            return attribute_value


    def PrintToTxt(self, fileName):
        # Get userprofile path (ex. C:\Users\Example_Username\)
        userProfile = os.environ['USERPROFILE']

        # Where the txt file would be saved
        savePath = userProfile + '\\desktop\\PythonParts\\TXT\\'

        # Check whether directory exists, if not create it
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        # name and extension of the file
        #fileName = 'ExampleFileName.txt'

        point = '??'

        # -------------------------------------------------------------------------------------

        arg1 = self.search_attribute('empty', fileName)   # E  # Nazwa rysunku                                                                                 @
        arg2 = self.search_attribute(1021, fileName)      # G  # Numer ryunku                                                                               @1021@
        arg3 = self.search_attribute(443, fileName)       # H  # Data utworzenia rysunku                                                                     @443@
        arg4 = self.search_attribute(440, fileName)       # I  # Ostatnia Rewizja                                                                            @440@
        arg5 = self.search_attribute(433, fileName)       # J  # Data ostatniej rewizji                                                                      @433@
        arg6 = self.search_attribute(18065, fileName)     # M  # Ilo???? sztuk danego elementu                                                               @18065@
        arg7 = self.search_attribute(223, fileName)       # N  # Objto???? elementu netto                                                                      @223@
        arg8 = self.search_attribute(1063, fileName)      # AI # Klasa betonu                                                                               @1063@
        arg9 = self.search_attribute(1083, fileName)      # AH # Minimalna wytrzyma??o???? betonu przy rozformowaniu                                           @1083@
        arg10 = self.search_attribute(1058, fileName)     # R  # Stal zbrojeniowa - masa zbrojenia [kg]                                                     @1058@
        arg11 = self.search_attribute(36057, fileName)    # X  # Stal spr????aj??ca - d???? / ILO???? strun w dolnej cz????ci elementu                              @36057@
        arg12 = self.search_attribute(36046, fileName)    # Y  # Stal spr????aj??ca - d???? / ??REDNICA strun w dolnej cz????ci elementu                           @36046@
        arg13 = self.search_attribute(36059, fileName)    # Z  # Stal spr????aj??ca ??? d????/NACI??G ??? si??a naci??gu strun w dolnej cz????ci elementu [kN]           @36059@
        arg14 = self.search_attribute(36043, fileName)    # AA # Stal spr????aj??ca ??? g??ra/ILO???? strun w g??rnej cz????ci elementu                               @36043@
        arg15 = self.search_attribute(36042, fileName)    # AB # Stal spr????aj??ca ??? g??ra/??REDNICA strun w dolnej cz????ci elementu                            @36042@
        arg16 = self.search_attribute(36045, fileName)    # AC # Stal spr????aj??ca ??? g??ra/NACI??G ??? si??a naci??gu strun w dolnej cz????ci elementu [kN]          @36045@
        arg17 = self.search_attribute(1084, fileName)     # AF # Odporno???? ogniowa                                                                          @1084@
        arg18 = self.search_attribute(1031, fileName)     # AG # Klasa expozycji                                                                            @1031@
        arg19 = self.search_attribute(198, fileName)      # AJ # strun w dolnej cz????ci elementu [mm]                                                         @198@
        arg20 = self.search_attribute(199, fileName)      # AK # Szeroko???? elementu ??? okre??la szeroko???? elementu [mm]                                        @199@
        arg21 = self.search_attribute(204, fileName)      # AL # Wysoko???? elementu ??? okre??la wysoko???? elementu [mm]                                          @204@
        arg22 = self.search_attribute(1890, fileName)     # K  # Status ??? status rysunku (zgodnie z okre??lon?? list??)                                        @1890@
        arg23 = self.search_attribute(36075, fileName)    # L  # nazwa fabryki                                                                             @36075@
        arg24 = self.search_attribute('empty', fileName)  # T  # Siatki zbrojeniowe ??? masa siatek zbrojeniowych [kg]                                         @
        arg25 = self.search_attribute('empty', fileName)  # W  # Masa element??w ??? masa stalowych element??w [kg]                                              @
        # ------------ BE do BU - masa stali zbrojeniowej danej ??rednicy [kg] ------------ #                             @
        arg26 = self.search_attribute('empty', fileName)  # BE # fi 4
        arg27 = self.search_attribute('empty', fileName)  # BF # fi 5
        arg28 = self.search_attribute('empty', fileName)  # BG # fi 6
        arg29 = self.search_attribute('empty', fileName)  # BH # fi 8
        arg30 = self.search_attribute('empty', fileName)  # BI # fi 10
        arg31 = self.search_attribute('empty', fileName)  # BJ # fi 12
        arg32 = self.search_attribute('empty', fileName)  # BK # fi 14
        arg33 = self.search_attribute('empty', fileName)  # BL # fi 16
        arg34 = self.search_attribute('empty', fileName)  # BM # fi 18
        arg35 = self.search_attribute('empty', fileName)  # BN # fi 20
        arg36 = self.search_attribute('empty', fileName)  # BO # fi 22
        arg37 = self.search_attribute('empty', fileName)  # BP # fi 25
        arg38 = self.search_attribute('empty', fileName)  # BQ # fi 28
        arg39 = self.search_attribute('empty', fileName)  # BR # fi 32
        arg40 = self.search_attribute('empty', fileName)  # BS # fi 40
        arg41 = self.search_attribute('empty', fileName)  # BT # fi 42
        arg42 = self.search_attribute('empty', fileName)  # BU # fi 45
        # -------------------------------------------------------------------------------------------------------------------- #
        arg43 = self.search_attribute('empty', fileName)  # BB # Wyst??puje ??? parametr dla akcesori??w stalowych, daj??cy informacje w jakich elementach wyst??puje
        arg44 = self.search_attribute(18065, fileName)  # Q  # Sztuki tab. zbrojeniowa ??? ilo???? sztuk ca??ego zbrojenia dla danego elementu
        arg45 = self.search_attribute('empty', fileName)  # V  # Sztuki tab. stal ??? ilo???? element??w stalowych
        # ------- HS do IP - Rev_... ??? rewizja elementu, pobiera takie dane jak: symbol rewizji, opis, data, u??ytkownik ------ #
        arg46 = self.search_attribute('empty', fileName)  # HS #
        arg47 = self.search_attribute('empty', fileName)  # HT ##
        arg48 = self.search_attribute('empty', fileName)  # HU ###
        arg49 = self.search_attribute('empty', fileName)  # HV ####
        arg50 = self.search_attribute('empty', fileName)  # HW #####
        arg51 = self.search_attribute('empty', fileName)  # HX ###### Prawdopodobnie nieaktualne i zawsze puste
        arg52 = self.search_attribute('empty', fileName)  # HY ####
        arg53 = self.search_attribute('empty', fileName)  # HZ ###
        arg54 = self.search_attribute('empty', fileName)  # IA ##
        arg55 = self.search_attribute('empty', fileName)  # IB #
        # -------------------------------------------------------------------------------------------------------------------- #
        arg56 = self.search_attribute('empty', fileName)  # S  # Sztuki tab. siatki ??? ilo???? sztuk siatek dla zbrojenia danego elementu
        arg57 = self.search_attribute(721, fileName, multiplier=1000)  # O  # Masa ??? masa elementu (netto) [kg]
        arg58 = self.search_attribute(721, fileName, multiplier=1150)  # P  # Masa monta??owa ??? masa monta??owa elementu [kg]
        arg59 = self.search_attribute('empty', fileName)  # BC # Symbol z oferty ??? nieaktualne
        arg60 = self.search_attribute('empty', fileName)  # AM # Powierzchnia po obrysie [m2]

        arg61 = '??$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$|$ $$'  # REWIZJE # Rozdzielone '|' rewizje. Pobiera takie informacje jak: symbol rewizji, komentarz, dat?? rewizji i u??ytkownika.

        arg62 = self.search_attribute(1021, fileName)  # A   # Nazwa ??? nazwa elementu
        arg63 = self.search_attribute(1893, fileName)  # B   # Typ ??? typ elementu (zgodnie z okre??lon?? list??)
        arg64 = self.search_attribute('empty', fileName)  # C   # Zakres ??? okre??la miejsce wyst??powania elementu
        arg65 = self.search_attribute('empty', fileName)  # D   # Cz?????? ??? okre??la czy element ma orientacj?? poziom?? czy pionow??
        arg66 = self.search_attribute(936, fileName)  # D1  # Indeks kontraktu
        arg67 = self.search_attribute('empty', fileName)  # D2  # Nazwa pliku dwg
        arg68 = self.search_attribute(20, fileName)  # D3  # Nazwa u??ytkownika wykonuj??cego funkcje ???pref???-export danych
        arg69 = self.search_attribute(36061, fileName)  # D4  # Typ formy (tylko na d??wigar??w ???w tej chwili???)
        arg70 = self.search_attribute('empty', fileName)  # D5  # Lista pkt POLX (czyli obwiednia elementu)
        arg71 = self.search_attribute('empty', fileName)  # D6  # Wyko??czenie (tekst w postaci Malowanie, Paint, Tynkowanie,Plastering, Cegla, Brick)
        arg72 = self.search_attribute('empty', fileName)  # D7  # Rysunek wyko??czenia (tekst w postaci WS_001M)
        arg73 = self.search_attribute('empty', fileName)  # D8  # Wysoko???? stron d????  (dla plyt HC)
        arg74 = self.search_attribute('empty', fileName)  # D9  # Wysoko???? strun g??ra (dla p??yt HC)
        arg75 = self.search_attribute('empty', fileName)  # D10 # Wymiar ca??kowity d??ugo????
        arg76 = self.search_attribute('empty', fileName)  # D11 # Wymiar ca??kowity szeroko??c
        arg77 = self.search_attribute('empty', fileName)  # D12 # Wymiar ca??kowity wysoko????
        arg78 = self.search_attribute('empty', fileName)  # D13 # obj??to???? warstwy elewacyjnej
        arg79 = self.search_attribute('empty', fileName)  # D14 # Obj??to??c warstwy konstrukcyjnej

        content = ''
        for i in range(79):
            value = "arg" + str(i + 1)
            content += point + eval(value)  # get value of an expression
            print(content)
        if self.search_attribute(1021, fileName) == '':
            tempFileName = "delete"
        else:
            tempFileName = self.search_attribute(1021, fileName) + '.txt'        ### !!!!!   W MIEJSCE ATR. 498 WPISAC NR ATRYBUTU ODPOWIEDZIALNEGO ZA NAZWE ELEMENTU   !!!!!!!


        fullName = os.path.join(savePath, tempFileName)

        if tempFileName == 'delete':
            pass
        else:
            workFile = open(fullName, "w")
            workFile.write(content)
            workFile.close()

        print(fullName)
        #self.search_attribute('508')

        ###   Na jutro: Pliki w folderze ATTRIBUTES te?? powinny generowa?? si?? w liczbie kopii r??wnej liczbie element??w,
        ###   w przeciwnym razie tworzy si?? tylko jeden plik .txt                                                        ZROBIONE

        # atrybuty z listy np. 1000 * (nr atr) to zmina jednostki, doda?? funkcj                                          ZROBIONE

        # Doda?? przycisk wybierz obszar                                                                                  ZREZYGNOWANO