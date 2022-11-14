import bico_scheduling as bs


d = bs.bmc.get_data_list_of_dicts("brynmawr/data/Fall2000.csv")
bs.bmc.write_constraints_to_file(d, "test/bconstraints.txt")
bs.bmc.write_prefs_to_file(d, "test/bprefs.txt")


d = bs.hav.get_data_list_of_dicts("haverford\haverfordEnrollmentDataS14.csv")
bs.hav.write_constraints_to_file(d, "test/hconstraints.txt")
bs.hav.write_prefs_to_file(d, "test/hprefs.txt")

# -----------------------------------------------------------------------
# Combined Section

# students_c, classes_c, rooms_c, times_c, profs_c = bs.prep_data(
#     "test/bconstraints.txt", "test/bprefs.txt", "test/hconstraints.txt", "test/hprefs.txt")

# class_p_c = bs.class_priority(classes_c)
# student_p_c = bs.student_priority(students_c)
# student_athletes_c = bs.student_athletes(students_c, .386)

# custom_times = bs.custom_times(8, 16, 1)
# schedule_c, reg_students_c = bs.make_schedule(
#     students_c, classes_c, rooms_c, custom_times, profs_c,
#     student_p_c, class_p_c)

# print("Combined  schedule rating:", bs.schedule_rating(schedule_c, students_c))
# bs.schedule_to_file(schedule_c, "test/schedule.txt")


# -------------------------------------------------------------------------
# Bryn Mawr Section

students_b, classes_b, rooms_b, times_b, profs_b = bs.prep_data(
    "test/bconstraints.txt", "test/bprefs.txt")

class_p_b = bs.class_priority(classes_b)
student_p_b = bs.student_priority(students_b)
student_athletes_b = bs.student_athletes(students_b, 1)

custom_times = bs.custom_times(8, 18, 1)
schedule_b, reg_students_b = bs.make_schedule(
    students_b, classes_b, rooms_b, custom_times, profs_b,
    student_p_b, class_p_b, bs.ZoomParams(0,50), student_athletes_b)

print("Bryn Mawr schedule rating:", bs.schedule_rating(schedule_b, students_b))
bs.schedule_to_file(schedule_b, "test/schedule.txt")


# -------------------------------------------------------------
# Haverford Section

# students_h, classes_h, rooms_h, times_h, profs_h = bs.prep_data(
#     "test/hconstraints.txt", "test/hprefs.txt")

# class_p_h = bs.class_priority(classes_h)
# student_p_h = bs.student_priority(students_h)
# student_athletes_h = bs.student_athletes(students_h, .386)

# custom_times = bs.custom_times(8, 16, 1)
# schedule_h, reg_students_h = bs.make_schedule(
#     students_h, classes_h, rooms_h, custom_times, profs_h,
#     student_p_h, class_p_h)

# print("Haverford schedule rating:", bs.schedule_rating(schedule_h, students_h))
# bs.schedule_to_file(schedule_h, "test/schedule.txt")
