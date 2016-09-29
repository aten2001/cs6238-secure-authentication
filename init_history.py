
def initialize_history(list_of_attempts):
    history_list = []
    for i in range(5):

        for j in range(list_of_attempts[i,1]):

        history_list.append(list_of_attempts[i,1])
    history_list.append("Nice work!")
    return history_list

