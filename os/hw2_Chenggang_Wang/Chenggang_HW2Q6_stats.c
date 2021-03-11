/**
 * 
 *
 * Operating System Concepts - Ninth Edition
 * Copyright John Wiley & Sons, 2013.
 */

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

/* the list of integers */
int *list;

/* the threads will set these values */
double average;
int maximum;
int minimum;

void *calculate_average(void *param);
void *calculate_maximum(void *param);
void *calculate_minimum(void *param);
int calculate_list_length(void *param);


int main(int argc, char *argv[])
{
	/* write your code: allocate memory to hold array of integers, create the threads, wait for the threads to exit, and print out the results */

    // input int numbe list
    char *tmp = "please enter integer list:\n";
    printf("%s", tmp);
    int inputIntList[100]={0}, i=0, j;
    char y;
    do{
        scanf("%d", &inputIntList[i++]);
    }while( (y=getchar()) != '\n' );

    int listSize = calculate_list_length(inputIntList);
    printf("the size of list is: %d \n", listSize);
    tmp = "the input integer list is: ";
    printf("%s", tmp);
    for(j=0; j<listSize; j++){
        printf("%d, ", inputIntList[j]);
    }
    printf("\n");


    // initialize pthread value
    pthread_t thread1, thread2, thread3;
    const char *msg1 = "This is Thread 1";
    const char *msg2 = "This is Thread 2";
    const char *msg3 = "This is Thread 3";
    pid_t p1, p2, p3;

    // create independent threads each of which will excute appropriate function
    p1 = pthread_create(&thread1, NULL, calculate_average, inputIntList);
    if(p1){
        fprintf(stderr, "Error - pthread_create() run with thread1 have return code: %d\n", p1);
        exit(EXIT_FAILURE);
    }else{
        printf("pthread_create() for thread1 returns: %d\n", p1);
    }

    p2 = pthread_create(&thread2, NULL, calculate_maximum, inputIntList);
    if(p2){
        fprintf(stderr, "Error - pthread_create() run with thread2 have return code: %d\n", p2);
        exit(EXIT_FAILURE);
    }else{
        printf("pthread_create() for thread2 returns: %d\n", p2);
    }

    p3 = pthread_create(&thread3, NULL, calculate_minimum, inputIntList);
    if(p1){
        fprintf(stderr, "Error - pthread_create() run with thread3 have return code: %d\n", p3);
        exit(EXIT_FAILURE);
    }else{
        printf("pthread_create() for thread3 returns: %d\n", p3);
    }

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);

    printf("The average is: %f\n", average);
    printf("The minimum is: %d\n", minimum);
    printf("The maximum is: %d\n", maximum);


    return 0;
}


int calculate_list_length(void *param){
    int listLength = 0;
    int *intList = (int*)param;
    while(1){
        if(0 == intList[listLength]){
            break;
        }else{
            listLength++;
        }
    }
    return listLength;
}

void *calculate_average(void *param)
{
	/*write your code here*/
    int *intList = (int*)param;
    int sum = 0;
    int listLength = calculate_list_length(intList);

    for(int i=0; i<listLength; i++) {
        sum = sum + intList[i];
    }

    average = sum / listLength;

}

void *calculate_maximum(void *param)
{
	/*write your code here*/
    int *intList = (int*)param;

    maximum = intList[0];
    int numOfList = calculate_list_length(param);
    for(int i=1; i<numOfList; i++){
        if (maximum < intList[i]){
            maximum = intList[i];
        }
    }


}

void *calculate_minimum(void *param)
{
	/*write your code here*/
    int *intList = (int*)param;

    minimum = intList[0];
    int numOfList = calculate_list_length(param);
    for(int i=1; i<numOfList; i++){
        if (minimum > intList[i]){
            minimum = intList[i];
        }
    }


}

