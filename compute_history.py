
import logging
from Crypto.Cipher import AES

#This function takes in a feature list and begin to build the file.
# it will use the input as the key to encrypt the history file
def compute_history(first_five_logins, key):
    # type: (object, object) -> object
    encyrpted_history_file = [[0 for x in range(first_five_logins[0])] for y in range(2)]
    cipher = AES.new(key, AES.MODE_ECB)
    cipher.encrypt(first_five_logins[1])






