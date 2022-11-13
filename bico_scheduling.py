# -*- coding: utf-8 -*-
"""AlgsProject

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19wZLJf6FPzf542hQa5zeEovv-FLYsoH_

# Helper functions
"""


import re
import pandas as pd
import numpy as np
import brynmawr.get_bmc_info as bmc
import haverford.get_haverford_info as hav
from sbbst import *
import time as ts
import datetime as dt


# static counter class for experimental timekeeping
class Counter:
    i = 0

    @staticmethod
    def reset():
        Counter.i = 0
        pass

    @staticmethod
    def tick(n=1):
        Counter.i += n
        pass

    @staticmethod
    def set(i):
        Counter.i = i


# Section class for holding data for each timeslot and class
class Section:
    def __init__(self, id, time, cls, cls_p):
        # We can and should add professor to this?
        self.id = id
        self.time = time
        self.room = None
        self.cls = cls
        self.applicants = [{}, {}, {}, {}]
        self.size = 0  # min num apps and room size
        self.tmax = 0  # theoretical max size (num applicants)
        self.professor = None
        self.class_p = cls_p  # class priority 0-3
        self.num_applicants = 0

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "Class: " + str(self.cls) + " Professor: " + str(self.professor) + \
            " Time: " + str(self.time) + " Room: " + str(self.room)\
            + " Accepted: " + str(self.accepted) + " TMax: " + str(self.tmax)


def cmp_sections(x: Section, y: Section):
    if x.tmax > y.tmax:
        return True
    elif x.tmax == y.tmax:
        if x.class_p > y.class_p:
            return True
        elif x.class_p == y.class_p:
            if x.id > y.id:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


class ZoomParams:
    def __init__(self, use_zoom, overflow_val) -> None:
        self.use_zoom = use_zoom
        self.overflow_val = overflow_val


# todo: make sure students only enrolled in at most 4 classes
def make_schedule(students, classes, rooms, times, profs, student_ps=None, class_ps=None,
                  zoom_params=ZoomParams(0, 0), student_athletes=None):
    t0 = ts.time() * 1000

    # array of sections
    schedule = {}
    reg_students = {student: [] for student in students.keys()}

    num_rooms = len(rooms)

    # init 2D array of sections
    sections = {}
    id = 0
    for cls in classes.keys():
        sections[cls] = {}
        # set applicants for all times of the section
        for time in times:
            Counter.tick()
            sec = Section(id, time, cls, class_ps[cls])
            sections[cls][time] = sec
            # sections_list.append(sec)
            id += 1

    # get sorted list of rooms for each section
    sorted_rooms = rooms.sort_values(
        by="capacity", ascending=False).reset_index(drop=True)
    indices = {time: 0 for time in times}

    # get student interest
    for student_id in students.keys():
        for cls in students[student_id]:
            # set hashmap of student interest
            if cls not in sections.keys():
                continue
            for time in sections[cls].keys():
                if student_athletes is None or student_athletes[student_id] == False:
                    sections[cls][time].applicants[student_ps[student_id]
                                                   ][student_id] = False
                    sections[cls][time].tmax += 1
                elif time < 16:
                    sections[cls][time].applicants[student_ps[student_id]
                                                   ][student_id] = False
                    sections[cls][time].tmax += 1
                # sections[cls][time].num_applicants += 1

    t_trees = {}

    # initialize dict of bst's
    for time in times:
        tree = sbbst(fun=cmp_sections)
        for cls in sections.keys():
            tree.insert(sections[cls][time])
            t_trees[time] = tree

    # t1 = ts.time() * 1000 - t0
    # print(t1)
    # while there are valid classes left
    while (True):
        # choose the section
        max_val = 0
        max_sec = None
        max_time = None
        max_room = None
        for time in times:
            if t_trees[time].head is not None and indices[time] < num_rooms:
                sec: Section = t_trees[time].getMaxVal()
                room = sorted_rooms["capacity"][indices[time]]
                m = min(sec.tmax, room)
                if m > max_val:
                    max_val = m
                    max_sec = sec
                    max_time = time
                    max_room = sorted_rooms["room"][indices[time]]

        # break out of while loop if there are no more sections
        if max_val == 0:
            break

        max_cls = max_sec.cls

        # get section info and append to final schedule
        if zoom_params.use_zoom == 2 and max_sec.tmax > zoom_params.overflow_val:
            max_sec.room = "zoom"
            max_sec.size = max_sec.tmax
        elif zoom_params.use_zoom == 1 and max_sec.tmax > zoom_params.overflow_val:
            max_sec.size = max_sec.tmax
            max_sec.room = max_room
            indices[max_time] += 1  # increment index for chosen time
        else:
            indices[max_time] += 1  # increment index for chosen time
            max_sec.room = max_room
            max_sec.size = max_val
        max_sec.professor = classes[max_cls]

        # add applicants to chosen section
        num_acc = 0
        for i in range(1, 5):
            for key in max_sec.applicants[-i].keys():
                if num_acc >= max_sec.size:
                    reg_students[key].append((max_cls, max_time, "NO_ROOM"))
                else:
                    max_sec.applicants[-i][key] = True
                    num_acc += 1

        # append section to schedule
        schedule[max_cls] = max_sec

        # remove conflicting sections from contention
        for time in sections[max_cls].keys():
            t_trees[time].delete(sections[max_cls][time])
        sections.pop(max_cls)

        # t15 = ts.time() * 1000 - t1
        # ti = ts.time() * 1000

        # remove other classes the prof is teaching from the same time
        for cls in profs[max_sec.professor]:
            Counter.tick()
            if cls in sections.keys():
                if max_time in sections[cls].keys():
                    t_trees[max_time].delete(sections[cls][max_time])
                    sections[cls].pop(max_time)  # Love this

        # Handling scheduling multiple applicants at the same time
        for i in range(4):
            for student in max_sec.applicants[i].keys():
                if max_sec.applicants[i][student] == False:
                    continue
                for cls in students[student]:
                    if cls in sections.keys() and max_time in sections[cls].keys() and\
                            student in sections[cls][max_time].applicants[i]:
                        sections[cls][max_time].applicants[i].pop(student)
                        reg_students[student].append(
                            (cls, max_time, "TIME_CONFLICT"))
                        t_trees[max_time].delete(sections[cls][max_time])
                        sections[cls][max_time].tmax -= 1
                        t_trees[max_time].insert(sections[cls][max_time])

    print(ts.time() * 1000 - t0)

    return schedule, reg_students


# function for finding max class size of a section :D
def class_rating(section: Section, rooms):
    if rooms[section.time].empty:
        return 0
    idx = rooms[section.time].index[0]
    size = min(section.num_applicants, rooms[section.time]["capacity"][idx])
    name = rooms[section.time]["room"][idx]
    return size


# find the accuracy of the schedule
def schedule_rating(schedule, students):
    total = 0
    accepted = 0
    for key in students.keys():
        for cls in students[key]:
            if cls in schedule.keys():
                total += 1
    for key in schedule.keys():
        for i in range(4):
            for app in schedule[key].applicants[i].keys():
                accepted += schedule[key].applicants[i][app]

    return accepted / total


# make a file out of a list of Sections
def schedule_to_file(schedule, output_file):
    lines = ["Course\tRoom\tTeacher\tTime\tStudents\n"]
    for key in schedule.keys():
        students = ""
        for i in range(4):
            for student in schedule[key].applicants[i].keys():
                if schedule[key].applicants[i][student] == True:
                    students += f"{student} "
        lines.append(
            f"{schedule[key].cls}\t{schedule[key].room}\t{schedule[key].professor}\t{schedule[key].time}\t{students}\n")

    with open(output_file, "w") as file:
        file.writelines(lines)


# read format data from list of constraints and prefs
def prep_data(constraints, student_prefs, constraints_1=None, student_prefs_1=None):
    row = []
    with open(constraints, "r") as file:
        row = file.readlines()
    row_1 = None
    if constraints_1 is not None:
        with open(constraints_1, "r") as file_1:
            row_1 = file_1.readlines()

    i = 0
    num_times = int(row[i].split()[-1])
    times = [str(i) for i in range(num_times)]
    i += 1
    while row[i].split()[0] != "Rooms":
        idx = re.search(r"[0-9]+[\s\t]+", row[i])
        # t0 = re.search(r"[0-9]?[0-9]:[0-9]{2}\s+(AM|PM)", row[i])
        # t1 = re.search(r"[0-9]?[0-9]:[0-9]{2}\s+(AM|PM)", row[i][t0.end(0):])
        # d = re.search(r"[\t\s]+.*", row[i][t1.end(0):])
        # print(t0.group(0), t1.group(0), d.group(0))
        times[i-1] = int(idx.group(0)[:-1])
        i += 1

    rooms = {"room": [], "capacity": []}

    j = 0
    if row_1 is not None:
        while row_1[j].split()[0] != "Rooms":
            j += 1
        j += 1
        while row_1[j].split()[0] != "Classes":
            r_1 = row_1[j].split()
            rooms["room"].append("1" + r_1[0])
            rooms["capacity"].append(int(r_1[1]))
            j += 1

    i += 1
    while row[i].split()[0] != "Classes":
        r = row[i].split()
        rooms["room"].append("0" + r[0])
        rooms["capacity"].append(int(r[1]))
        i += 1
    rooms = pd.DataFrame.from_dict(rooms)

    profs = {"-1": []}
    classes = {}

    if row_1 is not None:
        rows_1 = int(row_1[j].split()[1]) + j + 2
        j += 2
        while j < rows_1:
            r_1 = row_1[i].split()
            if len(r_1) == 2:
                if profs.get("1" + r_1[1]) != None:
                    profs["1" + r_1[1]].append("1" + r_1[0])
                else:
                    profs["1" + r_1[1]] = ["1" + r_1[0]]
                classes["1" + r_1[0]] = "1" + r_1[1]
            else:
                profs["-1"].append("1" + r_1[0])
                classes["1" + r_1[0]] = "-1"
            j += 1

    rows = int(row[i].split()[1]) + i + 2
    i += 2
    while i < rows:
        r = row[i].split()
        if len(r) > 1:
            if profs.get("0" + r[1]) != None:
                profs["0" + r[1]].append("0" + r[0])
            else:
                profs[r[1]] = ["0" + r[0]]
            classes["0" + r[0]] = r[1]
        else:
            profs["-1"].append("0" + r[0])
            classes["0" + r[0]] = "-1"
        i += 1

    rows = []
    rows_1 = None
    with open(student_prefs, "r") as file:
        rows = file.readlines()
    if student_prefs_1 is not None:
        with open(student_prefs_1, "r") as file_1:
            rows_1 = file_1.readlines()

    students = {}

    if rows_1 is not None:
        for row in rows[1:]:
            r_1 = row.split()
            students["1" + r_1[0]] = ["1" + r_1[i] for i in range(1, len(r_1))]

    for row in rows[1:]:
        r = row.split()
        students["0" + r[0]] = ["0" + r[i] for i in range(1, len(r))]

    return (students, classes, rooms, times, profs)


def class_priority(classes):
    p = {}
    for cls in classes.keys():
        p[cls] = np.random.randint(0, 3)
    return p


def student_priority(students):
    p = {}
    for st in students.keys():
        p[st] = np.random.randint(1, 4)
    return p


def student_athletes(students, p_athletes):
    p = {}
    i = 0
    for st in students.keys():
        f = np.random.random()
        if f < p_athletes:
            p[st] = True
        else:
            p[st] = False
        i += 1
    return p


def custom_times(start, finish, interval):
    times = [i for i in range(start, finish, interval)]
    return times
