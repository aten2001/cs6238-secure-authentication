#!/usr/bin/python

#reads from file and passes results to the login_handler
#returns a list l where l[0] is user entered password and l[1] is an array of features 
def parse(filename):
	feature = False
	password_features = [] # list of features per entered password
	features = [] # list of password_features list
	list_passwords = [] #list of user entered passwords

	print "parsing input file"
	with open(filename,'r') as f:
		for line in f:
			if feature == False: #store the user input password
				user_input_pass = line
				list_passwords.append(user_input_pass.rstrip("\n"))

				feature = True
			else:
				input_features = line.split(',') # split the input on comma delimeted
				for l in input_features:
					password_features.append(int(l))
				features.append(password_features)
				password_features=[]
				feature = False

	ret_list = [list_passwords, features]
	return ret_list

#Run the main function
if __name__ == '__main__':
	parse('input-file.txt')