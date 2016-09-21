#include <stdio.h>
#include "main.h"
#include "snapper.h"

int main(int argc,char *argv[])
{
  int res, iter, T = {0};
  FILE *fp;
  char str[NUM];
  INPUT input[T_NUM] = {{0, 0}};

  if (argc < 2) {
    printf("Please input file name");
    return -1;
  }

  // File open
  fp = fopen(argv[1],"r");
  if (fp == NULL) {
    printf("File open failed.\n");
    return -1;
  }

  while ((fgets(str, NUM, fp)) != NULL) {
    if (iter == 0)
       sscanf(str,"%d", &T);
    else
       sscanf(str,"%d %d", &(input[iter-1].n), &(input[iter-1].k));
    iter++;
  }

  // Culculation prosess start.
  for (iter = 0; iter < T; iter++) {
    res = snapper_culc(&(input[iter]));
    printf("Case #%d: %s\n", iter + 1, res == 1 ? "ON" : "OFF");
  }

  // Close file
  fclose(fp);
  return 0;
}
