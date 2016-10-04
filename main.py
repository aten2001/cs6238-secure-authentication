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


	#need to compute mu and sigma
	#will return a list of mus per feature
	mu_list = math.compute_mu_list(history)
	sigma_list=math.compute_sigma_list(history)
	#figures out if we are slow or fast and computes the instruction table.
	instruction_table = math.compute_instruction_table(mu_list,sigma_list)
	pwd = user_input[0][0]
	#need to encrypt the instruction table with the user entered pwd
	encrypted_instruction_table = math.encrypt_instruction_table(instruction_table,pwd)

	encrypted_history_file = compute_history.compute_history(history, hpwd)

	#check the rest of the user's inputs and see if he or she logged in correctly


#Run the main function
if __name__ == '__main__':
	main()

