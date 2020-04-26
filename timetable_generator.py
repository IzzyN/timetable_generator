import csv
from pprint import pprint

preferences_file_name = 'Term2lessonpreferencesEXAMPLE3.csv'
fieldnames = ["Child Name", 'Monday Start', 'Monday End', 'Tuesday Start', 'Tuesday End', 'Wednesday Start', 'Wednesday End', 'Thursday Start', 'Thursday End']

days = set([]) 	#SET

lists_dictionary = {}
secondary_lists_dictionary = {}

emergency_stop = 0
finished = False

def test():
	assert increment_timeslot('1000') == '1030'
	assert options_for_day('monday') == True
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

def options_for_day(day):
	#checking if the day actually has options, returns True if there are options, False if not
	day_list = lists_dictionary[f'{day}_starts']
	for item in day_list:
		if item != None:
			return True
	return False

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

	if not options_for_day(least_popular_day):
		days.remove(least_popular_day)
		try:
			least_popular_day = days_sorted[-2]

		except:
			finished = True


	#pprint(start_days_dict[least_popular_day])
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

	try:
		maximum = max(secondary_lists_dictionary[f'{day}_{time}s_times'])
		minimum = min(secondary_lists_dictionary[f'{day}_{time}s_times'])
		return minimum, maximum

	except:
		print(lists_dictionary['child_names'])
	#print(f"max {day}_{time}s_times: {maximum}")
	#print(f"min {day}_{time}s_times: {minimum}")


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
			print(f'IndexError - List {l} {lists_dictionary[l]} did not have index {student_index}')
		
		except ValueError:
			print(f'ValueError - List {l} {lists_dictionary[l]} did not have index {student_index}')

	#pprint(lists_dictionary)

def remove_options(student_index, day):
	print('REMOVE OPTIONS')

	lists_dictionary[f'{day}_starts'][student_index] = None 		#removing start time


	lists_dictionary[f'{day}_ends'][student_index] = None			#removing end time


def find_student_info(student_index, lists_dictionary=lists_dictionary):
	info = {}
	for l in lists_dictionary:		#list in list_dictionary
		#print(f'LINE 107: {lists_dictionary[l][student_index]}')
		#print(l)
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

def check_timeslot(timetable_day, min_start_time, student_index):
	if not timetable_day[min_start_time]:		#if the time is none, aka no student has taken it yet
		timetable_day[min_start_time] = lists_dictionary[f'child_names'][student_index]
		remove_student(student_index)
		return True
	else:
		return False



def place_student(least_popular_day=None, min_start_time=None, max_start_time=None):
	least_popular_day = find_least_popular_day()


	#find earliest start time. 
	min_start_time, max_start_time = find_min_and_max_time(least_popular_day, 'start')

	#Get list of options
	least_popular_day_list = lists_dictionary[f'{least_popular_day}_starts']

	timetable_day = timetable[least_popular_day]

	#establishing student_index
	try:
		student_index = lists_dictionary[f'{least_popular_day}_starts'].index(str(min_start_time))
	except ValueError:
		student_index = 0

	#check if timeslot is available
	if not check_timeslot(timetable_day, min_start_time, student_index):

		#pprint(timetable)

	#if timeslot isn't available, increment time slot.
		min_start_time = increment_timeslot(min_start_time)
		#rewrite new start time to correct list
		lists_dictionary[f'{least_popular_day}_starts'][student_index] = min_start_time
		pprint(f"LINE 182 {lists_dictionary[f'{least_popular_day}_starts']}")

		try:
			if min_start_time >= lists_dictionary[f'{least_popular_day}_ends'][student_index]:		#testing if the new time is too late
				print('Time is too late!')
				#remove both start and end times
				remove_options(student_index, least_popular_day)
			else:
				check_timeslot(timetable_day, min_start_time, student_index)

		except:
			print('Issue! cannot test if too late.')
			print(min_start_time)
			print(lists_dictionary[f'{least_popular_day}_ends'][student_index])
			remove_options(student_index, least_popular_day) 		#if incremented timeslot is too late, remove both start and end times. 


	#give timeslot, remove the student.





#START
extracting_info_from_file(preferences_file_name)

#pprint(lists_dictionary)

timetable = setup_blank_timetable()

pprint(timetable)

print(test())

pprint(lists_dictionary)

while lists_dictionary['child_names']:
	emergency_stop += 1
	if emergency_stop < 100 and finished == False:
		place_student()
		#pprint(timetable)
	else:
		print('staap')
		if finished == True:
			print('Completed')
		break
