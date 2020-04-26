import csv
from pprint import pprint

preferences_file_name = 'Term2lessonpreferencesEXAMPLE.csv'
fieldnames = ["Child Name", 'Monday Start', 'Monday End', 'Tuesday Start', 'Tuesday End', 'Wednesday Start', 'Wednesday End', 'Thursday Start', 'Thursday End']

days = set([]) 	#SET

lists_dictionary = {}
secondary_lists_dictionary = {}

emergency_stop = 0

def test():
	assert increment_timeslot('1000') == '1030'
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

	if len(start_days_dict[least_popular_day]) < 1:
		print("54!!!!!!\n\n\n\n")
		least_popular_day = days_sorted[-2]
	pprint(start_days_dict[least_popular_day])
	#return(least_popular_day, days_sorted, start_days_dict)
	return(least_popular_day)

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
		

def find_min_and_max_time(day, time):
	secondary_lists_dictionary[f'{day}_{time}s_times'] = []
	for i in range(len(lists_dictionary[f'{day}_{time}s'])):
		item = lists_dictionary[f'{day}_{time}s'][i]
		if item:
			secondary_lists_dictionary[f'{day}_{time}s_times'].append(int(item))
		

	pprint(secondary_lists_dictionary[f'{day}_{time}s_times'])

	maximum = max(secondary_lists_dictionary[f'{day}_{time}s_times'])
	minimum = min(secondary_lists_dictionary[f'{day}_{time}s_times'])
	#print(f"max {day}_{time}s_times: {maximum}")
	#print(f"min {day}_{time}s_times: {minimum}")
	return minimum, maximum

def setup_blank_timetable(days=days):
	timetable = {}
	times = []


	for day in days:
		timetable[day] = {}
		for time in range(1000, 2000, 50):
			if str(time)[-2:] == '50':
				time -= 20
			#times.append(time)
			timetable[day][time] = None
	#pprint(timetable)
	return(timetable)


def remove_student(student_index):
	for l in lists_dictionary:		#list in list_dictionary
		#print(f'LINE 107: {lists_dictionary[l][student_index]}')
		
		try:
			item = lists_dictionary[l][student_index]
			lists_dictionary[l].remove(item)
		except IndexError:
			print(f'IndexError - List {lists_dictionary[l]} did not have index {student_index}')
		
		except ValueError:
			print(f'ValueError - List {lists_dictionary[l]} did not have index {student_index}')

	#pprint(lists_dictionary)

def find_student_info(student_index, lists_dictionary=lists_dictionary):
	info = {}
	for l in lists_dictionary:		#list in list_dictionary
		#print(f'LINE 107: {lists_dictionary[l][student_index]}')
		print(l)
		try:
			item = {lists_dictionary[l][student_index]}
			info[l] = item

		except IndexError:
			print(f'IndexError - List {lists_dictionary[l]} did not have index {student_index}')
		
		except ValueError:
			print(f'ValueError - List {lists_dictionary[l]} did not have index {student_index}')

	return(info)

def increment_timeslot(time):
	time = int(time)
	if str(time).endswith('30'):
		time += 70
		print('30!')
	else:
		time += 30

	return(str(time))



def place_student(least_popular_day=None, min_start_time=None, max_start_time=None):
	least_popular_day = find_least_popular_day()


	#find earliest start time. 
	min_start_time, max_start_time = find_min_and_max_time(least_popular_day, 'start')

	least_popular_day_list = lists_dictionary[f'{least_popular_day}_starts']
	timetable_day = timetable[least_popular_day]

	#establishing student_index
	try:
		student_index = lists_dictionary[f'{least_popular_day}_starts'].index(str(min_start_time))
	except ValueError:
		student_index = 0

	#check if timeslot is available
	if not timetable_day[min_start_time]:		#if the time is none, aka no student has taken it yet
		timetable_day[min_start_time] = lists_dictionary[f'child_names'][student_index]
		remove_student(student_index)
		pprint(timetable)


	#if timeslot isn't available, increment time slot.
	else:
		min_start_time = increment_timeslot(min_start_time)
		#rewrite new start time to correct list
		lists_dictionary[f'{least_popular_day}_starts'][student_index] = min_start_time
		pprint(f"LINE 182 {lists_dictionary[f'{least_popular_day}_starts']}")

	#if incremented timeslot is too late, remove both start and end times. 


	#give timeslot, remove the student.



	"""
	pprint(timetable)

	if not least_popular_day:
		least_popular_day = find_least_popular_day()

	least_popular_day_list = lists_dictionary[f'{least_popular_day}_starts']

	if not least_popular_day_list:
		least_popular_day = find_least_popular_day()

	elif min_start_time == None or max_start_time==None:
		min_start_time, max_start_time = find_min_and_max_time(least_popular_day, 'start')
	timetable_day = timetable[least_popular_day]
	#pprint(f'timetable_day {timetable_day}')
	print(f'154 {min_start_time}')

	print(f'LEAST POPULAR DAY LIST {least_popular_day_list}, {emergency_stop}')
	#print(least_popular_day_list.index(str(min_start_time)))
	try:
		student_index = lists_dictionary[f'{least_popular_day}_starts'].index(str(min_start_time))
	except ValueError:
		student_index = 0

	if not timetable_day[min_start_time]:		#if the time is none, aka no student has taken it yet
		timetable_day[min_start_time] = lists_dictionary[f'child_names'][student_index]
		remove_student(student_index)
		#print(student_index, timetable_day[min_start_time])

	else:
		print(f'MIN START TIME {min_start_time} ')
		#see if student can do next timeslot
		info = find_student_info(student_index)

		#test if going to next timeslot clashes with end_time
		student_end_time = lists_dictionary[f'{least_popular_day}_ends'][student_index]
		print(f'STUDENT END TIME {student_end_time}')

		#move time to next timeslot
		if student_end_time != None:
			if str(min_start_time).endswith('30'):
				min_start_time += 70
				print('30!')
			else:
				min_start_time += 30

			if min_start_time >= int(student_end_time):
				print('OH NO')
			
			else:
				lists_dictionary[f'{least_popular_day}_starts'][student_index] = min_start_time
				#place_student(least_popular_day, min_start_time, max_start_time)
		else:
			#place_student()
			print('\n')

			"""
		#pprint(f'INFO : {info}')

	#print(f'{timetable_day[min_start_time]}')



#START
extracting_info_from_file(preferences_file_name)

#pprint(lists_dictionary)

timetable = setup_blank_timetable()

pprint(timetable)

print(test())

while lists_dictionary['child_names']:
	emergency_stop += 1
	if emergency_stop < 20:
		place_student()
	else:
		print('staap')
		break
