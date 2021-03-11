/**
 *
 * Operating System Concepts
 * Copyright John Wiley & Sons, 2013.
 */

#include "pid.h"
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>


/**
 * Allocates the pid map.
 */
int allocate_map(void)
{
	/* write your code here */
    if(NULL == pid_map){
        return -1;
    }else{
        memset(pid_map, 0, sizeof(pid_map));
    }

    for(int i=0; i<PID_MIN; i++){
        pid_map[i] = -1;
    }

    return 1;
}

/**
 * Allocates a pid
 */
int allocate_pid(void)
{
	/* write your code here */
    for(int i=PID_MIN; i<PID_MAX+1; i++){
        if(0 == pid_map[i]){
            pid_map[i] = 1;
            return i;
        }
    }
    return -1;
}

/**
 * Releases a pid
 */
void release_pid(int pid)
{
	/* write your code here */
    assert(pid >= PID_MIN);
    assert(pid <= PID_MAX);
    pid_map[pid] = 0;
}
