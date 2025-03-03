def get_teacher_dict(sf, events):
    # Get unique teachers
    teachers = set()
    for event in events:
        for teacher in event.get("teachers"):
            teachers.add(teacher)

    # Get teacher details of each teacher who taught
    teacher_dict = {teacher: sf.get_teacher_details(teacher) for teacher in teachers}

    # Append events to teacher details
    for teacher in teacher_dict:
        filtered_events = list(filter(lambda event: teacher in event.get("teachers") and event.get("held"), events))
        teacher_dict.get(teacher).update({"events": filtered_events})

    # Compute total amount per teacher
    for teacher_email in teacher_dict:
        teacher = teacher_dict.get(teacher_email)

        total_amount = sum([event.get("amount") for event in teacher.get("events")])
        total_minutes = sum([event.get("minutes") for event in teacher.get("events")])

        teacher.update({
            "total_amount": total_amount,
            "hours": int(total_minutes // 60),
            "minutes": int(total_minutes % 60)
        })
        nice_name = f"{teacher.get('Full_Name__c')} -> {teacher.get('Contract_Type__c')} [{teacher.get('hours')}h{teacher.get('minutes')} - {teacher.get('total_amount')}€]"
        teacher.update({"nice_name": nice_name})

    return teacher_dict

def generate_confirmation_text(teacher_dict, events):
    return_string = []

    # 1. Held and to be paid classes
    return_string += [
        "#########################",
        "##  Held and to be paid classes",
        "#########################"]
    total = 0
    for teacher_email in teacher_dict:
        teacher = teacher_dict.get(teacher_email)
        total += float(teacher.get("total_amount"))
        return_string += [teacher.get("nice_name")]
        for event in teacher.get("events"):
            return_string += [event.get('nice_name')]
    return_string += ["", f"--> TOTAL: {total}"]

    # 2. Double Teacher
    double_events = [event for event in events if len(event.get("teachers")) > 1 and event.get("held")]
    return_string += ["",
        "#########################",
        "##  Double Teacher ",
        "#########################"]
    for event in double_events:
        return_string += [f"{event.get('nice_name')} -> {event.get('teachers')}"]

    # 3. None, Not Cancelled
    none_not_cancelled_events = [event for event in events if len(event.get("teachers")) == 0 and event.get("held")]
    return_string += ["",
        "#########################",
        "##  None, Not Cancelled ",
        "#########################"]
    for event in none_not_cancelled_events:
        return_string += [event.get('nice_name')]

    # 4. Not Held
    not_held_events = [event for event in events if len(event.get("teachers")) > 0 and not event.get("held")]
    return_string += ["",
        "#########################",
        "##  Not Held ",
        "#########################"]
    for event in not_held_events:
        return_string += [event.get('nice_name')]

    return return_string
