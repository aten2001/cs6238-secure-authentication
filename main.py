#!/usr/bin/python
import input_parser,sys,init_history,compute_history,myMath,logging

logging.basicConfig(filename='status.log', level=logging.DEBUG)

def test_decrypt_history(key):
	message = "Brian Is the Man!"
	logging.debug("Testing the Encrypt and Decrypt functionality of the history file")
	logging.debug("ORIGINAL MESSAGE: "+message)
	cipher_text = compute_history.compute_history(message, key)
	logging.debug("CIPHER TEXT: "+cipher_text)
	logging.debug("Decrypted Cipher Text: "+ compute_history.decrypt_history(cipher_text,key))

def main():
	#open the input file for reading
	x = sys.argv[1]

	user_input = input_parser.parse(x)
	m = len(user_input[1][0])  # TODO need to assign m correctly based on user input.
	#store the user's input passwords
	history = init_history.initialize_history(user_input)
	#will compute the history of the user's input and creates a history file
	# need to choose a random hardened password and r and q
	pwdArray = myMath.choose_hpwd()
	hpwd = pwdArray[0]
	q = pwdArray[1]
	r  = pwdArray[2]
	print "hpwd"
	print hpwd
	#need to compute mu and sigma
	#will return a list of mus per feature
	mu_list = myMath.compute_mu_list(history)
	sigma_list=myMath.compute_sigma_list(history)
	pwd = user_input[0][0]
	#figures out if we are slow or fast and computes the instruction table.
	instruction_table = myMath.compute_instruction_table(mu_list, sigma_list,hpwd,m,r,q,pwd)

	#BRIANS TEST CODE"
	test_decrypt_history(hpwd)
	#encrypted_history_file = compute_history.compute_history(history, hpwd)


	#??? Do we need to print success for the first 5 runs?
	print ("First Five Login Attempts: ")
	for i in range(5):
		print 1

	print("Account Initialized.... Subsequent login attempts: ")
	#check the rest of the user's inputs and see if he or she logged in correctly
	for i in range(5,len(user_input[0])):
		#we check each entry at this point to see if it is sucessful
		#use password to unzip instruction table
		pwd = 0

		mu_list = []
		sigma_list = []
		hpwd = 0
		history = []
		pwd = user_input[0][i]
		speeds_of_user = []
		for j in user_input[1][i]:
			if j < 10:
				speeds_of_user.append(0)
			else:
				speeds_of_user.append(1)

		hpwd = myMath.reconstruct_polynomial(instruction_table,speeds_of_user,q,r,pwd)




#Run the main function
if __name__ == '__main__':
	main()


