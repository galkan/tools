#include <stdio.h>
#include <GeoIP.h>
#include <GeoIPCity.h>
#include <stdlib.h>

//  gcc -o calistir deneme.c -lGeoIP
//  https://github.com/maxmind/geoip-api-c/blob/master/test/test-geoip.c

int main(void)
{
      const char *ipAddress = "193.140.74.29";
      char expectedCountry[3];
      const char *returnedCountry;
      GeoIP *gi;
      int i;
 
      if (0 == i) {
	  /* Read from filesystem, check for updated file */
	  gi = GeoIP_open("/usr/share/GeoIP/GeoIP.dat",  GEOIP_STANDARD | GEOIP_CHECK_CACHE);
      } else {
	  /* Read from memory, faster but takes up more memory */
	  gi = GeoIP_open("/usr/share/GeoIP/GeoIP.dat", GEOIP_MEMORY_CACHE);
      }

      if (gi == NULL) {
	fprintf(stderr, "Error opening database\n");
	exit(1);
      }
  
      returnedCountry = GeoIP_country_code_by_addr(gi, NULL);
      if (returnedCountry != NULL) {
	  fprintf(stderr, "Invalid Query test failed, got non NULL, expected NULL\n");
	  exit(EXIT_FAILURE);  
      }
  
      returnedCountry = GeoIP_country_code_by_name(gi, NULL);
      if (returnedCountry != NULL) {
	fprintf(stderr,"Invalid Query test failed, got non NULL, expected NULL\n");
      }
  
      returnedCountry = GeoIP_country_code3_by_addr(gi, ipAddress);
      printf("%s => %s\n", ipAddress, returnedCountry);
      
      return 0;
}
