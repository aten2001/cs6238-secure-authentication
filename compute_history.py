
import logging
from Crypto.Cipher import AES

logging.basicConfig(filename='status.log', level=logging.DEBUG)

#This function takes in a feature list and begin to build the file.
# it will use the input as the key to encrypt the history file
def compute_history(first_five_logins, key):
    # type: (object, object) -> object
    list_features = first_five_logins[0]
    secret = first_five_logins[1]
    cipher = AES.new(key, AES.MODE_ECB)
    cipher.encrypt(secret)

def decrypt_history(encrypted_h_file,key):
    cipher = AES.new(key, AES.MODE_ECB)
    print "DO SOMETHING"


if __name__ == '__main__':
    logging.debug("INSIDE OF THE COMPUTE HISTORY FILE")







