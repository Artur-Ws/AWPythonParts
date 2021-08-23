import os
import tkinter
import shutil
from distutils.dir_util import copy_tree

# sourcePath = "C:\\ProgramData\\Nemetschek\\Allplan\\2021\\Etc\\PythonPartsScripts\\AWPythonParts\\copysource"
sourcePath = "\\ALPLAN\\alplan\\AWPythonPartsCopySource"
targetPath = "C:\\ProgramData\\Nemetschek\\Allplan\\2021\\Etc\\PythonPartsScripts\\AWPythonParts\\aaa"


def check_allplan_version(build_ele, version):
    return True


def create_element(build_ele, doc):
    model_elem_list = []
    handle_list = []
    del build_ele
    del doc

    return (model_elem_list, handle_list)


print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

if not os.path.exists(targetPath):
    os.makedirs(targetPath)

copy_tree(sourcePath, targetPath)

window = tkinter.Tk()
window.title("PBX PP Update")
info = tkinter.Label(window, text='Pomyślnie zaktualizowano PythonPartsy', width=50, height=5)
info.grid(column=0, row=0)
window.mainloop()
