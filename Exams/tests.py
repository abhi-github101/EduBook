from django.test import TestCase, Client
from unittest import skip
from json import loads
from Exams.models import Exam, Category, Subject, Topic

class TestExamsAPI(TestCase):
    
    def setUp(self):
        self.host = "http://127.0.0.1"
        self.port = "8000"
        self.url = self.host+":"+self.port+"/"

    def test_1_createExam(self):
        api = self.url+"exams/createexam/"
        
        __ = "Test: Accept only POST methods"
        with self.subTest(__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __ = "Test: Create Exam without parameters"
        with self.subTest(__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 400)

        __ = "Test: Create Exam"
        exam = "IIT"
        with self.subTest(__, api= api, exam= exam):
            response = self.client.post(api, {"exam": exam})
            self.assertGreater(int(response.content), 0)
        
        __ = "Test: Exam exists"
        exam = "IIT"
        with self.subTest(__, api= api, exam= exam):
            response = self.client.post(api, {"exam": exam})
            self.assertEqual(response.content.decode('utf-8'), "Exists")
            
    def test_2_getExamsList(self):
        api = self.url+"exams/getexamslist/"
        
        __ = "Test: Accept only GET methods"
        with self.subTest(__, api=api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 405)
        
        __ = "Test: Get Empty Exam List"
        with self.subTest(__, api= api):
            response = self.client.get(api)
            data = loads(response.content)
            self.assertListEqual(data["exams"], [])

        __ = "Test: Get Exams List"
        Exam.objects.create(name="CAT")
        # CAT (E)
        Exam.objects.create(name="AIEEE")
        # AIEEE (E)
        Exam.objects.create(name="GRE")        
        # GRE (E)
        with self.subTest(__, api= api):
            response = self.client.get(api)
            data = loads(response.content)
            result = Exam.objects.values_list('name', flat=True)
            self.assertListEqual(data["exams"], list(result))
        
    def test_3_addCategory(self):                
        api = self.url+"exams/addcategory/"
        
        __ = "Test: Accept only POST methods"
        with self.subTest(__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __ = "Test: Add category without parameters"
        with self.subTest(__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 400)
        
        __ = "Test: Add category to exam"
        exam = Exam.objects.create(name="CAT")
        # CAT (E)
        category = "Aptitude"
        with self.subTest(__, api= api, exam = exam, category= category):
            response = self.client.post(api, {"category": category, "attachTo": exam.name})
            c = Category.objects.get(name= category)
            self.assertEqual(int(response.content), c.id)

        __ = "Test: Add category to another category"
        # CAT (E) -> Aptitude (C)
        attachTo = "Aptitude"
        category = "Statistics"
        with self.subTest(__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            c = Category.objects.get(name= category)
            self.assertEqual(int(response.content), c.id)
        
        __ = "Test: Add category to inner category"
        # CAT (E) -> Aptitude (C) -> Statistics (C)
        attachTo = "Aptitude"
        category = "Probability"
        with self.subTest(__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            c = Category.objects.get(name= category)
            self.assertEqual(int(response.content), c.id)

        __ = "Test: Add category to unknown parent"
        category = "Grammar"
        attachTo = "English"
        with self.subTest(__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            self.assertEqual(response.status_code, 404)

        __ = "Test: Add category to exam with subject"
        exam = Exam.objects.create(name="IIT")
        # IIT (E)
        Subject.objects.create(name= "Physics", associated_to= 'E', association_id= exam.id)
        # IIT (E) -> Physics (S)
        category = "Science"
        with self.subTest(__, api= api, exam= exam, category= category):
            response = self.client.post(api, {"category": category, "attachTo": exam.name})
            self.assertEqual(response.status_code, 405)

        __ = "Test: Add category to another category with subject"
        c = Category.objects.get(name= "Statistics")
        Subject.objects.create(name="3M", associated_to= 'C', association_id= c.id)
        # CAT (E) -> Aptitude (C) -> Statistics (C) -> 3M (S)
        attachTo = c.name
        category = "Data Models"
        with self.subTest(__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"category": category, "attachTo": attachTo})
            self.assertEqual(response.status_code, 405)

    def test_3_addSubject(self):                
        api = self.url+"exams/addsubject/"
        
        __ = "Test: Accept only POST methods"
        with self.subTest(__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __ = "Test: Add subject without parameters"
        with self.subTest(__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 400)
        
        __ = "Test: Add subject under exam"
        exam = Exam.objects.create(name= "IIT")
        # IIT (E)
        subject = "Physics"
        with self.subTest(__, api= api, exam= exam, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": exam.name})
            s = Subject.objects.get(name= subject)
            self.assertEqual(int(response.content), s.id)

        __ = "Test: Add subject under low-level category"
        exam = Exam.objects.create(name= "GATE")
        # GATE (E)
        category = Category.objects.create(name="Computer Science", exam= exam)
        # GATE (E) -> Computer Science (C)
        subject = "Database"
        with self.subTest(__, api= api, category= category, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": category.name})
            s = Subject.objects.get(name= subject)
            self.assertEqual(int(response.content), s.id)

        __= "Test: Add subject under exam with category"
        # GATE (E) -> Computer Science (C) -> Database (S)
        exam = Exam.objects.get(name= "GATE")
        subject = "Operating System"
        with self.subTest(__, api= api, exam= exam, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": exam.name})
            self.assertEqual(response.status_code, 405)

        __ = "Test: Add subject under inner category"
        # GATE (E) -> Computer Science (C) -> Database (S)
        exam = Exam.objects.get(name= "GATE")
        inCategory = Category.objects.create(name= "Mathematics")
        # GATE (E) -> Computer Science (C) -> Database (S)
        # GATE (E) -> Mathematics (C)
        Category.objects.create(name= "Applied Mathematics", parent= inCategory)
        # GATE (E) -> Mathematics (C) -> Applied Mathematics (C)
        subject = "Operating System"
        with self.subTest(__, api= api, inCategory= inCategory, subject= subject):
            response = self.client.post(api, {"subject": subject, "attachTo": inCategory.name})
            self.assertEqual(response.status_code, 405)

        __ = "Test: Add subject to unknown parent"
        subject = "Grammar"
        attachTo = "English"
        with self.subTest(__, api= api, attachTo= attachTo, category= category):
            response = self.client.post(api, {"subject": category, "attachTo": attachTo})
            self.assertEqual(response.status_code, 404)

    def test_3_addTopic(self):                
        api = self.url+"exams/addtopic/"
        
        __ = "Test: Accept only POST methods"
        with self.subTest(__, api=api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 405)
        
        __ = "Test: Add topic without parameters"
        with self.subTest(__, api= api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 400)
        
        __ = "Test: Add topic under subject"
        exam = Exam.objects.create(name= "IIT")
        # IIT (E)
        subject = Subject.objects.create(name= "Physics", associated_to= 'E', association_id= exam.id)
        # IIT (E) -> Physics (S)
        topic = "Relativity Theory"
        with self.subTest(__, api= api, subject= subject, topic= topic):
            response = self.client.post(api, {"topic": topic, "attachTo": subject.name})
            t = Topic.objects.get(name= topic)
            self.assertEqual(int(response.content), t.id)

        __ = "Test: Add topic under another topic"
        # IIT (E) -> Physics (S) -> Relative Theory (T)
        attachTo = "Relativity Theory"
        topic = "Dark Matter"
        with self.subTest(__, api= api, topic= topic, attachTo= attachTo):
            response = self.client.post(api, {"topic": topic, "attachTo": attachTo})
            t = Topic.objects.get(name= topic)
            self.assertEqual(int(response.content), t.id)

        __ = "Test: Add topic under inner topic"
        # IIT (E) -> Physics (S) -> Relative Theory (T) -> Dark Matter (T)
        attachTo = "Relativity Theory"
        topic = "E=MC^2"
        with self.subTest(__, api= api, topic= topic, attachTo= attachTo):
            response = self.client.post(api, {"topic": topic, "attachTo": attachTo})
            t = Topic.objects.get(name= topic)
            self.assertEqual(int(response.content), t.id)

        __ = "Test: Add topic to unknown parent"
        topic = "Grammar"
        attachTo = "English"
        with self.subTest(__, api= api, attachTo= attachTo, topic= topic):
            response = self.client.post(api, {"topic": topic, "attachTo": attachTo})
            self.assertEqual(response.status_code, 404)
    
    def test_4_getExamDetails(self):
        api = self.url+"exams/getexamdetails/"
        
        __ = "Test: Accept only GET methods"
        with self.subTest(__, api=api):
            response = self.client.post(api)
            self.assertEqual(response.status_code, 405)
        
        __ = "Test: Get Exam details without parameters"
        with self.subTest(__, api= api):
            response = self.client.get(api)
            self.assertEqual(response.status_code, 400)
        
        __ = "Test: Get Exam details of unknown"
        with self.subTest(__, api= api):
            response = self.client.get(api, {"exam":"IIT"})
            self.assertEqual(response.status_code, 404)
        
        __ = "Test: Get Exam details with no subcategory & subject"
        exam = Exam.objects.create(name= "IIT")
        # IIT (E)
        with self.subTest(__, api= api, exam= exam):
            response = self.client.get(api, {"exam": exam.name})
            self.assertEqual(loads(response.content.decode('utf-8')), {"exam": "IIT", "subjects":[]})

        __ = "Test: Get Exam details with subjects and topics"
        # IIT (E)
        subject = Subject.objects.create(name= "Physics", associated_to= 'E', association_id= exam.id)
        # IIT (E) -> Physics (S)
        topic = Topic.objects.create(name="Wave Optics", subject= subject)
        # IIT (E) -> Physics (S) -> Wave Optics (T)
        Topic.objects.create(name="Reflection", parent= topic)
        # IIT (E) -> Physics (S) -> Wave Optics (T) -> Reflection (T)        
        Topic.objects.create(name="Refraction", parent= topic)
        # IIT (E) -> Physics (S) -> Wave Optics (T) -> Refraction (T)        
        Subject.objects.create(name= "Chemistry", associated_to= 'E', association_id= exam.id)
        # IIT (E) -> Chemistry (S)
        with self.subTest(__, api= api, exam = exam):
            response = self.client.get(api, {"exam": exam.name})
            expectedResult = {
                "exam":"IIT",
                "subjects":[
                    {
                        "subject":"Physics",
                        "topics":[
                            {
                                "topic": "Wave Optics", 
                                "subtopics":[
                                    {"topic": "Reflection"},
                                    {"topic": "Refraction"}
                                    ]
                            }]
                    },
                    {
                        "subject":"Chemistry"
                    }
                    ]
                }
            self.assertEqual(loads(response.content.decode('utf-8')), expectedResult)

        __ = "Test: Get Exam details with subcategory, subjects and topics"
        exam = Exam.objects.create(name= "GATE")
        # GATE (E)
        category = Category.objects.create(name= "Computer Science", exam= exam)
        # GATE (E) -> Computer Science (C)        
        subject = Subject.objects.create(name= "Database", associated_to= 'C', association_id= category.id)
        # GATE (E) -> Computer Science (C) -> Database (S)
        Topic.objects.create(name="RDBMS", subject= subject)
        # GATE (E) -> Computer Science (C) -> Database (S) -> RDBMS (T)
        Topic.objects.create(name="NoSQL", subject= subject)
        # GATE (E) -> Computer Science (C) -> Database (S) -> NoSQL (T)      
        subject = Subject.objects.create(name= "Operating System", associated_to= 'C', association_id= category.id)
        # GATE (E) -> Computer Science (C) -> Operating System (S)
        Topic.objects.create(name="Process", subject= subject)
        # GATE (E) -> Computer Science (C) -> Operating System (S) -> Process (T)
        with self.subTest(__, api= api, exam = exam):
            response = self.client.get(api, {"exam": exam.name})
            expectedResult = {                
                "exam":"GATE",
                "categories": [
                    {
                    "category": "Computer Science",
                    "subjects": [
                        {
                            "subject": "Database",
                            "topics":[                                                    
                                    {"topic": "NoSQL"},
                                    {"topic": "RDBMS"}
                                ]                                
                        },
                        {
                            "subject":"Operating System",
                            "topics": [
                                {"topic": "Process"}
                            ]
                        }                                                
                    ]
                    }
                ]                     
                }
            self.assertEqual(loads(response.content.decode('utf-8')), expectedResult)