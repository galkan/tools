#!/usr/bin/env python
 
class man(object):
 
    # name of the man
    name = ""
 
    def __init__(self, P_name):
        """ Class constructor """
        self.name = P_name
        print("Here comes " + self.name)
 
    def talk(self, P_message):        
        print(self.name + " says: '" + P_message + "'")        
 
    def walk(self):
        """ This let an instance of a man to walk """
        print(self.name + " walks")
 
# This class inherits from Man class
# A superman has all the powers of a man (A.K.A. Methods and Properties in our case ;-)
class superman(man):
 
    # Name of his secret identity
    secret_identity = ""
 
    def __init__(self, P_name, P_secret_identity):
        """ Class constructor that overrides its parent class constructor"""
        # Invokes the class constructor of the parent class #
        super(superman, self).__init__(P_name)
        # Now let's add a secret identity
        self.secret_identity = P_secret_identity
        print("...but his secret identity is '" + self.secret_identity + "' and he's a super-hero!")
 
    def walk(self, P_super_speed = False):
        # Overrides the normal walk, because a superman can walk at a normal
        # pace or run at the speed of light!
        if (not P_super_speed): super(superman, self).walk()
        else: print(self.secret_identity + " run at the speed of light")
 
    def fly(self):
        """ This let an instance of a superman to fly """
        # No man can do this!
        print(self.secret_identity + " fly up in the sky")
 
    def x_ray(self):
        """ This let an instance of a superman to use his x-ray vision """
        # No man can do this!
        print(self.secret_identity + " uses his x-ray vision")
 
 
# Declare some instances of man and superman
lois = man("Lois Lane")
jimmy = man("Jimmy Olsen")
clark = superman("Clark Kent", "Superman")
