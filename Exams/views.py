from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound, HttpResponseNotAllowed
from django.views.decorators.http import require_GET, require_POST
from .models import Exam, Category, Subject, Topic

# Request Handlers for TASKS

# TASK 1: Create exam

@require_POST
def createExam(request):
    """
    Create new Exam

        Parameters:
        -----------
        ``exam``
            exam name as string

        Responses:
        ----------
        HttpResponseBadRequest
            If ``exam`` parameter is not provided or its not of type ``string``

        HttpResponse
            ``Id`` of the new Exam created, otherwise ``Exists`` if exam already present

        HttpResponseServerError
            Internal Server Error
    """
    
    try:
        if "exam" in request.POST:
            exam = request.POST["exam"]
            if isinstance(exam, str):
                try:
                    examObj = Exam.objects.create(name= exam)
                    return HttpResponse(str(examObj.id))        
                except:
                    return HttpResponse("Exists")
        return HttpResponseBadRequest()
    except:
        return HttpResponseServerError()

# TASK 2: Get the list of all exams

@require_GET
def getExamsList(request):
    """
    Get list of all Exams present

        Responses:
        ----------

        JsonResponse
            {'exams': []}

        HttpResponseServerError
            Internal Server Error
    """
    
    try:
        result = {"exams": list(Exam.objects.values_list('name', flat= True).order_by('name'))}
        return JsonResponse(result, safe= True)        
    except:
        return HttpResponseServerError()
    

# TASK 3: Add sub-categories, subjects and topics under an exam only one record at a time.

@require_POST
def addCategory(request):
    """
    Add new Category, to Exam or other Category. First check Category table, then go to Exam table.

        Parameters:
        -----------
        ``category``
            category name as string

        ``attachTo``
            parent category or exam name as string

        Responses:
        ----------
        HttpResponseBadRequest
            If ``category`` and ``attachTo`` parameter are not provided or their type is not ``string``, both are **required**

        HttpResponse
            ``Id`` of the new Category created

        HttpResponseNotAllowed
            If ``Subject`` is already present, and trying to add new category

        HttpResponseNotFound
            When there's no ``attachTo`` related to Category or Exam exists 

        HttpResponseServerError
            Internal Server Error
    """
    
    try:        
        if "category" in request.POST and "attachTo" in request.POST:
            newCategory = request.POST["category"]
            attachTo = request.POST["attachTo"]
            if isinstance(newCategory, str) and isinstance(attachTo, str):
                try:
                    # if the category exists create this new category under it, otherwise exception will be raised
                    parentCategory = Category.objects.get(name__iexact = attachTo)
                    if not Subject.objects.filter(associated_to= 'C', association_id= parentCategory.id).exists():
                        # newCatObj = Category.objects.create(name= newCategory, parent= parentCategory, exam= parentCategory.exam)
                        newCatObj = Category.objects.create(name= newCategory, parent= parentCategory)
                        return HttpResponse(str(newCatObj.id))
                    return HttpResponseNotAllowed("Cannot create new category, subject is already present under Category")                                            
                except:
                    try:
                        # it will run if the category provided in 'attachTo' doesn't exists
                        # if the exam exists create this new category under exam, otherwise exception will be raised
                        exam = Exam.objects.get(name__iexact = attachTo)
                        if not Subject.objects.filter(associated_to= 'E', association_id= exam.id).exists():
                            newCatObj = Category.objects.create(name= newCategory, exam= exam)
                            return HttpResponse(str(newCatObj.id))
                        return HttpResponseNotAllowed("Cannot create new category, subject is already present under Exam")                                                    
                    except:
                        return HttpResponseNotFound("attachTo doesn't exists")
        return HttpResponseBadRequest()
    except:
        return HttpResponseServerError()

@require_POST
def addSubject(request):
    """
    Add new Subject, to Exam or lowest-level Category. First check Category table, then go to Exam table.
        
        Parameters:
        -----------
        ``subject``
            subject name as string
        
        ``attachTo``
            name of lowest-level category or exam with no category as string

        Responses:
        ----------
        HttpResponseBadRequest
            If ``subject`` and ``attachTo`` parameter are not provided or their type is not ``string``, both are **required*
        
        HttpResponse
            ``Id`` of the new Subject created
        
        HttpResponseNotAllowed
            If trying to add new subject to inner level Category or Exam's with Category
        
        HttpResponseNotFound
            When there's no ``attachTo`` related to Category or Exam exists 
        
        HttpResponseServerError
            Internal Server Error
    """
    
    try:
        if "subject" in request.POST and "attachTo" in request.POST:
            newSubject = request.POST["subject"]
            attachTo = request.POST["attachTo"]
            if isinstance(newSubject, str) and isinstance(attachTo, str):
                try:
                    category = Category.objects.get(name__iexact = attachTo)
                    if category.is_leaf_node():
                        newSubObj = Subject.objects.create(name= newSubject, associated_to="C", association_id= category.id)
                        return HttpResponse(str(newSubObj.id))
                    else:
                        return HttpResponseNotAllowed("attachTo is not lowest sub-category")
                except:
                    try:
                        exam = Exam.objects.get(name__iexact = attachTo)
                        if exam.category_set.count() == 0 :
                            newSubObj = Subject.objects.create(name= newSubject, associated_to="E", association_id= exam.id)
                            return HttpResponse(str(newSubObj.id))
                        else:
                            return HttpResponseNotAllowed("cannot attach to exam if it already has categories")
                    except:
                        return HttpResponseNotFound("attachTo doesn't exists")
        return HttpResponseBadRequest()
    except:
        return HttpResponseServerError()

@require_POST
def addTopic(request):
    """
    Add new Topic, to Subject or other Topics. First check Topic table, then go to Subject table
        
        Parameters:
        -----------
        ``topic``
            topic name as string

        ``attachTo``
            parent topic or subject name as string

        Responses:
        ----------
        HttpResponseBadRequest
            If ``topic`` and ``attachTo`` parameter are not provided or their type is not ``string``, both are required
        
        HttpResponse
            ``Id`` of the new Topic created

        HttpResponseNotFound
            When there's no ``attachTo`` related to Topic or Subject exists 

        HttpResponseServerError
            Internal Server Error
    """

    try:
        if "topic" in request.POST and "attachTo" in request.POST:
            newTopic = request.POST["topic"]
            attachTo = request.POST["attachTo"]
            if isinstance(newTopic, str) and isinstance(attachTo, str):
                try:
                    parentTopic = Topic.objects.get(name__iexact = attachTo)
                    # newTopObj = Topic.objects.create(name= newTopic, parent= parentTopic, subject= parentTopic.subject)
                    newTopObj = Topic.objects.create(name= newTopic, parent= parentTopic)
                    return HttpResponse(str(newTopObj.id))
                except:
                    try:
                        subject = Subject.objects.get(name__iexact = attachTo)
                        newTopObj = Topic.objects.create(name= newTopic, subject= subject)
                        return HttpResponse(str(newTopObj.id))
                    except:
                        return HttpResponseNotFound("attachTo doesn't exists")
        return HttpResponseBadRequest()
    except:
        return HttpResponseServerError()

# TASK 4: Get the entire hierarchy of an exam, its sub-categories their subjects and topics.

@require_GET
def getExamDetails(request):
    """
    Get all details of specified exam, details related to categories, subjects, topics.
        
        Parameters:
        -----------
        ``exam``
            exam name as string

        Responses:
        ----------
        HttpResponseBadRequest
            If ``exam`` parameter is not provided or its type is not ``string``

        JsonResponse
            {"exam": string, "subcategory": [], "subject": []}

        HttpResponseNotFound
            If the ``exam`` doesn't exists

        HttpResponseServerError
            Internal Server Error
    """

    try:
        if "exam" in request.GET:
            exam = request.GET["exam"]
            if isinstance(exam, str):
                try:
                    examObj = Exam.objects.get(name__iexact= exam)
                    result = {"exam": examObj.name}
                    if examObj.category_set.count() > 0:
                        result["categories"] = []
                        for cObj in examObj.category_set.all():
                            result["categories"].append(cObj.shakeCategoryTree())
                    else:
                        result["subjects"] = examObj.getRelatedSubjects()
                    return JsonResponse(result, safe= True)
                except:
                    return HttpResponseNotFound("Exam doesn't exists")
        return HttpResponseBadRequest()
    except:
        return HttpResponseServerError()