#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>

#define MAX_BUFF 4096
#define URL_SIZE 2048
#define SRCIP_SIZE 32
#define IDENT_SIZE 16
#define METHOD_SIZE 8

struct SQUID {
	char *url;
	char *srcip;
	char *ident;
	char *method;
};

void parse_buff(struct SQUID *squid_line, const char *str);
void log_event(const char *msg);

int main(int argc, const char *argv[])
{
	int finished = 0;
	int domain_index = 0;
	char buff[MAX_BUFF];
	char *tmp;
	char *domain;
	struct SQUID *squid_line;

	if ( (squid_line = (struct SQUID *)malloc(sizeof(struct SQUID))) == NULL ) {
		perror("malloc");
		exit(EXIT_FAILURE);
	}
		
	while (!finished) {
		while(fgets(buff, MAX_BUFF, stdin) != NULL) {
			
			parse_buff(squid_line, buff);

			if ( (tmp = strstr(squid_line->url, "http://")) != NULL ) {
				tmp = tmp + 7;
				domain_index = 0;

				if ( (domain = (char *)malloc(URL_SIZE)) == NULL ) {
					perror("malloc");
					exit(EXIT_FAILURE);	
				}
				
				while ( *tmp != '/') {
					domain[domain_index] = *tmp;
					tmp = tmp + 1;
					domain_index = domain_index + 1;	
				}
				domain[domain_index] = '\0';
			}
			else
				continue;	

			if (strcmp(domain, "www.google.com") == 0) {
				char *new_url = (char *)malloc(URL_SIZE);
				sprintf(new_url, "http://www.galkan.net %s %s %s\n", squid_line->srcip, squid_line->ident, squid_line->method);
				printf("%s",new_url);			
				fflush(stdout);
				free(new_url);
				continue;

			} else {
				puts("");
				fflush(stdout);
				continue;
			}

		}

	}

	free(squid_line);

	return 0;
}

void log_event(const char *msg)
{
	FILE *fp;

	fp = fopen("/tmp/galkan.log", "a");
	fwrite(msg , 1 , strlen(msg) , fp); 
	fclose(fp);	
}

void parse_buff(struct SQUID *squid_line, const char *str)
{
	int index = 0;
	int count = 0;

	squid_line->url = (char *)malloc(URL_SIZE);
	memset(squid_line->url, 0x0, URL_SIZE);

	squid_line->srcip = (char *)malloc(SRCIP_SIZE);
	memset(squid_line->srcip, 0x0, SRCIP_SIZE);	
	
	squid_line->ident = (char *)malloc(IDENT_SIZE);
	memset(squid_line->ident, 0x0, IDENT_SIZE);	

	squid_line->method = (char *)malloc(METHOD_SIZE);
	memset(squid_line->method, 0x0, METHOD_SIZE);

	while (*str != '\0') {

		 if ( *str == ' ') {
                        while (*str == ' ')
                                str = str + 1;

                        switch (index) {
			case 0:			
                                squid_line->url[count] = '\0';
				break;
                        case 1:
                                squid_line->srcip[count] = '\0';
				break;
			case 2:
				squid_line->ident[count] = '\0';
				break;
			case 3:
				squid_line->method[count] = '\0';
				break;
			}

                        index = index + 1;
                        count = 0;
                        continue;
                }

		switch (index) {
		case 0:
			squid_line->url[count] = *str;
			count = count + 1;
			break;
		case 1:
			squid_line->srcip[count] = *str;
			count = count + 1;
			break;
		case 2:
			squid_line->ident[count] = *str;
			count = count + 1;
			break;
		case 3:
			squid_line->method[count] = *str;
			count = count + 1;
			break;
		}

		str = str + 1;
	}
}

