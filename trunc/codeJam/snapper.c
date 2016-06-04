#include <stdio.h>
#include "snapper.h"

int snapper_culc(INPUT *input) {
  int res, i, k = 0;
  SNAPPER snap[S_MAX];

  for (i = 0; i < S_MAX; i++) {
    snap[i].OUT   = 0;
    snap[i].STATE = 0;
  }

  // Fist snapper is as Power supply. State is Dummy
  snap[0].OUT = HIGH;

  for (i = 0; i < input->k; i++) {
    for (k = input->n; k >= 1; k--) {
      if (snap[k-1].OUT == HIGH) {
        snap[k].STATE = 1 - snap[k].STATE;
      }
    }
    for (k = 1; k < input->n; k++) {
      if (snap[k].STATE == ON && snap[k-1].OUT == HIGH) {
        snap[k].OUT = HIGH;
      }
      else {
        snap[k].OUT = LOW;
      }
    }
  }
  res = snap[input->n].OUT;

  return res;
}
