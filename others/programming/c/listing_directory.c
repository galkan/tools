#include <stdio.h>
#include <dirent.h>
#include <sys/stat.h>

int main(void)
{
        struct dirent *direntp;
        DIR *dirp;

        if((dirp = opendir("/tmp")) == NULL)
        {
                printf("Hata\n");
        }

        while((direntp = readdir(dirp)) != NULL)
        {
                if( ((strncmp(direntp->d_name, "textfile", 8) != 0)) && ((strncmp(direntp->d_name, ".", 1) != 0)) )
                        printf("%s\n",direntp->d_name);
        }

        return 0;
}
