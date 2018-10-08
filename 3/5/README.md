% ./hello
hello(0)world(0)

Basic parallelization:
#include <stdio.h>
#include <omp.h>

int main(){
        int ID = 0;
        #pragma omp parallel
        printf("hello(%d)", ID);
        printf("world(%d) \n", ID);
        return 0;
}

% ./hello
hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)world(0)


48 threads are created by default (determined by the runtime system).
