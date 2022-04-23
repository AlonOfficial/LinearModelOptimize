from opencvLSD import roiLsd
from xmlParse import xmlParse
from getCornerPoints import getCornerPoints
from rotateToMesh import rotateToMesh
import numpy as np


imgName ='AM-5-00324'
# imgName = 'AM-3-00325'

# 区域直线检测，鼠标点选目标线
# 左键点选线条，右键结束单条边缘选择，中键结束当前平面选择
lineList = roiLsd(imgName)# roiLsd函数中包含文件夹路径

if lineList !=[[]]:
    print('Main lineList',lineList)

    # 直线拟合，角点计算
    cornerPoints = getCornerPoints(lineList)
    print('Main cornerPoints:',cornerPoints)

    # 读取xml文件中对应影像内外方元素
    # xmlInfo = [XImageCenter, YImageCenter, FocalLength, omega, phi, kappa, XCamera, YCamera, ZCamera]
    xmlInfo = xmlParse(imgName)

    # 二维点至三维模型投影
    finalPointsOnMesh = rotateToMesh(cornerPoints, xmlInfo)# rotateToMesh中包含mesh文件路径
    print('Main finalPointsOnMesh:',finalPointsOnMesh)

    # 保存三维点数据到文件
    finalPointsOnMesh=np.array(finalPointsOnMesh)
    np.save(imgName+'finalPointsOnMesh.npy',finalPointsOnMesh)   # 保存为.npy格式

print('ok')

# print(xmlInfo)



