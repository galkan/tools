#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>

#define PROC_DIR "/proc"

void exitsys(const char *msg);

int main(void)
{
	int n;
	int len;
        char proc_name[512];
	char target_path[512];
	
	struct dirent *direntp;
        DIR *dirp;
	
        if((dirp = opendir(PROC_DIR)) == NULL)
	    exitsys("opendir");
	  	  
        while((direntp = readdir(dirp)) != NULL) {
	   if ( strspn(direntp->d_name, "0123456789") == strlen(direntp->d_name)) {
	      sprintf(proc_name, PROC_DIR"/%s/exe", direntp->d_name);
	      memset(target_path, 0, 512);
	      len = readlink (proc_name, target_path, sizeof(target_path));
	      if (len > 0)
		printf("%s:%s\n", proc_name, target_path);
	      
	      }	  
	   }
  
	return 0;
}

void exitsys(const char *msg)
{
    perror("msg");
    exit(EXIT_FAILURE); 
}
