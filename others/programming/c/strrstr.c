char *strrstr(const char *x, const char *y);

char *strrstr(const char *x, const char *y) {
        char *prev = NULL;
        char *next;

        if (*y == '\0')
                return strchr(x, '\0');

        while ((next = strstr(x, y)) != NULL) {
                prev = next;
                x = next + 1;
        }

        return prev;
}
