#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <fcntl.h>
#include <getopt.h>
#include <semaphore.h>
#include <time.h>

#define BUFSIZE		32

void *thread_proc(void *param);
sem_t g_sem;

char *readline(int fd, char *str)
{
	static char g_buf[BUFSIZE];
	static int g_curIndex = BUFSIZE;
	static int g_curBufLen = BUFSIZE;
	int i;

	i = 0;
	for (;;) {
		if (g_curIndex >= g_curBufLen) {
			if ((g_curBufLen = read(fd, g_buf, BUFSIZE)) == 0)
				break;
			g_curIndex = 0;
		}
		if (g_buf[g_curIndex] == '\n') {
			++g_curIndex;
			break;
		}
		str[i++] = g_buf[g_curIndex++];
	}
	
	str[i] = '\0';
	
	return g_curBufLen == 0 && i == 0 ? NULL : str;
}

int main(int argc, char *argv[])
{
	int mflag = 0;
	int tflag = 0;
	char *targ;
	char *gonder_baba;
	int ch;
	int maxThread;
	char line[4096];
	int fd, result, semval;
	FILE *fp;
	pthread_t tid;
		    
	opterr = 0;
     
	while ((ch = getopt(argc, argv, "t:m")) != -1)
		switch (ch) {
			case 'm':
				mflag = 1;
				break;
			case 't':
				tflag = 1;
				targ = optarg;
				break;
			case '?':
				fprintf(stderr, "invalid argument: '%c'\n", optopt);
				exit(EXIT_FAILURE);
		}

	if (mflag)
		printf("mflag exists!\n");
	
	if (!tflag) {
		fprintf(stderr, "-t switch must be specified!\n");
		exit(EXIT_FAILURE);
	}
	
	if (optind != argc - 1) {
		fprintf(stderr, "too many arguments or argument missing!\n");
		exit(EXIT_FAILURE);
	}
	
	maxThread = (int) strtol(targ, NULL, 10);
		
	if ((fd = open(argv[optind], O_RDONLY)) == -1) {
		perror("open");
		exit(EXIT_FAILURE);
	}
	
	if (sem_init(&g_sem, 0, maxThread) < 0) {
		perror("sem_init");
		exit(EXIT_FAILURE);
	}
	
	while (readline(fd, line) != NULL) {
		gonder_baba = (char *)malloc(1024);
		strcpy(gonder_baba, line);
		sem_wait(&g_sem);
		if ((result = pthread_create(&tid, NULL, thread_proc, gonder_baba)) != 0) {
			fprintf(stderr, "pthread_create: %s\n", strerror(result));
			exit(EXIT_FAILURE);
		}
	}

	while (sem_getvalue(&g_sem, &semval), semval != maxThread) 
		usleep(100000);
	
	return 0;
}

void *thread_proc(void *param)
{
	char *str = (char *) param;
	
	printf("%s\n", str);
	sleep(rand() % 3);
	free(str);
	sem_post(&g_sem);
	
	return NULL;
}
