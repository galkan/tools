#include <stdio.h>
#include <stdlib.h>


int main( int argc, char *argv[] )
{

	FILE *fp;
  	char result[1024];

  	fp = popen("/bin/ls -il /etc/", "r");
  	if (fp == NULL) {
    		printf("Failed to run command\n" );
    		exit(EXIT_FAILURE);
  	}

  	while (fgets(result, sizeof(result)-1, fp) != NULL)
    		printf("%s", result);
  	
  	pclose(fp);

  	return 0;
}
