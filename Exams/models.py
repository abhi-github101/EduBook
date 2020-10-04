from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Exam(models.Model):
    """
    Model for Exam
    
    Table name: 
    -----------
        ``exam``
    
    Columns:
    --------
        ``id``- Primary Key, Auto Increment
        ``name``- name of exam
    """

    name = models.CharField(max_length=100, unique= True)

    class Meta:
        db_table = "exam"

class Category(MPTTModel):
    """
    Model for Category. Support for Hierarchical structure using MPTT model.

    Table name:
    ----------- 
        ``category``
    
    Columns:
    --------
        ``id``- Primary Key, Auto Increment
        ``name``- name of category
        ``exam``- Foreign Key to ``exam`` table
        ``parent``- Tree Foreign Key to self ``id``
    """

    name = models.CharField(max_length=100, unique=True)
    exam = models.ForeignKey('Exam', null=True, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        db_table = "category"

class Subject(models.Model):
    """
    Model for Subject
    
    Table name:
    ----------- 
        ``subject``
    
    Columns:
    --------
        ``id``- Primary Key, Auto Increment
        ``name``- name of category
        ``associated_to``- type of association, ``E`` for exam or ``C`` for Category
        ``association_id``- id of association, exam or category id
    """

    TYPE = [('E', "EXAM"),('C', "CATEGORY")]
    name = models.CharField(max_length=100, unique=True)
    associated_to = models.CharField(max_length=1, choices=TYPE)
    association_id = models.IntegerField()
    
    class Meta:
        db_table = "subject"

class Topic(MPTTModel):
    """
    Model for Topic. Support for Hierarchical structure using MPTT model.
    
    Table name:
    ----------- 
        ``topic``
    
    Columns:
    --------
        ``id``- Primary Key, Auto Increment
        ``name``- name of topic
        ``subject``- Foreign Key to ``subject`` table
        ``parent``- Tree Foreign Key to self ``id``
    """

    name = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey('Subject', null=True, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        db_table = "topic"

