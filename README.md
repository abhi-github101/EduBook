## Project directory: EduBook
## App directory: EduBook/Exams

## Requirements
- Language: `python >= 3.7.3`
- Framework: `django >= 3.0.8`
- Database: `mysql` or `sqlite`
- External package: `mptt`, install using 
```python
pip install django-mptt
```

## Run Application
- Make sure above requirements are fulfilled
- Open command prompt, from where you can run python
- Move inside the Project directory `EduBook`, using `cd` command
- Create databases using:
```python 
python manage.py migrate
``` 
> Default database is sqlite, change DATABASES settings to use MySQL
- Load database with initial data (Optional): 
```python
# open db shell using
python manage.py shell 
# when inside shell type
from Exams import fixtures
fictures.dbFixtures()
```
- Run app in development using 
```python 
python manage.py runserver
```
- Visit `http://127.0.0.1:8000/` to perform operations using UI

## API End-points
### TASK 1: Create exam
- URL: `http://127.0.0.1:8000:/exams/createexam/`
- Method: `POST`
- Parameter: `{"exam": <string: exam>}`

### TASK 2: Get the list of all exams
- URL: `http://127.0.0.1:8000:/exams/getexamslist/`
- Method: `GET`

### TASK 3: Add sub-categories, subjects and topics under an exam only one record at a time.
#### Add Sub Categories
- URL: `http://127.0.0.1:8000:/exams/addcategory/`
- Method: `POST`
- Parameters: `{"category": <string: new category>, "attachTo": <string: parent category or exam>}`

#### Add Subjects
- URL: `http://127.0.0.1:8000:/exams/addsubject/`
- Method: `POST`
- Parameters: `{"subject": <string: new subject>, "attachTo": <string: parent category or exam>}`

#### Add Topics
- URL: `http://127.0.0.1:8000:/exams/addtopic/`
- Method: `POST`
- Parameters: `{"topic": <string: new topic>, "attachTo": <string: parent topic or subject>}`
            

### TASK 4: Get the entire hierarchy of an exam, its sub-categories their subjects and topics.
- URL: `http://127.0.0.1:8000:/exams/getexamdetails/`
- Method: `GET`
- Parameters: `exam=<string: exam>`

## Database
### Database: edubook
### Tables:
- Exam
- Category
- Subject
- Topic