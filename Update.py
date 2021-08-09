import os
<<<<<<< HEAD
import tkinter
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

sourcePath = "\\ALPLAN\\alplan\\AWPythonPartsCopySource"
targetPath = "C:\ProgramData\Nemetschek\Allplan\2021\Etc\PythonPartsScripts\ToolsAndStartExamples"

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

class Update:

    def __init__(self, sourcePath, targetPath):
        self.sourcePath = sourcePath
        self.targetPath = targetPath

    def checkDirectory(self):
        '''Cheks wheter target directory exists, if not creates it'''

        if not os.path.exists(self.targetPath):
            os.makedirs(self.targetPath)

    def copyFiles(self):

        self.checkDirectory()
=======

sourcePath = "\\ALPLAN\\alplan\\AWPythonPartsCopySource"
targetPath = "C:\\ProgramData\\Nemetschek\\Allplan\\2021\\Etc\\PythonPartsScripts\\ToolsAndStartExamples"
class UpdatePP:
    def __init__(self):
        pass

    def searchSourcePath(self):
        pass

    def copyFiles(self):

        for item in os.listdir()


>>>>>>> 40a000a6c6b872bd0acf0f47a4d35311b5463fb8

        window = tkinter.Tk()
        window.title("PBX PP Update")
        info = tkinter.Label(window, text='Pomyślnie zaktualizowano PythonPartsy')
        info.grid(column=0, row=0)
        window.mainloop()

<<<<<<< HEAD
Update.copyFiles()
=======
>>>>>>> 40a000a6c6b872bd0acf0f47a4d35311b5463fb8
