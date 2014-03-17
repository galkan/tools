#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
        int ret;
        int fd;
        char buffer[2048];
        char *message_name = "dosya.txt";
 

        if ( (fd = open(message_name, O_WRONLY|O_CREAT|O_TRUNC,0644)) ==- 1)
        {
                fprintf(stderr, "Dosya %s Acilamadi !!!\n", message_name);
        }

        // standart inputdan oku ve fd file descriptoruna yaz
        while( (ret = read(0, buffer, sizeof(buffer))) > 0 )
        {
                if ( write(fd, buffer,ret) == -1 )
                {
                        ;
                }
        }

        close(fd);

        // fd file descriptoru tekrardan okuma modunda ac ve ekrana yazdir
        fd = open(message_name, O_RDONLY);
        while( (ret = read(fd, buffer, sizeof(buffer))) > 0 )
        {
                printf("%s\n", buffer);
        }

        close(fd);

        return 0;
}
