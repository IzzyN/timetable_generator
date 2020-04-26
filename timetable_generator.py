import csv
from pprint import pprint

preferences_file_name = 'Term2lessonpreferencesEXAMPLE.csv'
fieldnames = ["Child Name", 'Monday Start', 'Monday End', 'Tuesday Start', 'Tuesday End', 'Wednesday Start', 'Wednesday End', 'Thursday Start', 'Thursday End']

days = set([]) 	#SET

lists_dictionary = {}

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
		item = item.replace(':','')
		return item

def find_least_popular_day():

	start_days_dict = {}

	for key in lists_dictionary:
		for day in days:
			if day in key and 'start' in key and 'child' not in key:
				start_days_dict[day] = lists_dictionary[key]
				#print(f'DAY {day} KEY {key}')
		#print(f'KEY: {key}')

	#print(f'sorted days {sorted(days)}')

	days_sorted = sorted(days, key=lambda day: options_counter(start_days_dict[day]), reverse=True)

	#print(days_sorted)
	least_popular_day = days_sorted[-1]
	return(least_popular_day, days_sorted, start_days_dict)

def extracting_info_from_file(preferences_file_name):
	csvfile = open(preferences_file_name)
	reader = csv.DictReader(csvfile)
	for row in reader:
		for cell in row:
			day = (cell.split()[0]).lower()
			#pprint(f'day {day}')
			if 'child' not in day:
				days.add(day)
			column_name = cell.lower().replace(' ','_')

			if f'{column_name}s' in lists_dictionary:
				lists_dictionary[f'{column_name}s'] = lists_dictionary[f'{column_name}s'] + [converts_nones(row[cell])]

			else:
				list_name = f'{column_name}s'
				lists_dictionary[list_name] = [converts_nones(row[cell])]
		

def find_min_and_max_time(day):
	for time in ['start', 'end']:	
		lists_dictionary[f'{day}_{time}s_times'] = []
		lists_dictionary[f'{day}_{time}s_times_no_any'] = []
		for i in range(len(lists_dictionary[f'{day}_{time}s'])):
			item = lists_dictionary[f'{day}_{time}s'][i]
			if item:
				lists_dictionary[f'{day}_{time}s_times'] += [item]
				if item != 'Any':
					item = int(item)
					lists_dictionary[f'{day}_{time}s_times_no_any'].append(item)

		pprint(lists_dictionary[f'{day}_{time}s_times_no_any'])

	print(f"max {day}_{time}s_times_no_any: {max(lists_dictionary[f'{day}_{time}s_times_no_any'])}")
	print(f"min {day}_{time}s_times_no_any: {min(lists_dictionary[f'{day}_{time}s_times_no_any'])}")


extracting_info_from_file(preferences_file_name)

least_popular_day, days_sorted, days_dict = find_least_popular_day()

for day in days_sorted:
	find_min_and_max_time(day)

if lists_dictionary['child_names']:
	print('eww kids')

#pprint(lists_dictionary)

#print(test())
