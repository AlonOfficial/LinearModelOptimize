import cv2
import numpy as np




def roiLsd(imgName):
    # imgName = "AM-3-00166"  # 图片名
    # Read gray image
    imgSource = cv2.imread('./data/' + imgName + ".jpg", 0)


    # 鼠标框选roi
    cv2.namedWindow('roi', cv2.WINDOW_KEEPRATIO)
    roiRegion = cv2.selectROI('roi', imgSource, False, False)
    print(roiRegion)
    img = imgSource[int(roiRegion[1]):int(roiRegion[1] + roiRegion[3]), int(roiRegion[0]):int(roiRegion[0] + roiRegion[2])]

    # cv2.imshow("imageROI",img)
    # cv2.waitKey(0)

    # lsd参数
    scale_in = 0.9 # lsd算法内置缩放 小了线会更连续,但误差更大 0.8
    n_refine = 0  # 0 1 2  LSD_REFINE_NONE LSD_REFINE_STD LSD_REFINE_ADV细化为更小的线,none最好
    density_th = 0.7  # 最小密度阈值 0.7
    ang_th = 17.5  # 角度阈值22.5
    min_lenth_power2 = 400  # 最小线段长度的平方
    sigma_scale = 0.6
    quant = 2.0
    log_eps = 0

    # Create default parametrization LSD
    lsd = cv2.createLineSegmentDetector(refine=n_refine ,scale=scale_in, ang_th=ang_th, density_th=density_th)

    # Detect lines in the image
    lines = lsd.detect(img)[0]  # Position 0 of the returned tuple are the detected lines

    # Draw detected lines in the image
    # drawn_img = lsd.drawSegments(img,lines)


    cvImg = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")
    cv2.cvtColor(img, cv2.COLOR_GRAY2RGB, cvImg)
    # vis2 = np.CreateMat(img.rows, img.cols, np.CV_8UC3)

    # 长度筛选
    lines = [x for x in lines if (x[0][0] - x[0][2]) ** 2 + (x[0][1] - x[0][3]) ** 2 > min_lenth_power2]

    # lines.shape[0]
    # g, b, lineNo = 0, 0, 0

    # 绘制结果图，不同线条分别设色
    for i in range(len(lines)):
        dline = lines[i]
        # x0, y0, x1, y1 = dline.flatten()
        # cv2.line(img, (x0, y0), (x1, y1), 255, 1, cv2.LINE_AA)
        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        # g = i%255
        # b = int(i/255)
        cv2.line(cvImg, (x0, y0), (x1, y1), (255, i % 255, int(i / 255)), 2, cv2.LINE_8)  # LINE_AA LINE_8
        # cv2.line(cvImg, (x0, y0), (x1, y1), (0, 0, 255), 2, cv2.LINE_8)  # LINE_AA LINE_8

    print(len(lines))

    # Show image
    # 窗口大小模式：WINDOW_KEEPRATIO WINDOW_FREERATIO WINDOW_FULLSCREEN WINDOW_AUTOSIZE WINDOW_NORMAL
    cv2.namedWindow('Roi LSD', cv2.WINDOW_NORMAL)
    cv2.imshow('Roi LSD', cvImg)

    global faceNo
    faceNo = 0
    # 鼠标返回rgb来判断线条索引
    lineList = [[]]
    def mouseRGB(event, x, y, flags, param):
        global faceNo
        if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
            colorsB = cvImg[y, x, 0]
            colorsG = cvImg[y, x, 1]
            colorsR = cvImg[y, x, 2]
            colors = cvImg[y, x]
            # print("Red: ", colorsR)
            # print("Green: ", colorsG)
            # print("Blue: ", colorsB)

            if colorsB == 255:
                print('PickSuccess!')
                print("BRG Format: ", colors)
                # print("Coordinates of pixel: X: ", x, "Y: ", y)
                lineNo = colorsG + 255 * colorsR
                # print(lines[lineNo])
                lineTemp = [lines[lineNo][0][0]+roiRegion[0],lines[lineNo][0][1]+roiRegion[1],lines[lineNo][0][2]+roiRegion[0],lines[lineNo][0][3]+roiRegion[1]]
                # print(lineTemp)
                lineList[faceNo].append(lineTemp)
            else:
                print('=======================ERROR: please click again!=======================')
        if event == cv2.EVENT_RBUTTONDOWN:
            lineList[faceNo].append(0)
            print('Select Next Line')

        if event == cv2.EVENT_MBUTTONDOWN:
            faceNo += 1
            lineList.append([])
            print('Select Next Line On Next Face')

    param = roiRegion
    cv2.setMouseCallback('Roi LSD', mouseRGB,param)


    cv2.waitKey(0)
    return lineList
