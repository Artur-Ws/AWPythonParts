import os
import tkinter
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements

#sourcePath = "\\ALPLAN\\alplan\\AWPythonPartsCopySource"
sourcePath = "C:\\ProgramData\\Nemetschek\\Allplan\\2021\\Etc\\PythonPartsScripts\\AWPythonParts"
targetPath = "C:\\ProgramData\\Nemetschek\\Allplan\\2021\\Etc\\PythonPartsScripts\\AWPythonParts\\aaa"

def check_allplan_version(build_ele, version):

    return True

def create_element(build_ele, doc):

    del build_ele
    del doc

    return (list(), list())

print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

window = tkinter.Tk()
window.title("PBX PP Update")
info = tkinter.Label(window, text='Pomyślnie zaktualizowano PythonPartsy')
info.grid(column=0, row=0)
window.mainloop()


# def create_element(build_ele, doc):
#     """
#     Creation of element
#
#     Args:
#         build_ele: the building element.
#         doc:       input document
#
#     Returns:
#             tuple  with created elements, handles and (otional) reinforcement.
#     """
#
#     # Delete unused arguments
#     del doc
#
#     # Access the parameter property from *.pyp file
#     length = build_ele.Length.value
#     width = build_ele.Width.value
#     # Create a 2d line
#     line = AllplanGeo.Line2D(0, width, length, 0)
#     # Define common style properties
#     common_props = AllplanBaseElements.CommonProperties()
#     common_props.GetGlobalProperties()
#     # Create a 2D ModelElement instance and add it to elements list
#     model_elem_list = [AllplanBasisElements.ModelElement2D(common_props, line)]
#     # Define the handles list
#     handle_list = []
#     # Return a tuple with elements list and handles list
#     return (model_elem_list, handle_list)
#
#
# class Update:
#
#     def __init__(self, sourcePath, targetPath):
#         self.sourcePath = sourcePath
#         self.targetPath = targetPath
#
#     def checkDirectory(self):
#         '''Cheks wheter target directory exists, if not creates it'''
#
#         if not os.path.exists(self.targetPath):
#             os.makedirs(self.targetPath)
#
#     def copyFiles(self):
#
#         self.checkDirectory()
#
# sourcePath = "\\ALPLAN\\alplan\\AWPythonPartsCopySource"
# targetPath = "C:\\ProgramData\\Nemetschek\\Allplan\\2021\\Etc\\PythonPartsScripts\\ToolsAndStartExamples"
# class UpdatePP:
#     def __init__(self):
#         pass
#
#     def searchSourcePath(self):
#         pass
#
#     def copyFiles(self):
#         pass
#         #for item in os.listdir()
#
#         window = tkinter.Tk()
#         window.title("PBX PP Update")
#         info = tkinter.Label(window, text='Pomyślnie zaktualizowano PythonPartsy')
#         info.grid(column=0, row=0)
#         window.mainloop()
#
# Update.copyFiles()
# print("111111111111111111111111111111111111111111")
# print(sourcePath)
# print(targetPath)