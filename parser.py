#!/usr/bin/python

#reads from file and passes results to the login_handler
#returns a list l where l[0] is user entered password and l[1] is an array of features 
def parse(filename):
	print "parsing input file"
	# with open(filename,'r') as f:
	# 	for line in f:
	# 		print line

	user_input_pass = "pass"
	#list of features to return
	features = [0,3,4,5,1,9,8]
	ret_list = [user_input_pass, features]
	return ret_list