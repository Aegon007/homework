#include <stdio.h>
#include <stdlib.h>


/*
 * 32-bit virtual address is 2 to the power 32
 * the page size is 4-KB, which is 2 to the power of 12
 * */

int main(int argc, char* argv[]){
    if (argc < 2){
        printf("Please provide a address in the parameter.\n");
    } else if (argc > 2) {
        printf("Too many arguments are given.\n");
    }

    uint pageSize = 4096;
    uint memAddress = atoi(argv[1]);

    uint pageNum, offset;

    pageNum = (int)(memAddress/pageSize);
    offset = memAddress - pageNum * pageSize;


    printf("page number = %d\n", pageNum);
    printf("offset = %d\n", offset);

    return 0;
}
