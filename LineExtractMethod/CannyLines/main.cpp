#include <stdio.h>
#include <fstream>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui.hpp"
#include "CannyLine.h"

using namespace cv;
using namespace std;


int main()
{	
	string in_img = "AM-5-00093.jpg";
	//Mat img = imread("../../TestOpencv/TestOpencv/data/" + in_img);

	double start = double(getTickCount());

	string fileCur("../../data/" + in_img);
	cv::Mat img = imread( fileCur, CV_8UC1);//
	cv::Mat imgRGB = imread(fileCur);

	////Àı∑≈Õº∆¨
	//double scale = 0.5;
	//Size dsize = Size(img.cols * scale, img.rows * scale);
	//resize(img, img, dsize);
	//resize(imgRGB, imgRGB, dsize);

	if(img.empty()) return -1;

	CannyLine detector;
	std::vector<std::vector<float> > lines;
	lines = CannyLine::cannyLine(img);

	// show
	cv::Mat imgShow( img.rows, img.cols, CV_8UC3, cv::Scalar( 255, 255, 255 ) );
	for (auto & m : lines)
	{
		cv::line(imgRGB, cv::Point( m[0], m[1] ), cv::Point( m[2], m[3] ), cv::Scalar(0,0,255), 1);
	}
	cv::imwrite(in_img + ".canny.jpg", imgRGB);
	double duration_ms = (double(getTickCount()) - start) * 1000 / getTickFrequency();
	std::cout << "It took " << duration_ms << " ms." << std::endl;

	return 0;
}