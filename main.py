#!/usr/bin/python

def main():
	#open the input file for reading
	parser()


#reads from file and passes results to the login_handler
def parser():
	#do something
	print "parsing file"
	with open('input-file.txt','r') as f:
		for line in f:
			print line

#takes in password and feature list
def login_handler(user_password, list_features):
	print "login handler"



#Run the main function
if __name__ == '__main__':
    main()