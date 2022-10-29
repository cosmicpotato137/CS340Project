import bico_scheduling as bs

students, classes, rooms, times, profs = bs.prep_data(
    "basic/demo_constraints.txt", "basic/demo_studentprefs.txt")

schedule = bs.make_schedule(students, classes, rooms, times, profs)

bs.schedule_to_file(schedule, "test/schedule.txt")
