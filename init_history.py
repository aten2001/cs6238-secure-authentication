#list of attempts is the user entered input in the form of a 2 dimensional array.
# [x][y] where x is password and y is the feature value
def initialize_history(list_of_attempts):
	padding_entry = []
	history_list = []
	for i in range(len(list_of_attempts[1][0])):
		padding_entry.append(10)
	history_list.append(padding_entry)
	for i in range(5):
		history_list.append(list_of_attempts[1][i])


	return [history_list,"Nice Work!"]

if __name__ == '__main__':
	array = []
	for i in range(5):
		tempArray = []
		for j in range(5):
			tempArray.append(i*3)
		array.append(tempArray)
	initialize_history(["holder",array])
