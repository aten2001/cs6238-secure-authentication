import random

#takes in a random 160 bit number and returns a matching polynomial
def find_polynomial(q,num_features):
	#generate a bunch of x,y pairs
	return 0;

#during the intitialization phase of the user's first five inputs, we need to generate a random hpwd
def choose_hpwd():
	#choose a q that is 160 bits or smaller randomly
	q =random.randint(0, 2**160 - 1)

	return q




def compute_mu_list(h):
	return False

def compute_sigma_list(history):
	return False

def compute_instruction_table(mu_list,sigma_list,hpwd):

	#first need to create a polynomial function so we can create pairs
	coefficientsList = polynomial_creation(hpwd)

	# next generate a table of all correct values of the x,y pairings in a double array for both alpha and beta sides
	#####padding will also be inserted into our list here as well, so the length of the password is hidden
	xyPairsList = calculate_XY_pairs(coefficientsList)

	#now we will check the different feature values to determine if the user is fast or slow
	#if user is neither fast nor slow, we will insert a random value into the list that is not equal to the correct value
	instruction_table = calc_instruct_table(xyPairsList)

	return instruction_table

#possibly need this to turn into a binary array, not a python list object
def encrypt_instruction_table(instruction_table,pwd):
	return False

#decrypt the instruction table for use (might decrypt to the wrong information though)
def decrypt_instruction_table(instruction_table, pwd):
	return False

#this function will take in the hpwd, and generate a list of coefficients randomly that will by used as our function
def polynomial_creation(hpwd):
	return hpwd

#this function will take in all our coefficients (the polynomial function) and return our XY value pairs
def calculate_XY_pairs(coefficientsList):
	#calculate for teh number of features, then pad the rest of the values to a set number
	return False

#this function will take in our long list of xy pairs, replace the rows of the table that are distinct, and return our final instruction_table
def calc_instruct_table(xyPairsList):
	return False

