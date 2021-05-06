#include <stdio.h>
#include "average.h"


int main() {
    double arr[] = {1.0, 2.0, 3.0, 4.0};
    double arr2[] = {-1.0, 0.0, -0.5, 1.0, 1.0, 0.0, 0.25};

    double result = average(4, arr);
    double result2 = average(7, arr2);

    printf("The average of 1, 2, 3 and 4 is: %.4f\n", result);
    printf("The average of the second dataset is: %.4f\n", result2);
    return 0;    
}

