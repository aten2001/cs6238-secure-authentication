#!/usr/bin/python
import input_parser, sys, init_history, compute_history, myMath, logging

logging.basicConfig(filename='status.log', level=logging.DEBUG)

#Unit test function created during the debugging of the history file encryption
def test_decrypt_encrypt_string(key):
	message = "Brian Is the Man!"
	logging.debug("Testing the Encrypt and Decrypt functionality of a string")
	logging.debug("ORIGINAL MESSAGE: " + message)
	cipher_text = compute_history.encrypt_string(message, key)
	logging.debug("CIPHER TEXT: " + cipher_text)
	logging.debug("Decrypted Cipher Text: " + compute_history.decrypt_string(cipher_text, key))

#Unit test function created during the debugging of the history file encryption
def test_decrypt_encrypt_feature_array(key, list_features):
	logging.debug("\n\n")
	logging.debug("UNENCRYPTED FEATURES: \n"+str(list_features))
	encrypted_features = compute_history.encrypt_list_features(list_features,key)
	logging.debug("ENCRYPTED FEATURES: \n"+str(encrypted_features))
	logging.debug("Decrypted Features: \n"+str(compute_history.decrypt_list_features(encrypted_features,key)))
	logging.debug("\n\n")


def main():
	# open the input file for reading, and examine
	error_correction = int(sys.argv[3]) #error correction flag
	x = sys.argv[1]
	size_of_history = sys.argv[2] #size of history file
	history_file_demo = False
	custom_key = ""
	if len(sys.argv) > 4:
		#run the program and only show encryption and decryption of history file
		history_file_demo = True
		custom_key = sys.argv[4]

	user_input = input_parser.parse(x) #build a table of all the user input
	m = len(user_input[1][0])

	# store the user's input passwords and build the first history table
	history = init_history.initialize_history(user_input,size_of_history)

	# will compute the history of the user's input and creates a history file
	# need to choose a random hardened password and r and q
	pwdArray = myMath.choose_hpwd() #this function generates all the random numbers needed for the assignment
	hpwd = pwdArray[0]

	q = pwdArray[1]
	r = pwdArray[2]

	# will return a list of mus per feature
	mu_list = myMath.compute_mu_list(history)
	sigma_list = myMath.compute_sigma_list(history)
	pwd = user_input[0][0] #takes password from teh user, known to be correct
	master_pwd = pwd

	#this is where we store the pwd and hpwd, since our Lagrange function does not function properly
	master_hpwd = hpwd

	# figures out if we are slow or fast and computes the instruction table.
	instruction_table = myMath.compute_instruction_table(mu_list, sigma_list, hpwd, m, r, q, pwd)

	#the answers list saves the values for us, so we can complete our work around for the Lagrange function
	answers_list = instruction_table[1]
	instruction_table = instruction_table[0]

	#now we encrypt
	encrypted_history_file = compute_history.encrypt_history_data_structure(history,hpwd)

	# compute_history.write_to_disk(encrypted_history_file)
	# will demonstrate that the history file is encrypted and decrypted correctly
	if history_file_demo:
		encrypted_history_file = compute_history.encrypt_history_data_structure(history, custom_key)
		compute_history.demostrate_history_file(encrypted_history_file, custom_key)

	for i in range(5):
		print 1

	second_time = False
	# check the rest of the user's inputs and see if he or she logged in correctly
	for i in range(5, len(user_input[0])): #this list iterates through all the remaining attemps and allows or denies them

		#these next lines clear out any saved data in our system, so the security check is done safetly
		mu_list = []
		sigma_list = []
		hpwd = 0
		history = []
		pwd = user_input[0][i]
		speeds_of_user = []

		#this inspects the users input to determine if they were either fast or slow on their enteries for each feature
		for j in user_input[1][i]:
			if j < 10:
				speeds_of_user.append(0)
			else:
				speeds_of_user.append(1)

		#now we use the values to attempt to reconstruct the hpwd
		hpwd = myMath.reconstruct_polynomial(instruction_table, speeds_of_user, q, r, pwd)

		#this is again part of the work around we are doing
		login_attempt = True

		#this is where the work around is for the hpwd setup
		for k in range(len(speeds_of_user)):
			if answers_list[k]!=-1:
				if answers_list[k]!=speeds_of_user[k]:
					login_attempt=False
					break

		#checks the password directly for a match
		if master_pwd!=pwd:
			login_attempt=False

		#if our secondary check passes, we allow the login to take the correct hpwd
		if login_attempt:
			hpwd = master_hpwd

		decrypted_history_file = compute_history.decrypt_history_data_structure(encrypted_history_file, hpwd)

		#here we check for the token, and then update the entire history list and rebuild the instruction table
		if decrypted_history_file[1]=="Nice Work!":

			decrypted_history_file = compute_history.update_history_file(decrypted_history_file,user_input[1][i])
			mu_list = myMath.compute_mu_list(decrypted_history_file)
			sigma_list = myMath.compute_sigma_list(decrypted_history_file)
			pwdArray = myMath.choose_hpwd()

			#here we choose a new random value r
			r = pwdArray[2]
			instruction_table = myMath.compute_instruction_table(mu_list, sigma_list, hpwd, m, r, q, pwd)

			#this updates the tables we are saving in teh system
			answers_list = instruction_table[1]
			instruction_table = instruction_table[0]

			encrypted_history_file = compute_history.encrypt_history_data_structure(decrypted_history_file, hpwd)

			#this simply clears the history file so an attacker cannot gain access
			decrypted_history_file = ""
			print 1

		#this function implements our error correction for the test case files
		elif(master_pwd==pwd and error_correction): #this is where we try error reduction
			login_sucess = False
			login_attempt = True
			speeds_of_user2 = []

			#this copies a version of the user speeds for us to vary
			for item in speeds_of_user:
				speeds_of_user2.append(item)

			#now we vary each feature speed one at a time to see if it will be successful
			for l in range(len(speeds_of_user)):
				login_attempt = True
				speeds_of_user = []
				for item in speeds_of_user2:
					speeds_of_user.append(item)

				#this next set alters the value of the feature speed gathered from the user
				if speeds_of_user[l]==0:
					speeds_of_user[l] = 1
				else:
					speeds_of_user[l] = 0

				#now we rerun our login attempt to see if the new value works
				for k in range(len(speeds_of_user)):
					if answers_list[k] != -1:
						if answers_list[k] != speeds_of_user[k]:

							login_attempt = False
							break
				if login_attempt:
					hpwd = master_hpwd

				decrypted_history_file = compute_history.decrypt_history_data_structure(encrypted_history_file, hpwd)

				#this again checks to see if the value was a success, and if it was, then updates the history file and builds a new instruction table
				#this is the same as the code above, other than at the bottom
				if decrypted_history_file[1]=="Nice Work!":

					decrypted_history_file = compute_history.update_history_file(decrypted_history_file,user_input[1][i])
					mu_list = myMath.compute_mu_list(decrypted_history_file)
					sigma_list = myMath.compute_sigma_list(decrypted_history_file)
					pwdArray = myMath.choose_hpwd()
					r = pwdArray[2]
					instruction_table = myMath.compute_instruction_table(mu_list, sigma_list, hpwd, m, r, q, pwd)
					answers_list = instruction_table[1]
					instruction_table = instruction_table[0]
					encrypted_history_file = compute_history.encrypt_history_data_structure(decrypted_history_file, hpwd)
					decrypted_history_file = ""
					print 1
					login_sucess = True
					second_time = False
					#here we break out of the loop of checking new combinations of answers, since we already found one that works
					break

			#this code will execute if we were unable to make a correction that allows entry, and prints a 0 to indicate this
			if (not login_sucess) and second_time:
				print 0
				#second_time = False
			if (not login_sucess) and (not second_time):
				print 0
				#second_time = True

		#this else is reached if error correction is off, and simply prints a failure for the user
		else:
			print 0
			#if second_time:
			#	print 0
			#	second_time = False
			#else:
			#	second_time = True
# Run the main function
if __name__ == '__main__':
	main()
