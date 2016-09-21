#include <stdio.h>
#include "antena.h"

int antena_culc(INPUT *input)
{
  int i = 0;
  for (i = 0; i < 100 ; i++) {
    printf("%d\n", input[i]->k);
  }
  return 0;
}
