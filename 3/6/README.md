Parallelization with thread rank as ID
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

        printf("Hello from thread %d of %d\n", my_rank, thread_count);
}

% ./hello
Hello from thread 0 of 48
Hello from thread 16 of 48
Hello from thread 7 of 48
Hello from thread 4 of 48
Hello from thread 30 of 48
Hello from thread 34 of 48
Hello from thread 17 of 48
Hello from thread 43 of 48
Hello from thread 41 of 48
Hello from thread 45 of 48
Hello from thread 31 of 48
Hello from thread 19 of 48
Hello from thread 3 of 48
Hello from thread 47 of 48
Hello from thread 6 of 48
Hello from thread 27 of 48
Hello from thread 46 of 48
Hello from thread 9 of 48
Hello from thread 24 of 48
Hello from thread 25 of 48
Hello from thread 44 of 48
Hello from thread 12 of 48
Hello from thread 2 of 48
Hello from thread 5 of 48
Hello from thread 23 of 48
Hello from thread 20 of 48
Hello from thread 28 of 48
Hello from thread 22 of 48
Hello from thread 21 of 48
Hello from thread 11 of 48
Hello from thread 10 of 48
Hello from thread 15 of 48
Hello from thread 13 of 48
Hello from thread 14 of 48
Hello from thread 1 of 48
Hello from thread 18 of 48
Hello from thread 32 of 48
Hello from thread 35 of 48
Hello from thread 37 of 48
Hello from thread 39 of 48
Hello from thread 29 of 48
Hello from thread 42 of 48
Hello from thread 8 of 48
Hello from thread 40 of 48
Hello from thread 33 of 48
Hello from thread 26 of 48
Hello from thread 36 of 48
Hello from thread 38 of 48

Threads don't execute in order of their rank. Order depends on how the scheduler assigns execution.

In order to make then execute in order of rank, use '#pragma omp ordered':
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

# ./hello
Hello from thread 0 of 48
Hello from thread 1 of 48
Hello from thread 2 of 48
Hello from thread 3 of 48
Hello from thread 4 of 48
Hello from thread 5 of 48
Hello from thread 6 of 48
Hello from thread 7 of 48
Hello from thread 8 of 48
Hello from thread 9 of 48
Hello from thread 10 of 48
Hello from thread 11 of 48
Hello from thread 12 of 48
Hello from thread 13 of 48
Hello from thread 14 of 48
Hello from thread 15 of 48
Hello from thread 16 of 48
Hello from thread 17 of 48
Hello from thread 18 of 48
Hello from thread 19 of 48
Hello from thread 20 of 48
Hello from thread 21 of 48
Hello from thread 22 of 48
Hello from thread 23 of 48
Hello from thread 24 of 48
Hello from thread 25 of 48
Hello from thread 26 of 48
Hello from thread 27 of 48
Hello from thread 28 of 48
Hello from thread 29 of 48
Hello from thread 30 of 48
Hello from thread 31 of 48
Hello from thread 32 of 48
Hello from thread 33 of 48
Hello from thread 34 of 48
Hello from thread 35 of 48
Hello from thread 36 of 48
Hello from thread 37 of 48
Hello from thread 38 of 48
Hello from thread 39 of 48
Hello from thread 40 of 48
Hello from thread 41 of 48
Hello from thread 42 of 48
Hello from thread 43 of 48
Hello from thread 44 of 48
Hello from thread 45 of 48
Hello from thread 46 of 48
Hello from thread 47 of 48


