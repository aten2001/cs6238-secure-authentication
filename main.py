#!/usr/bin/python
import parser,sys

def main():
	#open the input file for reading
	user_input = parser.parse(sys.argv[1])
	#store the user's input passwords
	list_pass = user_input[1]
	#store the list of features
	list_features = user_input[0]



#Run the main function
if __name__ == '__main__':
    main()

