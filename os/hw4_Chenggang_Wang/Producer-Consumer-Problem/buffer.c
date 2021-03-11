/**
 *
 * This is a POSIX solution using unnamed semaphores.
 *
 * This solution will not work on OS X systems,
 * but will work with Linux.
 */

#include "buffer.h"
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>     /* required for pthreads */
#include <semaphore.h>   /* required for semaphores */
#include <unistd.h>

#define TRUE 1


buffer_item buffer[BUFFER_SIZE];

pthread_mutex_t mutex;
sem_t empty;
sem_t full;

int insertPointer = 0, removePointer = 0;

void *producer(void *param);
void *consumer(void *param);

int insert_item(buffer_item item)
{
    /* Write your code here
     * return 0 if successful, otherwise
     * return -1 indicating an error condition
     * */
    sem_wait(&empty);
    pthread_mutex_lock(&mutex);
    int flag = 0;

    if(insertPointer >= BUFFER_SIZE) {
        removePointer = BUFFER_SIZE - 1;
        flag = -1;
    }else{
        // produc an item
        // place in buffer
        buffer[insertPointer] = item;
        insertPointer++;
    }

    pthread_mutex_unlock(&mutex);
    sem_post(&full);

    return flag;
}

int remove_item(buffer_item *item)
{
	/* Write your code here
     * placing it in item
     * return 0 if successful, otherwise
     * return -1 indicating an error condition
     * */
    sem_wait(&full);
    pthread_mutex_lock(&mutex);
    int flag = 0;

    // remove item from buffer
    if (0 > removePointer){
        insertPointer = 0;
        flag = -1;
    }
    else {
        // consumes item
        *item = buffer[removePointer];
        removePointer--;
    }

    pthread_mutex_unlock(&mutex);
    sem_post(&empty);

    return flag;
}


int main(int argc, char *argv[])
{
	int sleepTime, producerThreads, consumerThreads;
	int i, j;

	if(argc != 4)
	{
		fprintf(stderr, "Useage: <sleep time> <producer threads> <consumer threads>\n");
		return -1;
	}

	sleepTime = atoi(argv[1]);
	producerThreads = atoi(argv[2]);
	consumerThreads = atoi(argv[3]);

	/* Initialize the synchronization tools */
	printf("%d\n",pthread_mutex_init(&mutex, NULL));
	printf("%d\n",sem_init(&empty, 0, 5));
	printf("%d\n",sem_init(&full, 0, 0));
	srand(time(0));

	/* Create the producer and consumer threads */
	for(i = 0; i < producerThreads; i++)
	{
		pthread_t tid;
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_create(&tid, &attr, producer, NULL);
	}

	for(j = 0; j < consumerThreads; j++)
	{
		pthread_t tid;
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_create(&tid, &attr, consumer, NULL);
	}

	/* Sleep for user specified time */
	sleep(sleepTime);
	return 0;
}

void *producer(void *param)
{
	buffer_item random;
	int r;

	while(TRUE)
	{
		r = rand() % 5;
		sleep(r);
		random = rand();

		if(insert_item(random))
			fprintf(stderr, "Error\n");

		printf("Producer produced %d \n", random);

	}

}

void *consumer(void *param)
{
	buffer_item random;
	int r;

	while(TRUE)
	{
		r = rand() % 5;
		sleep(r);

		if(remove_item(&random))
			fprintf(stderr, "Error Consuming\n");
		else
			printf("Consumer consumed %d \n", random);
	}
}
