#include <iostream>
#include <string>


#include <opencv2/core/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

int main(int argc, char** argv)
{

    string imgName = "AM-2-00420";      //图片名
    bool if_canny = false;              //是否canny边缘后再直线检测
    double scale_out = 1;               //使用opencv将输入图片缩放
    double scale_in = 0.7;              //lsd算法内置缩放 小了线会更连续,但误差更大 0.8
    int n_refine = LSD_REFINE_NONE;     //0 1 2  LSD_REFINE_NONE LSD_REFINE_STD LSD_REFINE_ADV细化为更小的线,none最好
    double density_th = 0.7;            //最小密度阈值 0.7
    double ang_th = 30;               //角度阈值22.5
    int min_lenth_power2 = 100;          //最小线段长度的平方
    double sigma_scale = 0.6; double quant = 2.0;  double log_eps = 0;


    /*
      LSD_REFINE_NONE，没有改良的方式；
      LSD_REFINE_STD，标准改良方式，将带弧度的线（拱线）拆成多个可以逼近原线段的直线度；
      LSD_REFINE_ADV，进一步改良方式，计算出错误警告数量，通过增加精度，减少尺寸进一步精确直线。
    */

        
    string in = imgName + ".jpg";
    Mat image = imread("../../data/"+in, IMREAD_GRAYSCALE);


    //缩放图片
    int n_cols = image.cols;
    int n_rows = image.rows;
    Size dsize = Size(image.cols * scale_out, image.rows * scale_out);
    cout << "当前cols rows" << n_cols * scale_out << n_rows * scale_out;
    Mat dst;
    
    //是否使用canny算子预处理
    if(if_canny)
    {
        Canny(image, dst, 50, 200, 3); // Apply canny edge
        resize(dst, dst, dsize);
    }
    else
    {
        resize(image, dst, dsize);
    }


    //LSD构建
    Ptr<LineSegmentDetector> ls = createLineSegmentDetector(n_refine, scale_in, sigma_scale,quant,ang_th,log_eps,density_th);


    double start = double(getTickCount());


    // Detect the lines
    /*
    lines_std : A vector of Vec4f elements specifying the beginning and ending point of a line. 
    Where Vec4f is (x1, y1, x2, y2), point 1 is the start, point 2 - end. 
    Returned lines are strictly oriented depending on the gradient.abs(iter[0][1] - iter[2])
    */
    vector<Vec4f> lines_std;

    ls->detect(dst, lines_std);



    double start_for = double(getTickCount());


    int n_lines = lines_std.size();
    int n_lines_reserved = 0;
    int n_lines_abolished = 0;


    ////删除短线段
    //for (vector<Vec4f>::iterator iter = lines_std.begin(); iter != lines_std.end();)
    //{

    //    if (pow((iter[0][0] - iter[0][2]),2) + pow((iter[0][1] - iter[0][3]),2) < min_lenth_power2)
    //    //if (abs(iter[0][0] - iter[0][2])<n_cols*0.03 && abs(iter[0][1] - iter[0][3]) < n_rows * 0.03)
    //    {
    //        //cout <<"已抛弃"<< iter[0][0] << " " << iter[0][1] << " " << iter[0][2] << " " << iter[0][3] << endl;
    //        //cout << "已抛弃" ;
    //        iter = lines_std.erase(iter);
    //        n_lines_abolished++;
    //        continue;
    //    }
    //    else
    //    {
    //        //cout << iter[0][0] << " " << iter[0][1] << " " << iter[0][2] << " " << iter[0][3] << endl;
    //        //cout << "已抛弃";
    //        n_lines_reserved++;
    //        iter++;
    //    }

    //}

    //double end_for = double(getTickCount());
    //cout << "for循环遍历耗时" << (end_for - start_for) * 1000 / getTickFrequency() <<"已抛弃"<<n_lines_abolished<<"已保留"<< n_lines_reserved<< endl;

    double duration_ms = (double(getTickCount()) - start) * 1000 / getTickFrequency();
    std::cout << "It took " << duration_ms << " ms." << std::endl;

    // Show found lines
    Mat imageShow = imread("./data/" + in);
    resize(imageShow, imageShow, dsize);
    Mat drawnLines(imageShow);
    ls->drawSegments(drawnLines, lines_std);

    //保存图片命名
    string out = "./result/" +imgName 
        + "_LSD"
        + "_scale"+ to_string(scale_out).substr(0, 3) + "_"+ to_string(scale_in).substr(0, 3)
        + "_density_th" + to_string(density_th).substr(0, 4)
        + "_ang_th" + to_string(ang_th).substr(0, 4)
        + "_min_lenth" + to_string(sqrt(min_lenth_power2)).substr(0, 3)
        + "_ms" + to_string(duration_ms).substr(0, 8) 
        + "_ifcanny" + to_string(if_canny)
        + "_refine" + to_string(n_refine)
        + ".jpg";
    imwrite(out, drawnLines);

    //namedWindow("LSD", 0);

    //resizeWindow("LSD", 640, 480);

    //imshow("LSD", drawnLines);

    //waitKey();
    return 0;
}
