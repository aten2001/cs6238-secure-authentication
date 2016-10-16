import random
import numpy
import math
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util import number
import logging

logging.basicConfig(filename='status.log',level=logging.DEBUG)


k = 2
t=10

#takes in a random 160 bit number and returns a matching polynomial
def find_polynomial(q,num_features):
	#generate a bunch of x,y pairs
	return 0;



#takes in a polynomial represented as a list of coefficients
def solveForY(coefficientsList, x):
	degree = len(coefficientsList)-1
	sum = 0
	power_x = 1
	for coefficient in reversed(coefficientsList):
		sum = sum + coefficient * power_x
		power_x = power_x * x

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
	q =number.getPrime(160)
	r = random.randint(0, 2 ** 160 - 1)
	#TODO choose random password
	hpwd = random.randint(0,q-1) #generates a random number that is less than q
	h = 6 #h is the number of previous login attempts to store in the history file

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
	instruction_table = calculate_instruction_table(coefficientsList, pwd, r, q,mu_list,sigma_list)


	return instruction_table



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



#should return a list of coefficients
def reconstruct_polynomial(instruction_table,speeds_of_user,q,r,pwd):
	y_list = []
	for i in range(len(speeds_of_user)):
		if speeds_of_user[i] == 0:
			alpha = instruction_table[0][i]
			#g = G(2*(i+1),r,pwd)%q
			#g1 = G(2 * i, r, pwd) % q
			y_list.append(alpha - (G(2*(i+1),r,pwd)%q))
		else:
			beta = instruction_table[1][i]
			y_list.append(beta - (G((2*(i+1))- 1, r, pwd))%q)


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
	print testValue
	return testValue

def Pr(message,r):

	h = MD5.new()
	h.update(str(r))
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

def isFeatureDistinguishing(mu_list,sigma_list):
	return False

def isFeatureFast(mu_list,sigma_list):
	return False

#this function will take in all our coefficients (the polynomial function) and return our XY value pairs
def calculate_instruction_table(coefficientsList, pwd, r, q, mu_list,sigma_list):
	logging.info("BUILDING INSTRUCTION TABLE")
	#calculate for the number of features, then pad the rest of the values to a set number
	num_features = len(coefficientsList)
	instruction_table=[[0 for x in range(num_features)] for y in range(2)]
	i = 1
	for coefficient in range(num_features):

		alpha_x = Pr(2*i,r)%q
		beta_x = Pr(2*i+1,r)%q

		alpha_y = solveForY(coefficientsList,alpha_x)
		beta_y = solveForY(coefficientsList,beta_x)

		logging.debug("REPEAT")
		logging.debug(alpha_y)
		logging.debug("PART 2")
		logging.debug(beta_y)

		print "REPEAT"
		print alpha_y
		print "PART 2"
		print beta_y

		g = G(2*i,r,pwd)%q
		#g1 = G(2*i,r,pwd)%q

		alpha = alpha_y + g
		g = G(2 * i + 1, r, pwd)%q
		beta = beta_y + g
		# if the feature is distinguishing only populate one side of the table with a correct value
		if isFeatureDistinguishing(sigma_list,mu_list) == False:
			instruction_table[0][coefficient] =	alpha
			instruction_table[1][coefficient] = beta
		#if the feature is fast only populate the alpha value with correct
		elif isFeatureFast(sigma_list,mu_list):
			instruction_table[0][coefficient] = alpha
			instruction_table[1][coefficient] = random.randint(0,2**159)
		#if the feature is slow, only populate the beta value
		else:
			instruction_table[0][coefficient] = random.randint(0, 2 ** 159)
			instruction_table[1][coefficient] = beta
		i = i+1
	return instruction_table

##########################Creating the Test Functions##############

def testIsPrime():
	trueprime = 13
	falseprime = 124
	print "CRYPTO " +str(number.isPrime(13))
	print " Generating Prime: " + str(number.getPrime(160))

if __name__ == '__main__':
	value = Pr(100, 200)
	testIsPrime()
	#encrypt_instruction_table([], 0, 0)
	testSolveForY()