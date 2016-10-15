import random
import numpy
import math
from Crypto.Cipher import AES
from Crypto.Hash import MD5

#takes in a random 160 bit number and returns a matching polynomial
def find_polynomial(q,num_features):
	#generate a bunch of x,y pairs
	return 0;



#takes in a polynomial represented as a list of coefficients
def solveForY(coefficientsList, x):
	degree = len(coefficientsList)-1
	sum = 0
	for coefficient in coefficientsList:
		sum = sum + coefficient * math.pow(x, degree)
		degree= degree - 1
	return sum


def testSolveForY():
	coefficientsList = [2,3,7]
	x = 3
	listA = [3,4,2,1]
	xA = 1
	print ("testing Solve For Y")
	print ("expected value 34, actual value: "+ str(solveForY(coefficientsList,x)))
	print ("expected value 10, actual value: "+str(solveForY(listA,xA)))

#during the intitialization phase of the user's first five inputs, we need to generate a random hpwd
def choose_hpwd():
	#choose a q that is 160 bits or smaller randomly
	#TODO adjust q appropriately
	q =random.randint(0, 2**160 - 1)
	r = random.randint(0, 2 ** 160 - 1)
	#TODO choose random password
	hpwd = random.randint(0,q-1) #generates a random number that is less than q
	h = 6 #h is the number of previous login attempts to store in the history file
	print "HPWD: " + str(hpwd)
	return [hpwd,q,r]


def compute_mu_list(h):
	return numpy.mean(h[0])

def compute_sigma_list(h):
	return numpy.std(h[0])

def compute_instruction_table(mu_list,sigma_list,hpwd, m, r ,q,pwd):

	#first need to create a polynomial function so we can create pairs
	coefficientsList = polynomial_creation(hpwd,m)

	# next generate a table of all correct values of the x,y pairings in a double array for both alpha and beta sides
	#####padding will also be inserted into our list here as well, so the length of the password is hidden
	xyPairsList = calculate_XY_pairs(coefficientsList,pwd,r,q)

	#now we will check the different feature values to determine if the user is fast or slow
	#if user is neither fast nor slow, we will insert a random value into the list that is not equal to the correct value
	instruction_table = calc_instruct_table(xyPairsList)

	return instruction_table

#possibly need this to turn into a binary array, not a python list object
def encrypt_instruction_table(instruction_table,pwd,r):

	obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	return False

#decrypt the instruction table for use (might decrypt to the wrong information though)
def decrypt_instruction_table(instruction_table, pwd):
	return False

#this function will take in the hpwd, and generate a list of coefficients randomly that will by used as our function
def polynomial_creation(hpwd, m):
	polynomial_list = []
	for i in range(0,m-1):
		polynomial_list.append(random.randint(0,2**63))
	polynomial_list.append(hpwd)
	return polynomial_list


#this function will take in our long list of xy pairs, replace the rows of the table that are distinct, and return our final instruction_table
def calc_instruct_table(xyPairsList):
	return False

def reconstruct_polynomial(instruction_table,speeds_of_user,q,r,pwd):
	xy_pairs = []
	for i in range(len(speeds_of_user)):
		if speeds_of_user[i] == 0:
			alpha = instruction_table[0][i]
			#y = (alpha - cipher.encrypt(cipher.encrypt(2*i)))% q

	return True

def G(message,r,pwd):

	pwd = ''.join(str(ord(c)) for c in pwd)

	pwdInt = int(pwd)

	key = pwdInt ^ r
	key = str(key)
	h = MD5.new()
	h.update(key)
	key = h.hexdigest()

	cipher = AES.new(key, AES.MODE_ECB)


	BS = 16
	pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
	s = pad(str(message))
	testValue = cipher.encrypt(cipher.encrypt(s))

	testValue = ''.join(str(ord(c)) for c in testValue)
	testValue = int(testValue)

	return testValue

def Pr(message,r):

	h = MD5.new()
	h.update(r)
	key = h.hexdigest()

	cipher = AES.new(key, AES.MODE_ECB)

	BS = 16
	pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
	s = pad(str(message))
	testValue = cipher.encrypt(cipher.encrypt(s))

	testValue = ''.join(str(ord(c)) for c in testValue)
	testValue = int(testValue)
	return testValue

def generateAlpha(i,pwd,r):
	x = Pr(2*i)
	return False

def generateBeta(i,pwd,r):
	return False



#this function will take in all our coefficients (the polynomial function) and return our XY value pairs
def calculate_XY_pairs(coefficientsList,pwd,r,q):

	#calculate for the number of features, then pad the rest of the values to a set number
	num_features = len(coefficientsList)
	instruction_table=[[0 for x in range(num_features)] for y in range(2)]
	i = 1
	for coefficient in range(num_features):
		alpha_x = Pr(2*i,r)
		beta_x = Pr(2*i+1,r)
		alpha_y = solveForY(coefficientsList,alpha_x)
		beta_y = solveForY(coefficientsList,beta_x)
		alpha = alpha_y + G(2*i,r,pwd) %q
		beta = beta_y + G(2*i+1,r,pwd) %q
		instruction_table[0][coefficient] =	alpha
		instruction_table[1][coefficient] = beta
		i = i+1
	return instruction_table


if __name__ == '__main__':
	value = G(100, 200, 'okay')

	#encrypt_instruction_table([], 0, 0)
	#testSolveForY()