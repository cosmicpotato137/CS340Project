import bico_scheduling as bs
import sys
import re
import test


def match_file(string):
    m = re.match(r"([a-zA-Z_-]+\/)*[a-zA-Z_-]+.txt", string)
    if m is not None:
        return True
    return False


usage = '''\
usage1: python make_schedule.py [<constraints file>] [<prefs file>] [<output file>]
    --athletes  exclude athletes past 4p
    --zoom [<1: hybrid class; 2: remote class>] [<interest threshold>]
                use zoom for some classes
usage2: python make_schedule.py --hb_concat
    example of Haverford and Bryn Mawr combined schedues'''

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("incorrect number of arguments")
    elif len(sys.argv) == 2 and sys.argv[1] == "--hb_concat":
        print("example of concatenated haverford and brynmawr schedules:")

        d = bs.bmc.get_data_list_of_dicts("brynmawr/data/Fall2007.csv")
        bs.bmc.write_constraints_to_file(d, "test/bconstraints.txt")
        bs.bmc.write_prefs_to_file(d, "test/bprefs.txt")

        d = bs.hav.get_data_list_of_dicts(
            "haverford\haverfordEnrollmentDataS14.csv")
        bs.hav.write_constraints_to_file(d, "test/hconstraints.txt")
        bs.hav.write_prefs_to_file(d, "test/hprefs.txt")

        students, classes, rooms, times, profs = bs.prep_data(
            "test/bconstraints.txt", "test/bprefs.txt", "test/hconstraints.txt", "test/hprefs.txt")

        class_p = bs.class_priority(classes)
        student_p = bs.student_priority(students)

        schedule, reg_students = bs.make_schedule(
            students, classes, rooms, times, profs,
            student_p, class_p)

        print("schedule rating:", bs.schedule_rating(schedule, students))
        bs.schedule_to_file(schedule, "test/schedule.txt")

    elif "-h" in sys.argv:
        print(usage)
    elif "-t" in sys.argv:
        print("running all tests from test.py")
        test.test()
    elif len(sys.argv) < 4:
        print("incorrect number of arguments")
        print(usage)
    elif not (match_file(sys.argv[1]) and match_file(sys.argv[2]) and match_file(sys.argv[3])):
        print("bad file format")
        print(usage)
    else:
        cf = sys.argv[1]
        pf = sys.argv[2]
        of = sys.argv[3]

        custom_times = bs.custom_times(8, 16, 1)

        students, classes, rooms, times, profs = bs.prep_data(cf, pf)

        student_athletes = None
        if "-a" in sys.argv or "--athletes" in sys.argv:
            student_athletes = bs.student_athletes(students, .386)
            times = bs.custom_times(8, 18, 1)

        zoom_params = bs.ZoomParams(0, 0)
        if "-z" in sys.argv or "--zoom" in sys.argv:
            idx = sys.argv.index("--zoom")
            if "-z" in sys.argv:
                idx = sys.argv.index("-z")
            if idx + 2 >= len(sys.argv):
                print(usage)
            try:
                zoom_params = bs.ZoomParams(sys.argv[idx+1], sys.argv[idx+2])
            except:
                print(usage)

        class_p = bs.class_priority(classes)
        student_p = bs.student_priority(students)
        # student_athletes = bs.student_athletes(students, .386)

        # custom_times = bs.custom_times(8, 16, 1)
        schedule, reg_students = bs.make_schedule(
            students, classes, rooms, times, profs,
            student_p, class_p, zoom_params=zoom_params, student_athletes=student_athletes)

        print("schedule rating:", bs.schedule_rating(schedule, students))
        bs.schedule_to_file(schedule, of)
