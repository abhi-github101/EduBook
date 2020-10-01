from .models import Exam, Category, Subject, Topic

def dbFixtures():
    """
    Use this method to fill the database with some initial data.
    """

    # Exam 'GATE'
    exam_gate = Exam.objects.create(name="GATE")
    
    # Category 'Computer Science' under Exam 'GATE'
    cat_cs = Category.objects.create(name="Computer Science", exam=exam_gate)
    
    # Subject 'Databases' associated with Category 'Computer Science'
    sub_db = Subject.objects.create(name="Databases", associated_to= 'C', association_id= cat_cs.id)
    # Topics related to Subject 'Databases'
    Topic.objects.create(name="RDBMS", subject=sub_db)
    Topic.objects.create(name="NoSQL", subject=sub_db)
    
    # Subject 'Operating System' associated with Category 'Computer Science'
    sub_os = Subject.objects.create(name="Operating System", associated_to= 'C', association_id= cat_cs.id)
    # Topics related to Subject 'Operating System'
    Topic.objects.create(name="Process", subject=sub_os)
    Topic.objects.create(name="Multi-threading", subject=sub_os)

    # Exam 'IIT'
    exam_iit = Exam.objects.create(name="IIT")
    
    # Subject 'Physics' associated with Exam 'IIT'
    sub_physics = Subject.objects.create(name="Physics", associated_to= 'E', association_id= exam_iit.id)
    # Topics related to Subject 'Physics'
    Topic.objects.create(name="Wave Optics", subject=sub_physics)
    Topic.objects.create(name="Mechanics", subject=sub_physics)
    Topic.objects.create(name="Thermodynmics", subject=sub_physics)
    
    # Subject 'Chemistry' associated with Exam 'IIT'
    sub_chem = Subject.objects.create(name="Chemistry", associated_to= 'E', association_id= exam_iit.id)
    # Topics related to Subject 'Chemistry'
    Topic.objects.create(name="Organic Chemistry", subject=sub_chem)
    Topic.objects.create(name="Physical Chemistry", subject=sub_chem)
    
    # Subject 'Mathematics' associated with Exam 'IIT'
    sub_maths = Subject.objects.create(name="Mathematics", associated_to= 'E', association_id= exam_iit.id)
    # Topics related to Subject 'Mathematics'
    Topic.objects.create(name="Trigonometry", subject=sub_maths)
    Topic.objects.create(name="Probability", subject=sub_maths)
    Topic.objects.create(name="Algebra", subject=sub_maths)
    