
import logging, main
from Crypto.Cipher import AES
from Crypto.Hash import MD5

logging.basicConfig(filename='history_file.log', level=logging.DEBUG)

#takes in a long value and converts it to an acceptable string key for AES
def prepareKey(key):
    h = MD5.new()
    h.update(str(key))
    mykey = h.hexdigest()
    return mykey



#This function takes in a feature list and begin to build the file.
# it will use the input as the key to encrypt the history file
def encrypt_string(secret, key):
    cipher = AES.new(prepareKey(key), AES.MODE_ECB)
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    s = pad(str(secret))
    encrypted_value = cipher.encrypt(s)
    return encrypted_value

#will take in a list of features and encrypt every feature individually
def encrypt_list_features(list_features,key):
    encrypted_features = []
    for feature in list_features:
        encrypted_features.append(encrypt_string(feature,key))
    return encrypted_features

def decrypt_list_features(list_encrypt_features,key):
    decrypted_features = []
    for feature in list_encrypt_features:
        decrypted_features.append(decrypt_string(feature,key))

    return decrypted_features


def decrypt_string(encrypted_h_file, key):
    h = MD5.new()
    h.update(str(key))
    mykey = h.hexdigest()
    cipher = AES.new(mykey, AES.MODE_ECB)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    plaintext_history_file = cipher.decrypt(encrypted_h_file)
    logging.debug("DECRYPTED STRING: "+ plaintext_history_file)
    return unpad(plaintext_history_file)

def encrypt_double_array_features(dub_array_features, key):
    encrypted_dub_array = []
    for list in dub_array_features:
        encrypted_dub_array.append(encrypt_list_features(list,key))
    return encrypted_dub_array

def decrypt_double_array_features(encrypted_double_array, key):
    decr_dub_array_features = []
    for list in encrypted_double_array:
        decr_dub_array_features.append(decrypt_list_features(list,key))
    return decr_dub_array_features


def encrypt_history_data_structure(history_data_structure,key):
    encrypted_h_data_structure = []
    dub_arrays  = history_data_structure[0]
    encrypt_features = encrypt_double_array_features(dub_arrays,key)
    encrypted_h_data_structure.append(encrypt_features)
    encrypted_h_data_structure.append(encrypt_string(history_data_structure[1],key))

    return encrypted_h_data_structure

def decrypt_history_data_structure(encrypted_history_file, key):
    decrypted_h_data_structure = []
    list_encrypted_features = encrypted_history_file[0]
    decrypted_features = decrypt_double_array_features(list_encrypted_features,key)
    decrypted_h_data_structure.append(decrypted_features)
    print "ENCRYPTED Final string:  " +encrypted_history_file[1]
    decrypted_final_string = decrypt_string(encrypted_history_file[1],key)
    decrypted_h_data_structure.append(decrypted_final_string)
    return decrypted_h_data_structure

def write_to_disk(encrypted_history_file):
    with open('encrypted_history_file.txt','w') as history_file:
        list_features = encrypted_history_file[0]
        for list in list_features:
            for feature_val in list:
                history_file.write(feature_val)
        final_string = encrypted_history_file[1]
        history_file.write(final_string)

def decrypt_history_file_from_disk():
    with open('encrypted_history_file.txt','r') as history_file:
        for line in history_file:
            logging.debug("FEATURE VAL: "+ line)




if __name__ == '__main__':
    print "history file before encryption: "

    decrypt_history_file_from_disk()






