


#This function takes in a feature list and begin to build the file.
# it will use the input as the key to encrypt the history file
def compute_history(first_five_logins, key):
    # type: (object, object) -> object

    with open('history-file.txt', 'w') as f:
        for features in first_five_logins:
            f.write(str(features))
    print "DO SOMETHING HERE"


