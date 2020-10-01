from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Exam(models.Model):
    """
    Model for Exam
    Table name: exam
    """

    name = models.CharField(max_length=100, unique= True)

    class Meta:
        db_table = "exam"

class Category(MPTTModel):
    """
    Model for Category. Support for Hierarchical structure using MPTT model.
    Table name: category
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
    Table name: subject
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
    Table name: topic
    """

    name = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey('Subject', null=True, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        db_table = "topic"

