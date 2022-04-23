'''
已实现mesh映射
'''


from scipy.spatial.transform import Rotation as R
import trimesh
import numpy as np
import time

# import random
# from transforms3d.euler import euler2mat, mat2euler
# import math



def rotateToMesh(cornerPoints,xmlInfo):
    mesh = trimesh.load('./data/Tile_+2887_+070.obj')
    # mesh = trimesh.load('./objTile/Tile_+2889_+067.obj')

    # 坐标系原点坐标
    XOrigin, YOrigin = 443367, 2450668


    # 获取xml内信息
    XImageCenter, YImageCenter, FocalLength, omega, phi, kappa, XCamera, YCamera, ZCamera = xmlInfo


    XCamera = XCamera - XOrigin
    YCamera = YCamera - YOrigin

    # 相机三维空间坐标（射线起点）
    ray_origins = np.array([[XCamera, YCamera, ZCamera]])


    # 旋转矩阵
    R1 = R.from_euler('XYZ', [omega, phi, kappa], degrees=True).as_matrix()
    # R2 = euler2mat(math.radians(omega), math.radians(phi), math.radians(kappa), 'rxyz')


    print(R1)
    # print(R2)
    
    locations = []

    shrinkDirect = [0,0]

    finalPointsOnMesh = []
    for cornerOneFace in cornerPoints:
        if cornerOneFace != []:
            # 计算平面中心
            x = [p[0] for p in cornerOneFace]
            y = [p[1] for p in cornerOneFace]
            centPt = (sum(x) / len(cornerOneFace), sum(y) / len(cornerOneFace))

            for p in cornerOneFace:
                print('new Point')
                locationOneLine = []
                for i in range(10):
                    # norm = cv2.norm(centPt, p)
                    norm = ((centPt[0] - p[0]) ** 2 + (centPt[1] - p[1]) ** 2) ** 0.5
                    # 计算射线收缩方向单位向量
                    shrinkDirect[0] = (centPt[0] - p[0]) / norm
                    shrinkDirect[1] = (centPt[1] - p[1]) / norm

                    # 获得向中心收缩1像素后的二维像素
                    xImage = p[0] + shrinkDirect[0] * i
                    yImage = p[1] + shrinkDirect[1] * i

                    # 三维像空间坐标
                    XImage = (xImage - XImageCenter) * 23.5 / 6000
                    YImage = (yImage - YImageCenter) * 23.5 / 6000  # !!一开始写错成了/4000
                    xyzImage = np.array([[XImage], [YImage], [FocalLength]])

                    # 获得射线方向向量（注意*15决定了射线长度）
                    ray_directions1 = np.matmul(R1, xyzImage).reshape(1, 3) * 15
                    # ray_directions2 = np.matmul(R2, xyzImage).reshape(1, 3) * 11

                    # print(ray_directions1)
                    # # print(ray_directions2)

                    # listRay = []

                    # 测试旋转角组合
                    #
                    # # for i in [omega,-omega,180+omega,180-omega,omega+90,-omega+90,180+omega+90,180-omega+90]:
                    # #     for j in [phi, -phi, 180 + phi, 180 - phi,phi+90, -phi+90, 180 + phi+90, 180 - phi+90]:
                    # #         for k in [kappa, -kappa, 180 + kappa, 180 - kappa,kappa+90, -kappa+90, 180 + kappa+90, 180 - kappa+90]:
                    # for i in [omega, -omega, 180 + omega, 180 - omega]:
                    #     for j in [phi, -phi, 180 + phi, 180 - phi]:
                    #         for k in [kappa, -kappa, 180 + kappa, 180 - kappa]:
                    #             for mode in ['sxyz','sxzy','syxz','syzx','szxy','szyx','rxyz','rxzy','ryxz','ryzx','rzxy','rzyx']:
                    #                 print(aa)
                    #                 aa+=1
                    #                 R2 = euler2mat(math.radians(i), math.radians(j), math.radians(k), mode)
                    #                 ray_directions2 = np.matmul(R2, xyzImage).reshape(1, 3) * 11
                    #                 ray_origin_back = ray_origins-ray_directions2
                    #                 ray_directions2 *= 2
                    #                 locationPoint, index_ray, index_tri = mesh.ray.intersects_location(ray_origins=ray_origin_back,ray_directions=ray_directions2,multiple_hits=False)
                    #
                    #
                    #                 # exit(0)
                    #
                    #                 if locationPoint.shape[0]!=0:
                    #
                    #                     print('有交点',i,j,k,mode)
                    #
                    #                     # stack rays into line segments for visualization as Path3D
                    #                     ray_visualize = trimesh.load_path(np.hstack((
                    #                         ray_origin_back,
                    #                         ray_origins + ray_directions2)).reshape(-1, 2, 3))
                    #                     listRay.append(ray_visualize)
                    #                     # # create a visualization scene with rays, hits, and mesh
                    #                     # scene = trimesh.Scene([
                    #                     #     mesh,
                    #                     #     ray_visualize,
                    #                     #     trimesh.points.PointCloud(locationPoint)])
                    #                     # scene = trimesh.Scene([
                    #                     #     mesh,
                    #                     #     ray_visualize])
                    #                     # # display the scene
                    #                     # scene.show()
                    #
                    # # make mesh transparent- ish
                    # mesh.visual.face_colors = [100, 100, 100, 100]
                    # scene = trimesh.Scene([
                    #     mesh,
                    #     listRay])
                    # # display the scene
                    # scene.show()
                    #

                    # 相交计算
                    start = time.perf_counter()
                    locationPoint, index_ray, index_tri = mesh.ray.intersects_location(ray_origins=ray_origins,
                                                                                       ray_directions=ray_directions1,
                                                                                       multiple_hits=False)
                    end = time.perf_counter()
                    timecost = end - start
                    locationOneLine.append(locationPoint.tolist()[0])

                    # print('mesh交点', locationPoint)

                    # 场景可视化代码
                    # # make mesh transparent- ish
                    # mesh.visual.face_colors = [100, 100, 100, 100]
                    #
                    # # stack rays into line segments for visualization as Path3D
                    # ray_visualize = trimesh.load_path(np.hstack((
                    #     ray_origins - ray_directions2,
                    #     ray_origins + ray_directions2)).reshape(-1, 2, 3))
                    #
                    # # # create a visualization scene with rays, hits, and mesh
                    # # scene = trimesh.Scene([
                    # #     mesh,
                    # #     ray_visualize,
                    # #     trimesh.points.PointCloud(locationPoint)])
                    # scene = trimesh.Scene([
                    #     mesh,
                    #     ray_visualize])
                    #
                    # # display the scene
                    # scene.show()

                # 判断收缩过程中是否发生高程突变，将突变点视作交点，否则选取第一点为交点
                for i in range(len(locationOneLine) - 1):
                    if abs(locationOneLine[i + 1][2] - locationOneLine[i][2]) > 0.3:
                        locations.append(locationOneLine[i + 1])
                        break
                    if i == len(locationOneLine) - 2:
                        locations.append(locationOneLine[0])

            print(locations)
            finalPointsOnMesh.append(locations)
            locations = []



    return finalPointsOnMesh



if __name__ == "__main__":
    # 函数测试数据
    xmlInfo=[2931.7862098435, 1986.92663388199, 35.3847466752216, -179.924417169181, -45.5113598243199, -86.0587861367522,
     451886.395581761, 2457263.57253971, 254.389484034851]
    # cornerPoints = [(4216.0703, 2647.4604), (4390.817, 2593.5005), (4582.843, 2895.731), (4402.1797, 2952.6553)]
    cornerPoints =  [[(4216.6367, 2647.4028), (4391.01, 2593.2703), (4581.7744, 2896.0767), (4401.439, 2952.917)], [(4394.3726, 3044.7607), (4402.585, 2952.5535), (4559.845, 2902.9526), (4553.0674, 2954.9802), (4463.734, 3025.2358)], []]
    print(rotateToMesh(cornerPoints,xmlInfo))
