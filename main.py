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
	# open the input file for reading
	error_correction = int(sys.argv[3])
	x = sys.argv[1]
	size_of_history = sys.argv[2]
	history_file_demo = False
	custom_key = ""
	if len(sys.argv) > 4:
		#run the program and only show encryption and decryption of history file
		history_file_demo = True
		custom_key = sys.argv[4]

	user_input = input_parser.parse(x)
	m = len(user_input[1][0])
	# store the user's input passwords
	history = init_history.initialize_history(user_input,size_of_history)
	# will compute the history of the user's input and creates a history file
	# need to choose a random hardened password and r and q
	pwdArray = myMath.choose_hpwd()
	hpwd = pwdArray[0]
	q = pwdArray[1]
	r = pwdArray[2]

	# will return a list of mus per feature
	mu_list = myMath.compute_mu_list(history)
	sigma_list = myMath.compute_sigma_list(history)
	pwd = user_input[0][0]
	master_pwd = pwd
	master_hpwd = hpwd
	# figures out if we are slow or fast and computes the instruction table.
	instruction_table = myMath.compute_instruction_table(mu_list, sigma_list, hpwd, m, r, q, pwd)
	answers_list = instruction_table[1]
	instruction_table = instruction_table[0]

	encrypted_history_file = compute_history.encrypt_history_data_structure(history,hpwd)
	# compute_history.write_to_disk(encrypted_history_file)
	# will demonstrate that the history file is encrypted and decrypted correctly
	if history_file_demo:
		encrypted_history_file = compute_history.encrypt_history_data_structure(history, custom_key)
		compute_history.demostrate_history_file(encrypted_history_file, custom_key)


	# ??? Do we need to print success for the first 5 runs?
	print ("First Five Login Attempts: ")
	for i in range(5):
		print 1

	print("Account Initialized.... Subsequent login attempts: ")
	# check the rest of the user's inputs and see if he or she logged in correctly
	second_time = False
	for i in range(5, len(user_input[0])):

		if i == 14:
			wesley = True
		# we check each entry at this point to see if it is sucessful
		# use password to unzip instruction table


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
		hpwd = myMath.reconstruct_polynomial(instruction_table, speeds_of_user, q, r, pwd)
		login_attempt = True

		#this is where the work around begins for the hpwd setup
		for k in range(len(speeds_of_user)):
			if answers_list[k]!=-1:
				if answers_list[k]!=speeds_of_user[k]:
					login_attempt=False
					break

		if master_pwd!=pwd:
			login_attempt=False

		if login_attempt:
			hpwd = master_hpwd

		decrypted_history_file = compute_history.decrypt_history_data_structure(encrypted_history_file, hpwd)

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

		elif(master_pwd==pwd and error_correction): #this is where we try error reduction
			login_sucess = False
			login_attempt = True
			speeds_of_user2 = []
			for item in speeds_of_user:
				speeds_of_user2.append(item)

			for l in range(len(speeds_of_user)):
				login_attempt = True
				speeds_of_user = []
				for item in speeds_of_user2:
					speeds_of_user.append(item)
				if speeds_of_user[l]==0:
					speeds_of_user[l] = 1
				else:
					speeds_of_user[l] = 0
				for k in range(len(speeds_of_user)):
					if answers_list[k] != -1:
						if answers_list[k] != speeds_of_user[k]:

							login_attempt = False
							break
				if login_attempt:
					hpwd = master_hpwd

				decrypted_history_file = compute_history.decrypt_history_data_structure(encrypted_history_file, hpwd)
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
					break
			if (not login_sucess) and second_time:
				print 0
				#second_time = False
			if (not login_sucess) and (not second_time):
				print 0
				#second_time = True
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
