import  cv2
import numpy as np

def getCornerPoints(lineList):
    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    # print line_intersection((A, B), (C, D))


    points = []
    lines = []
    cornerPoints = [[]]
    faceNo = 0
    for face in lineList:
        for i in face:
            if i == 0:
                # print(points)
                pointsOneLine = np.array(points, dtype=np.float32)
                # 直线拟合
                line = cv2.fitLine(pointsOneLine,cv2.DIST_L2,0,0.01,0.01)
                lines.append(line)
                # print(c)
                points = []
                pass
            else:
                points.append((i[0:2]))
                points.append((i[2:4]))

        print(lines)
        for i in range(len(lines)):

            A = [lines[i-1][2],lines[i-1][3]]
            B = [lines[i-1][2]+lines[i-1][0]*100,lines[i-1][3]+lines[i-1][1]*100]
            C = [lines[i][2],lines[i][3]]
            D = [lines[i][2]+lines[i][0]*100,lines[i][3]+lines[i][1]*100]
            # print(A,B,C,D)

            # 直线求交
            xC,yC = line_intersection((A,B),(C,D))
            cornerPoints[faceNo].append((xC[0],yC[0]))
        faceNo += 1
        cornerPoints.append([])
        points = []
        lines = []
    return cornerPoints

if __name__ == "__main__":
        print(getCornerPoints(0))


        # A = Point([lines[i-1][2],lines[i-1][3]])
        # B = Point([lines[i-1][2]+lines[i-1][0]*100,lines[i-1][3]+lines[i-1][1]*100])
        # C = Point([lines[i][2],lines[i][3]])
        # D = Point([lines[i][2]+lines[i][0]*100,lines[i][3]+lines[i][1]*100])


        # line1 = LineString([A, B])
        # line2 = LineString([C, D])
        # print(line1)
        #
        #
        # int_pt = line1.intersection(line2)
        # # point_of_intersection = int_pt.x, int_pt.y
        # #
        # print(int_pt)


    # points = (5,10,11,22)
    # points = [5,10,11,22]
    # print(points[0:2],points[2:4])
    # test = (points[0:1],points[2:3])
    # b1 = np.array(test,dtype=np.float32)
    # b = [[5,9],[11,18],[20,32]]
    # c = cv2.fitLine(b1,cv2.DIST_L2,0,0.01,0.01)
    # print(c)

# 测试数据：
    # a = [[4350.383743286133, 2605.9614219665527, 4217.456787109375, 2647.081214904785], 0,
    #      [4582.319396972656, 2894.8636169433594, 4429.08203125, 2653.7434310913086], 0,
    #      [4559.421783447266, 2903.114227294922, 4581.328552246094, 2896.2272033691406], [4403.308837890625, 2952.2952880859375, 4557.566650390625, 2903.6897583007812], 0,
    #      [4287.9671630859375, 2765.6746978759766, 4261.759468078613, 2722.3921966552734], [4324.758285522461, 2825.8448944091797, 4303.467666625977, 2790.3694610595703], [4400.386276245117, 2952.480438232422, 4381.164260864258, 2917.7416076660156], 0]


    # lineList= [[[4337.739196777344, 2609.797836303711, 4217.318023681641, 2647.1914978027344], 0,
    #      [4427.6361083984375, 2651.4232330322266, 4391.765533447266, 2594.4715576171875], 0,
    #      [4559.2913818359375, 2903.2171020507812, 4581.164794921875, 2896.249969482422], [4403.943206787109, 2952.133819580078, 4557.407196044922, 2903.72705078125], 0,
    #      [4400.616302490234, 2953.2186889648438, 4381.006134033203, 2917.440155029297], [4324.7403564453125, 2825.710968017578, 4303.2435302734375, 2790.1053161621094], [4287.949600219727, 2765.7779846191406, 4261.573440551758, 2722.1041717529297], 0],
    #     [[4398.495208740234, 2998.502166748047, 4402.700164794922, 2951.2652282714844], 0,
    #      [4403.943206787109, 2952.133819580078, 4557.407196044922, 2903.72705078125], 0,
    #      [4553.914459228516, 2948.3355712890625, 4559.490386962891, 2905.747314453125], 0,
    #      [4509.253814697266, 2990.3819580078125, 4545.353302001953, 2960.2019653320312], [4465.688720703125, 3022.33740234375, 4488.425231933594, 3007.0773315429688], 0,
    #      [4449.670013427734, 3029.009521484375, 4467.361755371094, 3024.8191528320312], [4421.997467041016, 3037.549072265625, 4444.374053955078, 3029.6973266601562], 0],[]]