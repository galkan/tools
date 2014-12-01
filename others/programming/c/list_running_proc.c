int _is_sniffer_running(void)
{
      int n,i;
      int retval = 0;
      int len;
      char proc_name[512];
      char target_path[512];
      char tofind[512];  
      char *packet_sniffers[] = {"wireshark","tcpdump","tshark", NULL};
      regex_t re;
  
      struct dirent *direntp;
      DIR *dirp;
  
      if((dirp = opendir(PROC_DIR)) == NULL)
	  exit(EXIT_FAILURE);
    
    
      while((direntp = readdir(dirp)) != NULL) {
	    if ( strspn(direntp->d_name, PROC_SIG) == strlen(direntp->d_name)) {
		 sprintf(proc_name, PROC_DIR"/%s/exe", direntp->d_name);
		 memset(target_path, 0, 512);
		 len = readlink (proc_name, target_path, sizeof(target_path));
		 
		 if (len > 0) {
		    for (i=0; packet_sniffers[i] != NULL; ++i) {
			  if(regcomp(&re, packet_sniffers[i], REG_EXTENDED) != 0) {
			      printf("Error\n");
			      return EXIT_FAILURE;   
			  }    
			  
			  if((retval = regexec(&re, target_path, 0, NULL, 0)) == 0) {
			      printf("%s\n", target_path);
			      return 0;
			  }
		    }  
		 }
	    }
       }
      
      return 1;
}
