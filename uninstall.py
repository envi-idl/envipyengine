

import sys
import os
import shutil

python_install_dir = os.path.dirname(sys.executable)
envipyengine_package_dir = os.path.join(python_install_dir, 'Lib', 'site-packages', 'envipyengine')
shutil.rmtree(envipy_package_dir)