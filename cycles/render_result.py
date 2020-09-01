import sys
sys.path.append('D:\Work\BlenderToolbox\cycles') # your path to “BlenderToolbox/cycles”
from include import *
import os
cwd = os.getcwd()

def render_strokes(file_path, output_label, is_lamp = True, resolution = 640):
    file_name = output_label + '.png'
    outputPath = os.path.join(cwd, './results/study_results', file_name) # make it abs path for windows

    ## initialize blender
    imgRes_x = resolution # recommend > 2000 (UI: Scene > Output > Resolution X)
    imgRes_y = resolution # recommend > 2000 (UI: Scene > Output > Resolution Y)
    numSamples = 100 # recommend > 200 for paper images (UI: Scene > Render > Sampling > Render)
    exposure = 1.5 # exposure of the entire image (UI: Scene > Render > Film > Exposure)
    blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    ## read mesh (choose either readPLY or readOBJ)
    # meshPath = '../meshes/spot.ply'
    meshPath = file_path
    if is_lamp:
        # lamp transform
        location = (-2.19284,
                    -0.823859,
                    -2.50489) # (UI: click mesh > Transform > Location)
        rotation = (90, 0, -75) # (UI: click mesh > Transform > Rotation)
        scale = (2.8,2.8,2.8) # (UI: click mesh > Transform > Scale)
    else:
        # shoe transform
        location = (-0.12047,
                    2.3203,
                    -3.2956) # (UI: click mesh > Transform > Location)
        rotation = (90, 0, 180) # (UI: click mesh > Transform > Rotation)
        scale = (4,4,4) # (UI: click mesh > Transform > Scale)
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
    # bpy.ops.wm.save_mainfile(filepath='./test.blend')

    # save rendering
    renderImage(outputPath, cam)