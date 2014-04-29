#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/sysctl.h>
#include <pwd.h>
#include <unistd.h>
#include <libproc.h>

char *get_procname(int pid)
{

	int ret;
	char *pathbuf;
	pathbuf = (char *)malloc(sizeof(char)*PROC_PIDPATHINFO_MAXSIZE);
	if (pathbuf == NULL)
		return NULL;

	ret = proc_pidpath (pid, pathbuf, PROC_PIDPATHINFO_MAXSIZE);
	if (ret < 0)
		return NULL;

	return pathbuf;
}


int main(int argc, const char **argv) 
{
    	int err = 0;
    	struct kinfo_proc *proc_list = NULL;
    	size_t length = 0;
	
    	static const int name[] = { CTL_KERN, KERN_PROC, KERN_PROC_ALL, 0 };

    	// Call sysctl with a NULL buffer to get proper length
    	err = sysctl((int *)name, (sizeof(name) / sizeof(*name)) - 1, NULL, &length, NULL, 0);
    	if (err) {
		perror(NULL);
		free(proc_list);
		return EXIT_FAILURE;
	}

    	// Allocate buffer
    	proc_list = malloc(length);
    	if (!proc_list) {
		perror(NULL);
		free(proc_list);
		return EXIT_FAILURE;
	}

    	// Get the actual process list
    	err = sysctl((int *)name, (sizeof(name) / sizeof(*name)) - 1, proc_list, &length, NULL, 0);
    	if (err) {
		perror(NULL);
		free(proc_list);
		return EXIT_FAILURE;
	}	

    	int proc_count = length / sizeof(struct kinfo_proc);

    	for (int i = 0; i < proc_count; i++) {
		char *proc_name;
		pid_t pid;
		pid = proc_list[i].kp_proc.p_pid;
		proc_name = get_procname(pid);
		printf("%s\n", proc_name);
		free(proc_name);

    }

    free(proc_list);

    return EXIT_SUCCESS;
}
