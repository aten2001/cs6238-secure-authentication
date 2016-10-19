import random
import numpy
import math
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util import number
import logging
import scipy.interpolate as interpolate

logging.basicConfig(filename='status.log', filemode='w', level=logging.DEBUG)

#these are the constant values we were given in the assignment
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

#this is a test function used to debug SolveForY
def testSolveForY():
	coefficientsList = [2,3,7]
	x = 3
	listA = [3,4,2,1]
	xA = 1
	logging.debug("testing Solve For Y")
	logging.debug("expected value 34, actual value: "+ str(solveForY(coefficientsList,x)))
	logging.debug("expected value 10, actual value: "+str(solveForY(listA,xA)))

#during the intitialization phase of the user's first five inputs, we need to generate a random hpwd
def choose_hpwd():
	#choose a q that is 160 bits or smaller randomly
	q =number.getPrime(160)

	#also choose an r and hpwd for the project
	r = random.randint(0, 2 ** 160 - 1)
	hpwd = random.randint(0,int(q/4)) #generates a random number that is less than q

	h = 6 #h is the number of previous login attempts to store in the history file
	return [hpwd,q,r]

#this computes the mean times of each feature of the history file to be used in determining if someone is distinct on a given feature
def compute_mu_list(h):
	x = numpy.mean(h[0],axis=0)
	answer = []
	for i in range(len(h[0])):
		sum1 = 0
		for itm in h[0][i]:
			sum1 = sum1 + itm
		answer.append(sum1/len(h[0][i]))
	return x

#this computes the standard deviation of times of each feature of the history file to be used in determining if someone is distinct on a given feature
def compute_sigma_list(h):
	x = numpy.std(h[0],axis=0)
	return x

#this is the controlling function which generates our instruction table
def compute_instruction_table(mu_list,sigma_list,hpwd, m, r ,q,pwd):

	#first need to create a polynomial function so we can create pairs
	coefficientsList = polynomial_creation(hpwd,m)

	# next generate a table of all correct values of the x,y pairings in a double array for both alpha and beta sides
	instruction_table = calculate_instruction_table(coefficientsList, pwd, r, q,mu_list,sigma_list)


	return instruction_table

#this function will take in the hpwd, and generate a list of coefficients randomly that will by used as our function
def polynomial_creation(hpwd, m):
	polynomial_list = []
	for i in range(0,m-1):
		#polynomial_list.append(random.randint(0,2**63))
		polynomial_list.append(random.randint(0,10))

	polynomial_list.append(hpwd)
	return polynomial_list



#this method generate hpwd from a users speeds, using the instruction table
def reconstruct_polynomial(instruction_table,speeds_of_user,q,r,pwd):
	y_list = []
	x_list = []

	#this next loop checks to see if a user is fast or slow, and chooses the coorespding entrie on the alpha or beta side of the instruction table
	for i in range(len(speeds_of_user)):
		if speeds_of_user[i] == 0:
			alpha = instruction_table[0][i]
			y_list.append((alpha - G(2*(i+1),r,pwd))%q)
			x_list.append(Pr(2*(i+1),r))

			y = (alpha - G(2*(i+1),r,pwd))%q
			x = Pr(2*(i+1),r)
		else:
			beta = instruction_table[1][i]
			y_list.append((beta - G(2*(i+1)+1, r, pwd))%q)
			x_list.append(Pr(2*(i+1)+1,r))

			y = (beta - G(2*(i+1)+1, r, pwd))%q
			x = Pr(2*(i+1)+1,r)

		#this is storing the x,y value pairs we recreate from our table, to demo their correctness to the TA
		#these are not used in any way within our system
		with open('xy_table.txt', 'a') as myFile:
			myFile.write('' + str(y) + '\n\n' + str(x) + '\n\n')

	#hpwd = Lagrange(x_list,y_list,q)
	#li = interpolate.barycentric_interpolate(x_list,y_list,0)
	#hpwd = li
	hpwd = 0

	return hpwd

#the G function is using a MD5 hash for implementation
def G(message,r,pwd):

	#this converts our pwd into a number value for use in our system
	pwd = ''.join(str(ord(c)) for c in pwd)
	pwdInt = int(pwd)

	#we create a unique key which is a combination of the pwd and our random r value, as described in the paper
	key = pwdInt ^ r

	#now we use the password to act as the key for our hash
	key = str(key)
	h = MD5.new()
	h.update(key)
	key = h.hexdigest()
	x = int(key, 16)

	return x

#this function uses a AES cipher to create a permutation that works in selecting our x values, as per the research papers direction
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
	#return testValue

	return message

#this function checks to see if a specific feature is distinguishing for further processing
def isFeatureDistinguishing(mu,sigma):
	x = mu - t
	if x < 0:
		x = -1 * x

	y = k*sigma
	if x>k*sigma:
		if x-(k*sigma)>0.01:
			return True
	return False

#this function decides if a distinguishing feature is considered fast (or the alpha side of the table)
def isFeatureFast(mu,sigma):
	x = mu + k*sigma
	if mu + k*sigma < t:
		return True
	return False

#this function will take in all our coefficients (the polynomial function) and return our XY value pairs
def calculate_instruction_table(coefficientsList, pwd, r, q, mu_list,sigma_list):
	logging.info("BUILDING INSTRUCTION TABLE")
	#calculate for the number of features, then pad the rest of the values to a set number
	num_features = len(coefficientsList)
	instruction_table=[[0 for x in range(num_features)] for y in range(2)]
	i = 1
	answers_list = []

	#this steps each feature in the instruction table and populates alpha and beta with the correct values
	for coefficient in range(num_features):

		alpha_x = Pr(2*i,r)%q
		beta_x = Pr(2*i+1,r)%q

		alpha_y = solveForY(coefficientsList,alpha_x)
		beta_y = solveForY(coefficientsList,beta_x)

		#this is used to save all x,y values used to calculate the instruction tables, to show the TA during the demo that we are able to get the correct values of x and y
		#this file is not used anywhere in our code
		with open('alpha_instruction_table.txt', 'a') as myFile:
			myFile.write(''+str(alpha_y)+'\n\n'+str(alpha_x)+'\n\n')

		with open('beta_instruction_table.txt', 'a') as myFile:
			myFile.write(''+str(beta_y)+'\n\n'+str(beta_x)+'\n\n')


		alpha = (alpha_y + G(2*i,r,pwd))%q

		beta = (beta_y + G(2 * i + 1, r, pwd))%q

		# if the feature is distinguishing only populate one side of the table with a correct value
		if isFeatureDistinguishing(mu_list[i-1],sigma_list[i-1]) == False:
			instruction_table[0][coefficient] =	alpha
			instruction_table[1][coefficient] = beta
			answers_list.append(-1)

		#if the feature is fast only populate the alpha value with correct
		elif isFeatureFast(mu_list[i-1],sigma_list[i-1]):
			instruction_table[0][coefficient] = alpha
			instruction_table[1][coefficient] = random.randint(0,2**159)
			answers_list.append(0)
		#if the feature is slow, only populate the beta value
		else:
			instruction_table[0][coefficient] = random.randint(0, 2 ** 159)
			instruction_table[1][coefficient] = beta
			answers_list.append(1)
		i = i+1
	return [instruction_table,answers_list]

##########################Creating the Test Functions##############

def testIsFeatureDistinguishing():
	logging.debug("TESTING isFeatureDistinguishing()")
	logging.debug("Expected Value: True actual value: "+ str(isFeatureDistinguishing(20,2)))
	logging.debug("Expected Value: False actual value: "+ str(isFeatureDistinguishing(20,10)))

def testIsFeatureFast():
	logging.debug("Testing isFeatureFast()")
	logging.debug("Expected Value: True actual value: " + str(isFeatureFast(5,1)))
	logging.debug("Expected Value: False actual value " + str(isFeatureFast(3,5)))

###########################Test function end#######################

#this is our lambda function from teh paper, which deals with the x values from our x,y pairs and returns the fraction to our Lagrange function
def lamb(x_array,i):
	mult = 1
	for j in range(len(x_array)):
		if j!=i:
			mult = mult*(x_array[j]/(x_array[j]-x_array[i]))
	return mult

#this is our Lagrange function, which takes x,y pairs and q to recreate hpwd
def Lagrange(x_array, y_array,q):
	sum = 0
	for i in range(len(y_array)):
		test = y_array[i]%q
		test1 = y_array[i]
		#this calls the lambda function which creates uses the x values to create the coefficient to multiply y with
		lam = lamb(x_array,i)
		#sum = sum + lam*(y_array[i]%q) #wrong way I believe

		#sum = (sum + lam * y_array[i]) % q
		#sum = sum + (lam*y_array[i])%q #this might be correct
		#sum = sum + ((lam%q) * y_array[i])  # this might be correct
		#this is where we sum the array
		sum = sum + (lam * y_array[i])
	#sum = sum%q
	return sum
	#return sum%q #wrong return



if __name__ == '__main__':
	solveForY([2,3,4], 2)
	value = Pr(100, 200)
	testIsFeatureDistinguishing()
	testIsFeatureFast()

	#encrypt_instruction_table([], 0, 0)
	#testSolveForY()