from django.test import TestCase, Client
from unittest import skip
from json import loads
from Exams.models import Exam, Category, Subject, Topic

class TestExamsApp(TestCase):
    
    def setUp(self):
        self.host = "http://127.0.0.1"
        self.port = "8000"
        self.url = self.host+":"+self.port+"/"

    def test_1_createExam(self):
        api = self.url+"exams/createexam/"
        
        __testname__ = "Test: Accept only POST methods"
        with self.subTest(__testname__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __testname__ = "Test: Create Exam without parameters"
        with self.subTest(__testname__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 500)

        __testname__ = "Test: Create Exam"
        exam = "IIT"
        with self.subTest(__testname__, api= api, exam= exam):
            response = self.client.post(api, {"exam": exam})
            self.assertGreater(int(response.content), 0)
        
        __testname__ = "Test: Exam exists"
        exam = "IIT"
        with self.subTest(__testname__, api= api, exam= exam):
            response = self.client.post(api, {"exam": exam})
            self.assertEqual(response.content.decode('utf'), "Exists")
            
    def test_2_getExamsList(self):
        api = self.url+"exams/getexamslist/"
        
        __testname__ = "Test: Accept only GET methods"
        with self.subTest(__testname__, api=api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 405)
        
        __testname__ = "Test: Get Empty Exam List"
        with self.subTest(__testname__, api= api):
            response = self.client.get(api)
            data = loads(response.content)
            self.assertListEqual(data["exams"], [])

        __testname__ = "Test: Get Exams List"
        Exam.objects.create(name="CAT")
        # CAT (E)
        Exam.objects.create(name="AIEEE")
        # AIEEE (E)
        Exam.objects.create(name="GRE")        
        # GRE (E)
        with self.subTest(__testname__, api= api):
            response = self.client.get(api)
            data = loads(response.content)
            self.assertListEqual(data["exams"], sorted(["CAT","AIEEE","GRE"]))
        
    def test_3_addCategory(self):                
        api = self.url+"exams/addcategory/"
        
        __testname__ = "Test: Accept only POST methods"
        with self.subTest(__testname__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __testname__ = "Test: Add category without parameters"
        with self.subTest(__testname__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 500)
        
        __testname__ = "Test: Add category to exam"
        exam = Exam.objects.create(name="CAT")
        # CAT (E)
        category = "Aptitude"
        with self.subTest(__testname__, api= api, exam = exam, category= category):
            response = self.client.post(api, {"category": category, "attachTo": exam.name})
            c = Category.objects.get(name= category)
            self.assertEqual(int(response.content), c.id)

        __testname__ = "Test: Add category to another category"
        # CAT (E) -> Aptitude (C)
        attachTo = "Aptitude"
        category = "Statistics"
        with self.subTest(__testname__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            c = Category.objects.get(name= category)
            self.assertEqual(int(response.content), c.id)
        
        __testname__ = "Test: Add category to inner category"
        # CAT (E) -> Aptitude (C) -> Statistics (C)
        attachTo = "Aptitude"
        category = "Probability"
        with self.subTest(__testname__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            c = Category.objects.get(name= category)
            self.assertEqual(int(response.content), c.id)

        __testname__ = "Test: Add category to unknown parent"
        category = "Grammar"
        attachTo = "English"
        with self.subTest(__testname__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            self.assertEqual(response.status_code, 404)

        __testname__ = "Test: Add category to exam with subject"
        exam = Exam.objects.create(name="IIT")
        # IIT (E)
        Subject.objects.create(name= "Physics", associated_to= 'E', association_id= exam.id)
        # IIT (E) -> Physics (S)
        category = "Science"
        with self.subTest(__testname__, api= api, exam= exam, category= category):
            response = self.client.post(api, {"category": category, "attachTo": exam.name})
            self.assertEqual(response.status_code, 405)

        __testname__ = "Test: Add category to another category with subject"
        # CAT (E) -> Aptitude (C) -> Statistics (C)
        # CAT (E) -> Aptitude (C) -> Probability (C)
        c= Category.objects.get(name= "Statistics")
        Subject.objects.create(name="3M", associated_to= 'C', association_id= c.id)
        # CAT (E) -> Aptitude (C) -> Statistics (C) -> 3M (S)
        # CAT (E) -> Aptitude (C) -> Probability (C)
        attachTo = c.name
        category = "Data Models"
        with self.subTest(__testname__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            self.assertEqual(response.status_code, 405)

    def test_3_addSubject(self):                
        api = self.url+"exams/addsubject/"
        
        __testname__ = "Test: Accept only POST methods"
        with self.subTest(__testname__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __testname__ = "Test: Add subject without parameters"
        with self.subTest(__testname__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 500)
        
        __testname__ = "Test: Add subject under exam"
        exam = Exam.objects.create(name= "IIT")
        # IIT (E)
        subject = "Physics"
        with self.subTest(__testname__, api= api, exam= exam, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": exam.name})
            s = Subject.objects.get(name= subject)
            self.assertEqual(int(response.content), s.id)

        __testname__ = "Test: Add subject under low-level category"
        exam = Exam.objects.create(name= "GATE")
        # GATE (E)
        category = Category.objects.create(name="Computer Science", exam= exam)
        # GATE (E) -> Computer Science (C)
        subject = "Database"
        with self.subTest(__testname__, api= api, category= category, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": category.name})
            s = Subject.objects.get(name= subject)
            self.assertEqual(int(response.content), s.id)

        __testname__= "Test: Add subject under exam with category"
        # GATE (E) -> Computer Science (C) -> Database (S)
        exam = Exam.objects.get(name= "GATE")
        subject = "Operating System"
        with self.subTest(__testname__, api= api, exam= exam, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": exam.name})
            self.assertEqual(response.status_code, 405)

        __testname__ = "Test: Add subject under inner category"
        # GATE (E) -> Computer Science (C) -> Database (S)
        exam = Exam.objects.get(name= "GATE")
        inCategory = Category.objects.create(name= "Mathematics")
        # GATE (E) -> Computer Science (C) -> Database (S)
        # GATE (E) -> Mathematics (C)
        Category.objects.create(name= "Applied Mathematics", parent= inCategory)
        # GATE (E) -> Mathematics (C) -> Applied Mathematics (C)
        subject = "Operating System"
        with self.subTest(__testname__, api= api, inCategory= inCategory, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": inCategory.name})
            self.assertEqual(response.status_code, 405)

        __testname__ = "Test: Add subject to unknown parent"
        subject = "Grammar"
        attachTo = "English"
        with self.subTest(__testname__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"subject": category, "attachTo": attachTo})
            self.assertEqual(response.status_code, 404)

def test_3_addTopic(self):                
        api = self.url+"exams/addtopic/"
        
        __testname__ = "Test: Accept only POST methods"
        with self.subTest(__testname__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __testname__ = "Test: Add topic without parameters"
        with self.subTest(__testname__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 500)
        
        __testname__ = "Test: Add topic under subject"
        exam = Exam.objects.create(name= "IIT")
        # IIT (E)
        subject = Subject.objects.create(name= "Physics", associated_to= 'E', association_id= exam.id)
        # IIT (E) -> Physics (S)
        topic = "Relativity Theory"
        with self.subTest(__testname__, api= api, subject= subject, topic= topic):
            response = self.client.post(api, {"topic": topic, "attachTo": subject.name})
            t = Topic.objects.get(name= topic)
            self.assertEqual(int(response.content), t.id)

        __testname__ = "Test: Add topic under another topic"
        # IIT (E) -> Physics (S) -> Relative Theory (T)
        attachTo = "Relativity Theory"
        topic = "Dark Matter"
        with self.subTest(__testname__, api= api, topic= topic, attachTo= attachTo):
            response = self.client.post(api, {"topic": topic, "attachTo": attachTo})
            t = Topic.objects.get(name= topic)
            self.assertEqual(int(response.content), t.id)

        __testname__ = "Test: Add topic under inner topic"
        # IIT (E) -> Physics (S) -> Relative Theory (T) -> Dark Matter (T)
        attachTo = "Relativity Theory"
        topic = "E=MC^2"
        with self.subTest(__testname__, api= api, topic= topic, attachTo= attachTo):
            response = self.client.post(api, {"topic": topic, "attachTo": attachTo})
            t = Topic.objects.get(name= topic)
            self.assertEqual(int(response.content), t.id)

        __testname__ = "Test: Add topic to unknown parent"
        topic = "Grammar"
        attachTo = "English"
        with self.subTest(__testname__, api= api, attachTo= attachTo, topic= topic):
            response = self.client.post(api, {"topic": topic, "attachTo": attachTo})
            self.assertEqual(response.status_code, 404)
