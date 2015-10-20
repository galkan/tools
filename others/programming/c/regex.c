#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <regex.h>        

#define MAXMATCH 10
#define LOG_FILE "sample.log"

int main(void)
{
        int reti, i;
        int numchars;

        regex_t regex;
        regmatch_t matches[MAXMATCH];

        char line[8192];
        char result[10240];
        char sourceCopy[10240];
        char msgbuf[100];

        FILE *fp;

        reti = regcomp(&regex, "^([0-9]+\\.[0-9]+)\\s+[0-9]+\\s+([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})\\s+(\\S+)\\s+([0-9]+)\\s+([A-Z]+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+([^$]+)$", REG_EXTENDED);

        if (reti) {
            fprintf(stderr, "Could not compile regex\n");
            exit(EXIT_FAILURE);
        }

        fp = fopen(LOG_FILE, "r");
        if (fp == NULL) {
                fprintf(stderr, "File Cannot Be Opened !!!");
                exit(EXIT_FAILURE);
        }

        while ( fgets(line, sizeof(line), fp) != NULL ) {
                reti = regexec(&regex, line, MAXMATCH, matches, 0);
                memset(result, 0x0, sizeof(result));
                if (!reti) {
                        printf("Match: %s", line);
                } else if (reti == REG_NOMATCH) {
                        printf("No Match: %s"n, line);
                } else {
                        regerror(reti, &regex, msgbuf, sizeof(msgbuf));
                        fprintf(stderr, "Regex match failed: %s\n", msgbuf);
                        exit(1);
                }
        }

        regfree(&regex);

        exit(0);
}
