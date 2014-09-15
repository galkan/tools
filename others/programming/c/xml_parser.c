#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

#define TAG_COUNT 32
#define IDS_COUNT 128

// gcc -o parser parser.c -lxml2 -I/usr/include/libxml2 

struct IDS_XML_NODE {
	xmlChar *id;
        xmlChar *rule;
        xmlChar *description;
        xmlChar *impact;
        xmlChar *tag[TAG_COUNT];
};

void parse_node (xmlDocPtr doc, xmlNodePtr cur, struct IDS_XML_NODE *idsxml) {
        xmlChar *id;
        xmlChar *rule;
        xmlChar *description;
        xmlChar *impact;
        xmlChar *tag[TAG_COUNT];
	xmlNodePtr tmp_cur;
	int count = 0;
	
        cur = cur->xmlChildrenNode;
        while (cur != NULL) {
                if ((!xmlStrcmp(cur->name, (const xmlChar *)"id"))) {
                        idsxml->id = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
                } else if ((!xmlStrcmp(cur->name, (const xmlChar *)"rule"))) {
                        idsxml->rule = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
                } else if ((!xmlStrcmp(cur->name, (const xmlChar *)"description"))) {
                        idsxml->description = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
                } else if ((!xmlStrcmp(cur->name, (const xmlChar *)"tags"))) {
			tmp_cur = cur;
			cur = cur->xmlChildrenNode;
			while(cur != NULL) {
				if ((!xmlStrcmp(cur->name, (const xmlChar *)"tag"))) {
					idsxml->tag[count] = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
					count = count + 1;
				}
        			cur = cur->next;
			}
			idsxml->tag[count] = NULL;
			cur = tmp_cur;
                } else if ((!xmlStrcmp(cur->name, (const xmlChar *)"impact"))) {
                        idsxml->impact = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
                }

        	cur = cur->next;
        }

        return;
}

static void parseDoc(char *docname, struct IDS_XML_NODE **idsxml) {
        xmlDocPtr doc;
        xmlNodePtr cur;
	int i;

        doc = xmlParseFile(docname);
        if (doc == NULL ) {
                fprintf(stderr,"Document not parsed successfully. \n");
                return;
        }

        cur = xmlDocGetRootElement(doc);
        if (cur == NULL) {
                fprintf(stderr,"empty document\n");
                xmlFreeDoc(doc);
                return;
        }

        if (xmlStrcmp(cur->name, (const xmlChar *) "filters")) {
                fprintf(stderr,"document of the wrong type, root node != filters");
                xmlFreeDoc(doc);
                return;
        }

	i = 0;
        cur = cur->xmlChildrenNode;
        while (cur != NULL) {
                if ((!xmlStrcmp(cur->name, (const xmlChar *)"filter"))){
			idsxml[i] = (struct IDS_XML_NODE *)malloc(sizeof(struct IDS_XML_NODE));
                        parse_node(doc,cur, idsxml[i]);
			i = i + 1;
                }
                cur = cur->next;
        }
	idsxml[i] = NULL;

        xmlFreeDoc(doc);

        return;
}

//
/// Main
//

int main(int argc, char **argv) {

	int k,i;
        char *docname;

        if (argc <= 1) {
                printf("Usage: %s docname\n", argv[0]);
                return(0);
        }

	struct IDS_XML_NODE *idsxml[IDS_COUNT];
        docname = argv[1];

        parseDoc (docname, idsxml);

	for(i=0; idsxml[i] != NULL; i++) {
        	printf("%s -- %s -- %s -- ", idsxml[i]->id, idsxml[i]->rule, idsxml[i]->description);
        	for(k=0; idsxml[i]->tag[k] != NULL; k++) {
        		if (idsxml[i]->tag[k+1] == NULL)
                		printf("%s -- ", idsxml[i]->tag[k]);                            
                	else
                        	printf("%s, ", idsxml[i]->tag[k]);                              
                	xmlFree(idsxml[i]->tag[k]);
        	}
        	printf("%s\n", idsxml[i]->impact);

        	xmlFree(idsxml[i]->id);
        	xmlFree(idsxml[i]->rule);
        	xmlFree(idsxml[i]->description);
        	xmlFree(idsxml[i]->impact);
        	free(idsxml[i]);
	}

        return 0;
}

