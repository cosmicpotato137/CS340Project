import bico_scheduling as bs

d = bs.bmc.get_data_list_of_dicts("brynmawr/data/Spring2006.csv")
bs.bmc.write_constraints_to_file(d, "test/constraints.txt")
bs.bmc.write_prefs_to_file(d, "test/prefs.txt")

# d = bs.hav.get_data_list_of_dicts("haverford\haverfordEnrollmentDataS14.csv")
# bs.hav.write_constraints_to_file(d, "test/constraints.txt")
# bs.hav.write_prefs_to_file(d, "test/prefs.txt")

students, classes, rooms, times, profs = bs.prep_data(
    "test/constraints.txt", "test/prefs.txt")
class_p = bs.class_priority(classes)
student_p = bs.student_priority(students)
schedule, reg_students = bs.make_schedule(
    students, classes, rooms, times, profs, student_p, class_p)

print("schedule rating:", bs.schedule_rating(schedule, students))
bs.schedule_to_file(schedule, "test/schedule.txt")
