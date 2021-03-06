
import logging, main, csv,sys
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import myMath
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


#encrypts the history file list object so that an attacker can not gain information on a user's password
#length
def strong_encrypt_list_features(list_features,key):
    encrypted_features = []
    first_string = list_features[0]
    csv = str(first_string)
    for i in range(1,len(list_features)):
        feature = list_features[i]
        csv = csv + ","+ str(feature)
    cipher_text = encrypt_string(csv,key)
    encrypted_features.append(cipher_text)
    plain_text = decrypt_string(cipher_text,key)
    return encrypted_features

#decrypts a given list object of features and returns as a list object where each entry in the
#list is a different feature value
def strong_decrypt_list_features(list_features,key):
    decrypted_features = []
    cipher_text = list_features[0]
    plain_text = decrypt_string(cipher_text,key)
    return plain_text.split(",")

#takes in a list of features and encrypts each individual feature in the string
def decrypt_list_features(list_encrypt_features,key):
    decrypted_features = []
    for feature in list_encrypt_features:
        decrypted_features.append(decrypt_string(feature,key))

    return decrypted_features

# takes in a cipher text string and key
# returns the unencrypted version of the string
def decrypt_string(cipher_text, key):
    cipher = AES.new(prepareKey(key), AES.MODE_ECB)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    plaintext_history_file = cipher.decrypt(cipher_text)
    logging.debug("DECRYPTED STRING: "+ plaintext_history_file)
    return unpad(plaintext_history_file)

#takes in a double array data structure of plaintext features and will encrypt them using the given keys
def encrypt_double_array_features(dub_array_features, key):
    encrypted_dub_array = []
    for list in dub_array_features:
        encrypted_dub_array.append(strong_encrypt_list_features(list,key))
    return encrypted_dub_array

#takes in an encrypted double array feature
def decrypt_double_array_features(encrypted_double_array, key):
    decr_dub_array_features = []
    for list in encrypted_double_array:
        #BRIAN made changes here to support the more secure encryption of the history file
        decr_dub_array_features.append(strong_decrypt_list_features(list,key))
    return decr_dub_array_features

#takes in a data structure that stores history file data and encrypts it.
#Returns the data structure with all encrypted values
def encrypt_history_data_structure(history_data_structure,key):
    encrypted_h_data_structure = []
    dub_arrays  = history_data_structure[0]
    encrypt_features = encrypt_double_array_features(dub_arrays,key)
    encrypted_h_data_structure.append(encrypt_features)
    encrypted_h_data_structure.append(encrypt_string(history_data_structure[1],key))

    return encrypted_h_data_structure

# Takes in a history file data structure and encrypts all the values. Will return the
# the features in decrypted format
def decrypt_history_data_structure(encrypted_history_file, key):
    decrypted_h_data_structure = []
    list_encrypted_features = encrypted_history_file[0]
    decrypted_features = decrypt_double_array_features(list_encrypted_features,key)
    decrypted_h_data_structure.append(decrypted_features)
    decrypted_final_string = decrypt_string(encrypted_history_file[1],key)
    decrypted_h_data_structure.append(decrypted_final_string)
    return decrypted_h_data_structure


#This function will update the history file data structure, with the newly created feature values from the most recent
#login attempt.
def update_history_file(history_file,new_times):
    new_history = []
    for i in range(1,len(history_file[0])):
        for j in range(len(history_file[0][i])):
            history_file[0][i][j] = int(history_file[0][i][j])
        new_history.append(history_file[0][i])
    new_history.append(new_times)
    history_file[0] = new_history
    return history_file

#test function that was written during the development of the
#encryption
def testStrongEncryptFeatures(key):
    features = [1,2,3,4,6,1,2,3,5]

    myFeatures = strong_encrypt_list_features(features,key)

    plain_text = strong_decrypt_list_features(myFeatures,key)
    print plain_text

#takes in a string and writes it to an output file for demonstration purposes
def writeStringToFile(text):
    with open('history-file-demo.txt', 'a') as f:
        f.write(str(text)+"\n")

#Function used to demonstrate the decryption of the history file using a random key
def print_decrypted_history_file(decrypted_history_file):
    writeStringToFile("DECRYPTED HISTORY FILE OBJECT")
    for object in decrypted_history_file:
        writeStringToFile(object)

#Function used to demonstrate the encryption of the history file of a random key
def print_encrypted_history_file(encrypted_history_file):
    writeStringToFile("ENCRYPTED TEXT FILE OBJECT")
    for object in encrypted_history_file:
        writeStringToFile(object)

#Function used to demonstrate the encryption and decryption of a history file
def demostrate_history_file(encrypted_history_file,custom_key):
    with open('history-file-demo.txt', 'w') as f:
        f.write("DEMO OF HISTORY FILE\n")
    print_encrypted_history_file(encrypted_history_file)
    decrypted_history_file = decrypt_history_data_structure(encrypted_history_file,custom_key)
    print_decrypted_history_file(decrypted_history_file)


if __name__ == '__main__':
    testStrongEncryptFeatures(sys.argv[1])







