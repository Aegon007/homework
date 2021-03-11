#define PID_MIN  	300
#define PID_MAX 	5000

int pid_map[PID_MAX+1];

int last;	// last pid in use

int allocate_map(void);

int allocate_pid(void);

void release_pid(int);
