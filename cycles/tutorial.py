import sys
sys.path.append('D:\Work\BlenderToolbox\cycles') # your path to “BlenderToolbox/cycles”
from include import *
import os
cwd = os.getcwd()

'''
RENDER AN IMAGE STEP-BY-STEP:
1. copy "tutorial.py" to your preferred local folder
2. In "tutorial.py":
    - change meshPath and readPLY/readOBJ
    - comment out the last line "renderImage"
    - set your desired material (select one from the demo scripts)
3. run "blender --background --python tutorial.py" in terminal, this outputs a "test.blend"
4. open "test.blend" with your blender software
5. In blender UI, adjust:
    - location, rotation, scale of the mesh
    - material parameters
6. In "tutorial.py":
    - type in the adjusted parameters from UI 
    - uncomment the last line "renderImage"
    - set outputPath and increase imgRes_x, imgRes_y, numSamples
7. run "blender --background --python tutorial.py" again to output your final image
'''

outputPath = os.path.join(cwd, './results/test-0.png') # make it abs path for windows

## initialize blender
imgRes_x = 640 # recommend > 2000 (UI: Scene > Output > Resolution X)
imgRes_y = 640 # recommend > 2000 (UI: Scene > Output > Resolution Y)
numSamples = 100 # recommend > 200 for paper images (UI: Scene > Render > Sampling > Render)
exposure = 1.5 # exposure of the entire image (UI: Scene > Render > Film > Exposure)
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
# meshPath = '../meshes/spot.ply'
meshPath = "../meshes/user-results/03-20200728173603_1_1_1_strokes.obj"
# lamp transform
location = (-2.3057,
            -0.55909,
            -2.658) # (UI: click mesh > Transform > Location)
rotation = (90, 0, -75) # (UI: click mesh > Transform > Rotation)
scale = (3, 3, 3) # (UI: click mesh > Transform > Scale)

# shoe transform
# location = (-0.12047,
#             2.3203,
#             -3.2956) # (UI: click mesh > Transform > Location)
# rotation = (90, 0, 180) # (UI: click mesh > Transform > Rotation)
# scale = (4,4,4) # (UI: click mesh > Transform > Scale)

# mesh = readPLY(meshPath, location, rotation, scale)
mesh = readOBJ(meshPath, location, rotation, scale) 

# # Set origin
# # store the location of current 3d cursor
# saved_location = bpy.context.scene.cursor.location  # returns a vector

# # give 3dcursor new coordinates
# bpy.context.scene.cursor.location = (0.0,1.0,0.0)

# # set the origin on the current object to the 3dcursor location
# bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# # set 3dcursor location back to the stored location
# bpy.context.scene.cursor.location = saved_location

## set shading (choose one of them)
bpy.ops.object.shade_smooth() # Option1: Gouraud shading
# bpy.ops.object.shade_flat() # Option2: Flat shading
# edgeNormals(mesh, angle = 10) # Option3: Edge normal shading

## subdivision 
subdivision(mesh, level = 2)

###########################################
## Set your material here (see other demo scripts)

# colorObj(RGBA, H, S, V, Bright, Contrast)
# RGBA = (144.0/255, 210.0/255, 236.0/255, 1)
# RGBA = (0.013034, 0.333901, 0.760525, 1)
# meshColor = colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
# setMat_singleColor(mesh, meshColor, AOStrength = 0.5)

bpy.ops.wm.append(filename="StrokeMat", directory="D:/Work/renders/base-scene-cycles.blend\\Material\\")
mat = bpy.data.materials.get("StrokeMat")

# bpy.ops.wm.append(filename="SurfacePatchMat", directory="D:/Work/renders/base-scene-cycles.blend\\Material\\")
# mat = bpy.data.materials.get("SurfacePatchMat")


mesh.data.materials.append(mat)
mesh.active_material = mat

## End material
###########################################

## set invisible plane (shadow catcher)
invisibleGround(location = (0,0,-0.4),shadowBrightness=0.8)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (2,2,2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
cam = setCamera(camLocation, lookAtLocation, focalLength)

## set light
## Option1: Three Point Light System 
# setLight_threePoints(radius=4, height=10, intensity=1700, softness=6, keyLoc='left')
## Option2: simple sun light
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
setLight_ambient(color=(0.1,0.1,0.1,1)) # (UI: Scene > World > Surface > Color)

## set gray shadow to completely white with a threshold (optional)
alphaThreshold = 0.05
shadowThreshold(alphaThreshold, interpolationMode = 'CARDINAL')

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath='./test.blend')

## save rendering
# renderImage(outputPath, cam)