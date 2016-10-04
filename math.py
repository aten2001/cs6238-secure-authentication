import random
#during the intitialization phase of the user's first five inputs, we need to generate a random hpwd
def choose_hpwd():
    #choose a q that is 160 bits or smaller randomly
    q =random.randint(0, 2**160 - 1)

    return q
