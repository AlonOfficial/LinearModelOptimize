from xml.dom.minidom import parse
import xml.dom.minidom
import numpy as np


def xmlParse(imgName):
    'name eg. AM-1-00145'

    n_photoGroup = int(imgName[3])

    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("aomen-export.xml")
    root = DOMTree.documentElement

    ## 获取影像组光心和焦距
    photogroup = root.getElementsByTagName('Photogroup')[n_photoGroup - 1]

    # 二维像素坐标
    xImage, yImage = 2792, 3654
    # 三维像空间坐标
    XImageCenter = float(photogroup.getElementsByTagName('x')[0].firstChild.nodeValue)
    YImageCenter = float(photogroup.getElementsByTagName('y')[0].firstChild.nodeValue)
    FocalLength = float(photogroup.getElementsByTagName('FocalLength')[0].firstChild.nodeValue)

    # XImage = (xImage - XImageCenter) * 23.5 / 6000
    # YImage = (yImage - YImageCenter) * 23.5 / 6000 # !!错了,一开始写成了/4000
    # xyzImage = np.array([[XImage], [YImage], [FocalLength]])
    # # i = np.matrix('XImage;YImage')
    # print(xyzImage)

    # 坐标系原点
    XOrigin, YOrigin = 443367, 2450668

    ## 获取单张相片方位元素
    photo = root.getElementsByTagName('Photo')

    for i in photo:
        b2 = i.getElementsByTagName('ImagePath')[0]
        if b2.firstChild.nodeValue == str(n_photoGroup) + '/' + imgName + '.JPG':
            omega = float(i.getElementsByTagName('Omega')[0].firstChild.nodeValue)
            phi = float(i.getElementsByTagName('Phi')[0].firstChild.nodeValue)
            kappa = float(i.getElementsByTagName('Kappa')[0].firstChild.nodeValue)
            print(omega, phi, kappa)

            XCamera = float(i.getElementsByTagName('x')[0].firstChild.nodeValue)
            YCamera = float(i.getElementsByTagName('y')[0].firstChild.nodeValue)
            ZCamera = float(i.getElementsByTagName('z')[0].firstChild.nodeValue)
            print(XCamera, YCamera, ZCamera)
            print('get xml info success')

            return [XImageCenter, YImageCenter, FocalLength, omega, phi, kappa, XCamera, YCamera, ZCamera]
