#!/usr/bin/python
import parser,sys,init_history,compute_history,math

def main():
	#open the input file for reading
	user_input = parser.parse(sys.argv[1])

	#store the user's input passwords

	history = init_history.initialize_history(user_input)
	#will compute the history of the user's input and creates a history file
    # need to choose a hardened password
    hpwd = math.choose_hpwd()

    encrypted_history_file = compute_history.compute_history(history, 50)


	#check the rest of the user's inputs and see if he or she logged in correctly



#Run the main function
if __name__ == '__main__':
    main()

