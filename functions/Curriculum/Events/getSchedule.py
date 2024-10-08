import datetime

def getSchedule(class_data):
    ## Step 1: Get all class dates
    # Parse dates and other inputs from class_data
    start_date = datetime.datetime.strptime(class_data['Yearly_Schedule__r']['Start_Date__c'], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(class_data['Yearly_Schedule__r']['End_Date__c'], '%Y-%m-%d').date()
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(class_data['Day_of_Week__c'])

    # Parse holiday weeks (assuming each entry is 'XX/XX/XXXX-XX/XX/XXXX')
    holiday_weeks = class_data['Yearly_Schedule__r']['Associated_Calendar__r']['Holiday_Weeks__c'] or ""
    holiday_weeks_list = []
    for line in holiday_weeks.splitlines():
        start, end = line.split('-')
        holiday_weeks_list.append((datetime.datetime.strptime(start.strip(), '%d/%m/%Y').date(),
                                    datetime.datetime.strptime(end.strip(), '%d/%m/%Y').date()))

    # Parse holiday days
    holiday_days = class_data['Yearly_Schedule__r']['Associated_Calendar__r']['Holiday_Days__c']
    print(holiday_days)
    holiday_days_set = set(datetime.datetime.strptime(day.strip(), '%d/%m/%Y').date() for day in holiday_days.splitlines()) if holiday_days else set()

    # Parse overwrite cancelled days
    overwrite_cancelled_1 = class_data['Yearly_Schedule__r']['Overwrite_Cancelled__c'] or ""
    overwrite_cancelled_2 = class_data['Overwrite_Cancelled__c'] or ""
    cancelled_set = set(datetime.datetime.strptime(day.strip(), '%d/%m/%Y').date() for day in overwrite_cancelled_1.splitlines())
    cancelled_set.update(datetime.datetime.strptime(day.strip(), '%d/%m/%Y').date() for day in overwrite_cancelled_2.splitlines())

    # Step 1: Create list of all valid course days between start_date and end_date on the given day_of_week
    course_days = []
    current_day = start_date

    while current_day <= end_date:
        if current_day.weekday() == day_of_week:
            # Step 2: Check if the day is within a holiday week
            in_holiday_week = any(holiday_start <= current_day <= holiday_end for holiday_start, holiday_end in holiday_weeks_list)

            # Step 3: Exclude holiday days, holiday weeks, and cancelled days
            if not in_holiday_week and current_day not in holiday_days_set and current_day not in cancelled_set:
                course_days.append(current_day)

        current_day += datetime.timedelta(days=1)  # Move to the next day

    ## Step 2: Get all permanent teachers
    # Create a dictionary with course days and their corresponding teacher
    teacher_schedule = {}
    permanent_teacher = [
        {"email": class_data['Teacher__r']['Email__c'], "name": class_data['Teacher__r']['Full_Name__c']}
    ] if class_data.get('Teacher__r') else []

    # Initialize all course days with the permanent teacher
    for course_day in course_days:
        teacher_schedule[course_day] = permanent_teacher

    # Step 5: Process replacements and update teacher for relevant dates
    replacements = class_data['Replacements__r']["records"] if class_data.get('Replacements__r') else []
    # Sort replacements by date
    sorted_replacements = sorted(replacements, key=lambda r: datetime.datetime.strptime(r.get('Date__c'), '%Y-%m-%d').date())

    # Iterate through sorted replacements and update the teacher for all future dates
    for replacement in sorted_replacements:
        if replacement['RecordTypeId'] == '012P5000001QAUbIAO':
            replacement_date = datetime.datetime.strptime(replacement['Date__c'], '%Y-%m-%d').date()
            new_teacher = [{
                "email": replacement['Teacher__r']['Email__c'],
                "name": replacement['Teacher__r']['Full_Name__c']
            }] if replacement.get("Teacher__r") else []

            # Update teacher for all future course days
            for course_day in course_days:
                if course_day >= replacement_date:
                    teacher_schedule[course_day] = new_teacher

    ## Step 3: Get all the teachers for the one-time replacements
    # Create a new dictionary for one-time replacements (do not overwrite the permanent teacher schedule)
    teacher_schedule_one_time = teacher_schedule

    # Iterate through sorted replacements and add one-time replacements for specific dates
    for replacement in sorted_replacements:
        if replacement['RecordTypeId'] == '012P5000001QASzIAO':
            replacement_date = datetime.datetime.strptime(replacement['Date__c'], '%Y-%m-%d').date()
            new_teacher = [{
                "email": replacement['Teacher__r']['Email__c'],
                "name": replacement['Teacher__r']['Full_Name__c']
            }] if replacement.get("Teacher__r") else []

            # Only replace for that specific day
            if replacement_date in course_days:
                teacher_schedule_one_time[replacement_date] = new_teacher

    ## Step 4: Add additional invitees
    if class_data['Additional_Invite__c']:
        teacher_schedule_one_time = {k: v +
            [{"email": email, "name": email} for email in class_data['Additional_Invite__c'].split(",")]
            for k, v in teacher_schedule_one_time.items()}

    # Loop through replacements looking for additional invitees
    for replacement in sorted_replacements:
        if replacement['RecordTypeId'] == '012P5000001YwypIAC':
            replacement_date = datetime.datetime.strptime(replacement['Date__c'], '%Y-%m-%d').date()
            if replacement.get('Teacher__r'):
                additional_invitee = {
                    "email": replacement.get('Teacher__r').get('Email__c'),
                    "name": replacement.get('Teacher__r').get('Full_Name__c')}

                # Only replace for that specific day
                if replacement_date in course_days:
                    teacher_schedule_one_time[replacement_date] = [*teacher_schedule_one_time[replacement_date], additional_invitee]

    return teacher_schedule_one_time
