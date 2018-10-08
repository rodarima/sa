#include <stdio.h>
#include <omp.h>

void hello(void);

int main(){
        #pragma omp parallel
        hello();
        return 0;
}

void hello(void){
        int my_rank = omp_get_thread_num();
        int thread_count = omp_get_num_threads();
		#pragma omp ordered
        printf("Hello from thread %d of %d\n", my_rank, thread_count);
}
