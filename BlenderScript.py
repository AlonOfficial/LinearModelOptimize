import mathutils
import bpy
from bpy import context
import numpy as np


cornerPoints=np.load('F:/CodeProj/4down/py_trimesh/finalPointsOnMesh.npy',allow_pickle=True)
cornerPoints=cornerPoints.tolist()


# exec script in modelView area
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        ctx = bpy.context.copy()
        ctx['area'] = area
        ctx['region'] = area.regions[-1]
        
        obj = context.object
        mesh = obj.data
        size = len(mesh.vertices)

        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # k-d tree build
        kd = mathutils.kdtree.KDTree(size)

        for i, v in enumerate(mesh.vertices):
            kd.insert(v.co, i)

        kd.balance()
        

        indexList = []
        faceNo = 0
        
        # neighbor vertex index search
        for pointsOneFace in cornerPoints:
            indexList.append([])
            for points in pointsOneFace:
                co, index, dist = kd.find(points)
                indexList[faceNo].append(index)
            faceNo += 1
            
        print(indexList)
            
        faceNo = 0
        edges_ind = []
        for pointsOneFace in indexList:
            edges_ind.append([])
            for i in range(len(pointsOneFace)):
                # select 2 points and the shortest_path between
                bpy.ops.object.mode_set(mode = 'OBJECT')
                mesh.vertices[ indexList[faceNo][i-1] ].select = True
                mesh.vertices[ indexList[faceNo][i] ].select = True
                
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bpy.ops.mesh.shortest_path_select(edge_mode='SELECT')
                
                # get edge index in shortest_path
                bpy.ops.object.mode_set(mode = 'OBJECT')
                edges_ind[faceNo] += [i.index for i in bpy.context.object.data.edges if i.select]
                bpy.ops.object.mode_set(mode = 'EDIT') 
                
                # straighten the shortest_path
                bpy.ops.mesh.looptools_gstretch(conversion='limit_vertices', conversion_distance=0.1, conversion_max=32, conversion_min=8, conversion_vertices=32, delete_strokes=False, influence=100, lock_x=False, lock_y=False, lock_z=False, method='regular')
                bpy.ops.mesh.select_all(action = 'DESELECT')
#                bpy.ops.mesh.shortest_path_pick(ctx, edge_mode='SELECT', use_fill=False, index=indexList[faceNo][i])
#                bpy.ops.mesh.looptools_gstretch(conversion='limit_vertices', conversion_distance=0.1, conversion_max=32, conversion_min=8, conversion_vertices=32, delete_strokes=False, influence=100, lock_x=False, lock_y=False, lock_z=False, method='regular')
            faceNo += 1
        print(edges_ind)
        

        bpy.ops.mesh.select_mode(type="EDGE")
        # select all edges of one face
        for face in edges_ind:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            for edge in face:
                mesh.edges[ edge ].select = True
            
            bpy.ops.object.mode_set(mode = 'EDIT') 
            bpy.ops.mesh.loop_to_region() # select vertex inside
            # flatten the area
            bpy.ops.mesh.looptools_flatten(influence=100, lock_x=False, lock_y=False, lock_z=False, plane='best_fit', restriction='none')


            bpy.ops.mesh.select_all(action = 'DESELECT')