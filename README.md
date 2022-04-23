# 基于无人机倾斜影像的地物线特征提取
本科毕业设计相关实现代码
部分源自OpenCV、Trimesh库官方示例

## 运行环境
三种线提取算法(C++):
OpenCV 4.55
VS 2019

主体python程序：
```
pip install -r requirements.txt
```

Blender脚本：
Blender 3.0.1


## 目录说明
│  BlenderScript.py 	#Blender模型优化脚本
│  getCornerPoints.py 	#角点计算
│  main.py 				#python主程序
│  opencvLSD.py 		#区域LSD，鼠标交互选择线段
│  rotateToMesh.py 		#二维点至三维线投影
│  xmlParse.py 			#获取xml文件中内外方元素信息
├─data					#实验数据
└─LineExtractMethod 	#三种线提取算法(C++版)
