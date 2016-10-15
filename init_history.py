#list of attempts is the user entered input in the form of a 2 dimensional array.
# [x][y] where x is password and y is the feature value
def initialize_history(list_of_attempts):

    history_list = []
    for i in range(5):
        history_list.append(list_of_attempts[1][i])

    return [history_list,"Nice Work!"]

