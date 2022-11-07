import bico_scheduling as bs

d = bs.bmc.get_data_list_of_dicts("brynmawr/data/Fall2000.csv")
bs.bmc.write_constraints_to_file(d, "brynmawr/data/constraints.txt")
bs.bmc.write_prefs_to_file(d, "test/prefs.txt")

students, classes, rooms, times, profs = bs.prep_data(
    "test/constraints.txt", "test/prefs.txt")

schedule = bs.make_schedule(students, classes, rooms, times, profs)

print("schedule rating:", bs.schedule_rating(schedule, students))
bs.schedule_to_file(schedule, "test/schedule.txt")
