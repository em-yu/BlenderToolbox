import sys
sys.path.append('/home/hsuehtil/Dropbox/BlenderToolbox/cycles')
from include import *
import bpy

outputPath = './results/demo_monotone.png'

# # init blender
imgRes_x = 1000 # should set to > 2000 for paper figures
imgRes_y = 1000 # should set to > 2000 for paper figures
numSamples = 100 # should set to >1000 for high quality paper images
exposure = 1.5
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# # read mesh 
meshPath = '../meshes/spot.ply'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
mesh = readPLY(meshPath, location, rotation, scale)

# # set shading
bpy.ops.object.shade_smooth()
# bpy.ops.object.shade_flat()

# # subdivision
level = 2
subdivision(mesh, level)

# # set material (option1: render mesh with edges)
colorPos = (0.05, 0.4) # the "size" of each discrete color (0~1), the "len(colorPos)+1" is the number of discrete colors
colorPosMidPercent = (0.9, 0.5) # (0~1) control the smooth of the transition between colors (the smaller the smoother)
colorDarkness = (0.7, 0.45, 0.25) # darkness if each discrete color, len(colorDark) = len(colorPos) + 1
saturation = 1.5
brightness = 1.0
shadowSize = 0.4
meshColor = coralRed
setMat_monotone(mesh, meshColor, saturation, brightness,shadowSize, colorPos, colorPosMidPercent, colorDarkness)

# # set invisible plane (shadow catcher)
groundCenter = (0,0,0)
shadowDarkeness = 0.7
groundSize = 20
invisibleGround(groundCenter, groundSize, shadowDarkeness)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.2,0.2,0.2,1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # # save rendering
bpy.data.scenes['Scene'].render.filepath = outputPath
bpy.data.scenes['Scene'].camera = cam
bpy.ops.render.render(write_still = True)