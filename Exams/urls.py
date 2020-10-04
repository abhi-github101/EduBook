"""
*************
EXAM'S ROUTES
*************

    Create exam
    ===========
        Route:
            ``exams/createexam/``
    
    Get Exams list
    ==============
        Route:
            ``exams/getexamslist/``
    
    Add Category
    ============
        Route:
            ``exams/addcategory/``
    
    Add Subject
    ===========
        Route:
            ``exams/addsubject/``
    
    Add Topic
    =========
        Route:
            ``exams/addtopic/``
    
    Get Exam Details
    ================
        Route:
            ``exams/getexamdetails/``
"""

from django.urls import path
from . import views

# Routes for TASKS

# TASK 1: Create exam
task1_api = [
            path("createexam/", views.createExam),
            ]

# TASK 2: Get the list of all exams
task2_api = [
            path("getexamslist/", views.getExamsList),
            ]

# TASK 3: Add sub-categories, subjects and topics under an exam only one record at a time.
task3_api = [
            path("addcategory/", views.addCategory),
            path("addsubject/", views.addSubject),
            path("addtopic/", views.addTopic),
            ]

# TASK 4: Get the entire hierarchy of an exam, its sub-categories their subjects and topics.
task4_api = [
            path("getexamdetails/", views.getExamDetails),
            ]

urlpatterns = task1_api + task2_api + task3_api + task4_api    
