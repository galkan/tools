#!/usr/bin/python

import ldap

class ActiveDirectory:

  def __init__(self):
    
      LDAP_SERVER_EMG = "ldap://192.168.37.37"
      BIND_DN = "user1@SIRKET.local"
      BIND_PASS = "PASSWORD"
      self.USER_BASE = "cn=domain admins,cn=users,dc=SIRKET,dc=local"

      try:
	ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
	self.lcon_emg = ldap.initialize(LDAP_SERVER_EMG)
	self.lcon_emg.simple_bind_s(BIND_DN, BIND_PASS)
      except ldap.LDAPError, e:
	print e
   
      self.scope = ldap.SCOPE_SUBTREE
      
  
  def execute_query(self, base_dn, ldap_filter, option, query_type):
  
    result_set = []
    retrieve_attributes = None
    timeout = 0
  
    try:
      result_id = self.lcon_emg.search(base_dn, self.scope, ldap_filter, retrieve_attributes)
      while True:
	result_type, result_data = self.lcon_emg.result(result_id, timeout)
	if (result_data == []):
	    break
	else:
	  if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
  
      for i in range(len(result_set)):
	for entry in result_set[i]:
	  try:
	      #print entry
	      if query_type == 1:
		base_list = entry[1][option]
		for base in base_list:
		  new_ldap_filter = "sAMAccountName=*"
		  self.execute_query(base, new_ldap_filter, "sAMAccountName", 2)
	      else:
		base_list = entry[1][option]
		for result in base_list:
		    print result
	  except:
	      pass
    except ldap.LDAPError, error_message:
      print error_message
    
##
### Main 
##
    
if __name__ == "__main__":
  
  active_directory = ActiveDirectory()
  ldap_filter = "member=*"
  active_directory.execute_query(active_directory.USER_BASE, ldap_filter, "member", 1)
