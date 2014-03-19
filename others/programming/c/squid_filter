#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>

#define MAX_BUFF 4096
#define TIMESTAMP_SIZE 16
#define ELAPSED_SIZE 8
#define REMOTEHOST_SIZE 16
#define CODE_STATUS_SIZE 32
#define BYTES_SIZE 8	
#define URL_SIZE 2048
#define METHOD_SIZE 8


struct SQUID {
	char *timestamp;
	char *elapsed;
	char *remotehost;
	char *code_status;
	char *bytes;
	char *method;
	char *url;
	char *rfc931;
	char *peerstatus_peerhost;
	char *type;
};

void parse_buff(struct SQUID *squid_line, const char *str);

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

			printf("%s", domain);	

			puts("");
			fflush(stdout);
			continue;
		}

	}

	free(squid_line);

	return 0;
}


void parse_buff(struct SQUID *squid_line, const char *str)
{
	int index = 0;
	int count = 0;

	squid_line->timestamp = (char *)malloc(TIMESTAMP_SIZE);
	memset(squid_line->timestamp, 0x0, TIMESTAMP_SIZE);

	squid_line->elapsed = (char *)malloc(ELAPSED_SIZE);
	memset(squid_line->elapsed, 0x0, ELAPSED_SIZE);	
	
	squid_line->remotehost = (char *)malloc(REMOTEHOST_SIZE);
	memset(squid_line->remotehost, 0x0, REMOTEHOST_SIZE);	

	squid_line->code_status = (char *)malloc(CODE_STATUS_SIZE);
	memset(squid_line->code_status, 0x0, CODE_STATUS_SIZE);

	squid_line->bytes = (char *)malloc(BYTES_SIZE);
	memset(squid_line->bytes, 0x0, BYTES_SIZE);

	squid_line->method = (char *)malloc(METHOD_SIZE);
	memset(squid_line->method, 0x0, METHOD_SIZE);	

	squid_line->url = (char *)malloc(URL_SIZE);
	memset(squid_line->url, 0x0, URL_SIZE);

	while (*str != '\0') {

		 if ( *str == ' ') {
                        while (*str == ' ')
                                str = str + 1;

                        switch (index) {
			case 0:			
                                squid_line->timestamp[count] = '\0';
				break;
                        case 1:
                                squid_line->elapsed[count] = '\0';
				break;
			case 2:
				squid_line->remotehost[count] = '\0';
				break;
			case 3:
				squid_line->code_status[count] = '\0';
				break;
			case 4:
				squid_line->bytes[count] = '\0';
				break;
			case 5:
				squid_line->method[count] = '\0';
				break;
			case 6:
				squid_line->url[count] = '\0';
				break;
			}

                        index = index + 1;
                        count = 0;
                        continue;
                }

		switch (index) {
		case 0:
			squid_line->timestamp[count] = *str;
			count = count + 1;
			break;
		case 1:
			squid_line->elapsed[count] = *str;
			count = count + 1;
			break;
		case 2:
			squid_line->remotehost[count] = *str;
			count = count + 1;
			break;
		case 3:
			squid_line->code_status[count] = *str;
			count = count + 1;
			break;
		case 4:
			squid_line->bytes[count] = *str;
			count = count + 1;
                        break;	
		case 5:
			squid_line->method[count] = *str;
			count = count + 1;
			break;	
		case 6:
			squid_line->url[count] = *str;
			count = count + 1;
			break;
		}

		str = str + 1;
	}
}

