import sys
from cx_Freeze import setup, Executable
import os  #, distutils, opcode

sys.setrecursionlimit(12000)  # get rid of recursion limit error
#print(sys.getrecursionlimit())

packages = ['pkg_resources', 'scipy'] #,"PyQt5.QtWidgets","PyQt5.QtGui","PyQt5.QtCore"]
includefiles = {
    os.path.join(sys.base_prefix, 'Library', 'bin', 'sqlite3.dll'),
    #            os.path.join(sys.base_prefix, 'Library', 'bin', 'mkl_intel_thread.dll'),
    #            os.path.join(sys.base_prefix, 'Library', 'bin', 'mkl_core.dll'),
    #            os.path.join(sys.base_prefix, 'Library', 'bin', 'mkl_def.dll'),
  #  os.path.join(sys.base_prefix, 'Library', 'plugins/platforms'),
#    os.path.join(sys.base_prefix, 'Library', 'bin', 'tcl86t.dll'),
#    os.path.join(sys.base_prefix, 'Library', 'bin', 'tk86t.dll'),
#    os.path.join(sys.base_prefix, 'Library', 'bin', 'libffi-7.dll'),
    "cute_gui_r1.ui", "CUTE2.ico", "CUTE2.png", "add-file-48.ico"
    , "close-window-48.ico", "folder-48.ico", "save-48.ico", "save-as-48.ico"    
}
excludes = ['scipy.spatial.cKDTree']

print(sys.base_prefix)
exe = Executable(
    script='main_prog.py',
    targetName='DayCent-CUTE.exe',
    base="Win32GUI"
    )

options ={
    'build_exe': {
        'packages': packages,
        'include_files': includefiles,
        'excludes': excludes,
        'build_exe': './/build'
    }
}

setup(
    name='DayCent-CUTE.exe',
    options=options,
    version='1.0',
    description='DayCent-CUTE',
    executables=[exe]
    )
