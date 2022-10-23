import bico_scheduling as bs
import sys

if __name__ == "__main__":
    # root directories for drive
    data_location = "./"  # for Mac

    bs.Counter.reset()
    if len(sys.argv) == 3:
        sch = bs.make_hav_schedule(
            data_location + sys.argv[1], data_location + sys.argv[2])
    elif len(sys.argv) == 1:
        hav = "haverford/haverfordEnrollmentDataS14.csv"
        sch = bs.make_hav_schedule(
            data_location + hav, data_location + "/test")
    else:
        print("Invalid number arguments")
        print(
            "Usage: " + sys.argv[0] + "<enrollment.csv> <student_prefs.txt> <constraints.txt>")
        exit(1)
