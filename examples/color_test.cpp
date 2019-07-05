#include <iostream>
#include <string>
#include <cstring>

using namespace std;

int sign(double v) {
    return (v > 0) - (v < 0);
}

double get_color_val(double dv, double min_diff, int index, double * pts, double * color_arr) {
    int color_range_sign = sign(color_arr[index+1] - color_arr[index]);
    double pt_range = pts[index+1] - pts[index];
    double color_val = color_arr[index] + color_range_sign * (min_diff - pts[index] * dv) / (pt_range * dv);
    return color_val;
}

void get_color_in_scale(double v, double vmin, double vmax, const char * scale) {
    int pointCount = 5;
    double *pts, *Rs, *Gs, *Bs;
    if (!strcmp(scale, "Rainbow")) {
        pts = new double[5] {0, 0.25, 0.5, 0.75, 1};
        Rs = new double[5] {0, 0, 0, 1, 1};
        Gs = new double[5] {0, 1, 1, 1, 0};
        Bs = new double[5] {1, 1, 0, 0, 0};
    } else if (!strcmp(scale, "GreyRainbow")) {
        pointCount = 6;
        pts = new double[6] {0, 0.005, 0.25, 0.5, 0.75, 1};
        Rs = new double[6] {1, 1, 0, 0, 1, 1};
        Gs = new double[6] {1, 1, 1, 1, 1, 0};
        Bs = new double[6] {1, 1, 1, 0, 0, 0};
    } else if (!strcmp(scale, "RainbowInv")) {
        pts = new double[5] {0, 0.25, 0.5, 0.75, 1};
        Rs = new double[5] {1, 1, 0, 0, 0};
        Gs = new double[5] {0, 1, 1, 1, 0};
        Bs = new double[5] {0, 0, 0, 1, 1};
    } else if (!strcmp(scale, "SeisSol")) {
        pts = new double[5] {0, 0.25, 0.5, 0.75, 1};
        Rs = new double[5] {1, 0, 0, 1, 1};
        Gs = new double[5] {1, 1, 0, 0.317647, 0};
        Bs = new double[5] {1, 1, 1, 0, 0};
    } else if (!strcmp(scale, "Kaikoura")) {
        pointCount = 3;
        pts = new double[3] {0, 0.01, 1};
        Rs = new double[3] {1, 92.0 / 255, 196.0 / 255};
        Gs = new double[3] {1, 190.0 / 255, 119.0 / 255};
        Bs = new double[3] {1, 215.0 / 255, 87.0 / 255};
    } else {
        pointCount = 3;
        pts = new double[3] {0, 0.5, 1};
        Rs = new double[3] {58.0 / 256, 221.0 / 256, 180.0 / 256};
        Gs = new double[3] {76.0 / 256, 222.0 / 256, 4.0 / 256};
        Bs = new double[3] {193.0 / 256, 222.0 / 256, 38.0 / 256};
    }
    
    if (v < vmin) v = vmin;
    if (v > vmax) v = vmax;
    double  min_diff = v - vmin,
            dv = vmax - vmin;
    
    int i;
    for (i = pointCount - 2; i >= 0; i--) {
        if (min_diff / dv >= pts[i])
            break;
    }
    
    cout << ((get_color_val(dv, min_diff, i, pts, Rs) * 255)) << endl;
    cout << (static_cast<int> (get_color_val(dv, min_diff, i, pts, Gs) * 255)) << endl;
    cout << (static_cast<int> (get_color_val(dv, min_diff, i, pts, Bs) * 255)) << endl;
    
    delete[] pts;
    delete[] Rs;
    delete[] Gs;
    delete[] Bs;
}

int main() {
    string scale("Rainbow");
    get_color_in_scale(0.65, 0, 1, scale.c_str());
    return 0;
}
