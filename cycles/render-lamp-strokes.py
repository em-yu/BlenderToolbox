import sys
sys.path.append('D:\Work\BlenderToolbox\cycles') # your path to “BlenderToolbox/cycles”
from include import *
import os
import re
from render_result import render_strokes
cwd = os.getcwd()

# Load all lamp stroke-only results and render them
files_to_render = []

root_folder = 'C:/Users/Emilie/Desktop/User results to render'

for r,d,f in os.walk(root_folder):
    for file in f:
        is_lamp = False
        if re.search(r'\d*-\d*_1_[01]_1_strokes.obj$', file) is not None:
            # it is a lamp
            is_lamp = True
        elif re.search(r'\d*-\d*_1_[01]_3_strokes.obj$', file) is not None:
            # it is a shoe
            is_lamp = False
        else:
            continue
        
        user_id = re.search(r'^\d{2}', file).group()
        system_id = re.search(r'[012](?=_\d_strokes.obj$)', file).group()
        model = "lamp" if is_lamp else "shoe"
        label = "{}-{}-{}".format(user_id, system_id, model)
        print("Rendering " + label)

        # Render
        file_path = os.path.join(root_folder, file)
        render_strokes(file_path, label, is_lamp, resolution = 640)

