#ifndef _SNAPPER_H_
#define _SNAPPER_H_
#include "main.h"

#define S_MAX 30
#define HIGH 1
#define LOW 0

#define ON 1
#define OFF 0

typedef struct _SNAPPER {
  int OUT;
  int STATE;
} SNAPPER;

// ヘッダファイルの中身
int snapper_culc(INPUT *input);

#endif // _SNAPPER_H_
