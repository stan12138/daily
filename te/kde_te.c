#include <stdlib.h>
#include <math.h>

void kde_count(double (*record) [3], double (*p) [4], int times, double r, int out_length)
{
	double one_max;
	double sum_xn1xnyn;
	double sum_xn;
	double sum_xnyn;
	double sum_xn1xn;
	for(int i=0; i<times; i++)
	{
		sum_xn1xnyn = 0;
		sum_xnyn = 0;
		sum_xn = 0;
		sum_xn1xn = 0;
		for(int j=0; j<times; j++)
		{
			if(abs(j-i)>out_length)
			{
				one_max = -1000;
				double x[3];
				for(int t=0; t<3; t++)
				{
					x[t] = fabs(record[j][t]-record[i][t]);
					if(x[t]>one_max) one_max=x[t];
				}
				if(r-one_max>0) sum_xn1xnyn++;

				if(r-x[1]>0) sum_xn++;
				if(r-(x[1]>x[2]?x[1]:x[2])>0) sum_xnyn++;
				if(r-(x[0]>x[1]?x[0]:x[1])>0) sum_xn1xn++;

			}
		}
		p[i][0] = sum_xn1xnyn;
		p[i][1] = sum_xn;
		p[i][2] = sum_xnyn;
		p[i][3] = sum_xn1xn;
	}
}