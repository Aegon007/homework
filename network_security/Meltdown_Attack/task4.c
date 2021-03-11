#include <stdio.h>

int main(){
    char *kernel_data_addr = (char*)0x0000000011bd0c15;
    char kernel_data = *kernel_data_addr;
    printf("I have reached here.\n");
    return 0;
}
