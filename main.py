#!/usr/bin/python
import parser,sys,init_history

def main():
	#open the input file for reading
	user_input = parser.parse(sys.argv[1])
<<<<<<< HEAD
	#store the user's input passwords
=======
	history = init_history.initialize_history(user_input)
	#store the user's input password
>>>>>>> 0e10d7b170c0cec57d0ccf37689c83db53ebfc90
	list_pass = user_input[1]
	#store the list of features
	list_features = user_input[0]



#Run the main function
if __name__ == '__main__':
    main()

