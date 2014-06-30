#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>

int main(int argc, char *argv[])
{
	int tflag = 0;
	int fflag = 0;
	char *targ;
	char *farg;
	int ch;
	int maxThread;

	opterr = 0;

	while ((ch = getopt(argc, argv, "t:f:")) != -1)
		switch (ch) {
			case 'f':
				fflag = 1;
				farg = optarg;
				break;
			case 't':
				tflag = 1;
				targ = optarg;
				break;
			case '?':
				fprintf(stderr, "invalid argument: '%c'\n", optopt);
				exit(EXIT_FAILURE);
	}


	if ( ! fflag) {
		fprintf(stderr, "-f switch must be specified !!!\n");
		exit(EXIT_FAILURE);
	}


	if (! tflag) {
		fprintf(stderr, "-t switch must be specified !!!\n");
		exit(EXIT_FAILURE);
	}

	maxThread = (int)strtol(targ, NULL, 10);

	return 0;
}
