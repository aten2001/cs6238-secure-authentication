
import logging
from Crypto.Cipher import AES
from Crypto.Hash import MD5

logging.basicConfig(filename='status.log', level=logging.DEBUG)

#This function takes in a feature list and begin to build the file.
# it will use the input as the key to encrypt the history file
def compute_history(secret, key):
    # type: (object, object) -> object
    #list_features = first_five_logins[0]
    #secret = first_five_logins[1]
    h = MD5.new()
    h.update(str(key))
    mykey = h.hexdigest()
    cipher = AES.new(mykey, AES.MODE_ECB)
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    s = pad(str(secret))
    encrypted_value = cipher.encrypt(s)
    return encrypted_value


def decrypt_history(encrypted_h_file,key):
    h = MD5.new()
    h.update(str(key))
    mykey = h.hexdigest()
    cipher = AES.new(mykey, AES.MODE_ECB)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    plaintext_history_file = cipher.decrypt(encrypted_h_file)

    return unpad(plaintext_history_file)



if __name__ == '__main__':
    logging.debug("INSIDE OF THE COMPUTE HISTORY FILE")







