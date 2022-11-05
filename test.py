import bico_scheduling as bs


# d = bs.bmc.get_data_list_of_dicts("brynmawr/data/Fall2000.csv")
# bs.bmc.write_constraints_to_file(d, "test/constraints.txt")
# bs.bmc.write_prefs_to_file(d, "test/prefs.txt")

students, classes, rooms, times, profs = bs.prep_data(
    "basic\demo_constraints.txt", "basic\demo_studentprefs.txt")


schedule = bs.make_schedule(students, classes, rooms, times, profs)

# print(schedule)
# bs.schedule_to_file(schedule, "test/schedule.txt")
