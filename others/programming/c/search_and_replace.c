char * escape_string( const char *string, const char *substr, const char *replacement )
{
        char *tok = NULL;
        char *newstr = NULL;
        char *oldstr = NULL;
        char *head = NULL;

        // if either substr or replacement is NULL, duplicate string a let caller handle it
        //if ( substr == NULL || replacement == NULL ) return strdup (string);

        newstr = strdup (string);
        head = newstr;
        while ( (tok = strstr ( head, substr ))){
                oldstr = newstr;
                newstr = malloc ( strlen ( oldstr ) - strlen ( substr ) + strlen ( replacement ) + 1 );
                /*failed to alloc mem, free old string and return NULL */
                if ( newstr == NULL ){
                        free (oldstr);
                        return NULL;
                }

                memcpy ( newstr, oldstr, tok - oldstr );
                memcpy ( newstr + (tok - oldstr), replacement, strlen ( replacement ) );
                memcpy ( newstr + (tok - oldstr) + strlen( replacement ), tok + strlen ( substr ), strlen ( oldstr ) - strlen ( substr ) - ( tok - oldstr ) );
                memset ( newstr + strlen ( oldstr ) - strlen ( substr ) + strlen ( replacement ) , 0, 1 );

                /* move back head right after the last replacement */
                head = newstr + (tok - oldstr) + strlen( replacement );
                free (oldstr);
        }

        return newstr;
}
