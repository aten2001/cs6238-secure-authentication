import myMath
#list of attempts is the user entered input in the form of a 2 dimensional array.
# [x][y] where x is password and y is the feature value
def initialize_history(list_of_attempts,size_of_history):
	padding_entry = []
	history_list = []
	for i in range(5):
		history_list.append(list_of_attempts[1][i])
	history_list = [history_list, "Nice Work!"]
	if size_of_history == '6':
		avg = myMath.compute_mu_list(history_list)
		new_history = [avg.tolist()]
		for item in history_list[0]:
			new_history.append(item)
		return [new_history,"Nice Work!"]
	return history_list


	return

if __name__ == '__main__':
	array = []
	for i in range(5):
		tempArray = []
		for j in range(5):
			tempArray.append(i*3)
		array.append(tempArray)
	initialize_history(["holder",array])
