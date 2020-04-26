import csv

preferences_file_name = 'Term2lessonpreferencesKeyInfo.csv'
fieldnames = ["Child Name", 'Monday Start', 'Monday End', 'Tuesday Start', 'Tuesday End', 'Wednesday Start', 'Wednesday End', 'Thursday Start', 'Thursday End']

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']

names = []
monday_starts = []
monday_ends = []
tuesday_starts = []
tuesday_ends = []
wednesday_starts = []
wednesday_ends = []
thursday_starts = []
thursday_ends = []

def test():
	
	return('Test passes')

def options_counter(day_list):
	item_counter = 0
	#counts all the options (items that are not None)
	for i in day_list:
		if i:
			item_counter += 1
	return item_counter

def converts_nones(item):
	if item == 'None':
		return None

	else:
		return item

def find_least_popular_day():
	days_dict = {	'Monday'	: monday_starts,
				'Tuesday'	: tuesday_starts,
				'Wednesday'	: wednesday_starts,
				'Thursday'	: thursday_starts	}

	#print(f'sorted days {sorted(days)}')

	days_sorted = sorted(days, key=lambda day: options_counter(days_dict[day]), reverse=True)

	#print(days_sorted)
	least_popular_day = days_sorted[-1]
	return(least_popular_day, days_sorted, days_dict)

def extracting_info_from_file(preferences_file_name):
	csvfile = open(preferences_file_name)
	reader = csv.DictReader(csvfile)
	for row in reader:
		name, row_monday_start, row_monday_end, row_tuesday_start, row_tuesday_end, row_wednesday_start, row_wednesday_end, row_thursday_start, row_thursday_end = [row[x] for x in fieldnames]
		#print(name, row_monday_start, row_monday_end)
		names.append(row['Child Name'])

		monday_starts.append(converts_nones(row_monday_start))
		monday_ends.append(converts_nones(row_monday_end))
		tuesday_starts.append(converts_nones(row_tuesday_start))
		tuesday_ends.append(converts_nones(row_tuesday_end))
		wednesday_starts.append(converts_nones(row_wednesday_start))
		wednesday_ends.append(converts_nones(row_wednesday_end))
		thursday_starts.append(converts_nones(row_thursday_start))
		thursday_ends.append(converts_nones(row_thursday_end))

extracting_info_from_file(preferences_file_name)

least_popular_day, days_sorted, days_dict = find_least_popular_day()
print(least_popular_day)



#print(test())
