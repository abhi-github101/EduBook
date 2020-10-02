## Project directory: EduBook
## App directory: EduBook/Exams

## Requirements
- Language: `python >= 3.7.3`
- Framework: `django >= 3.0.8`
- Database: `mysql` or `sqlite`
- External package: `mptt`, install using 
```python
C:\> pip install django-mptt
```

## Run Application
- Make sure above requirements are fulfilled
- Open command prompt, from where you have access to `python`
- Move inside the Project directory `EduBook`, using `cd` command
- Create databases using:
```python 
C:\..\Edubook> python manage.py migrate
``` 
> Default database is sqlite, change DATABASES settings to use MySQL
- Load database with initial data (Optional): 
```python
# open db shell using
C:\...\Edubook> python manage.py shell 

# when inside shell
In [1] from Exams import fixtures
In [1] fixtures.dbFixtures()
```
- Run app in development using 
```python 
C:\...\Edubook> python manage.py runserver
```
- Visit `http://127.0.0.1:8000/` to access APIs through UI

## API End-points
### TASK 1: Create exam
- URL: `http://127.0.0.1:8000:/exams/createexam/`
- Method: `POST`
- Parameter: `{"exam": <string: exam>}`
- Returns: <string: new exam id or "Exists" if Exam already created>
- Constraints: 
    - It will only create unique Exams.

### TASK 2: Get the list of all exams
- URL: `http://127.0.0.1:8000:/exams/getexamslist/`
- Method: `GET`
- Returns: Json data, eg. {"exams": [\<list of all exams\>]}

### TASK 3: Add sub-categories, subjects and topics under an exam only one record at a time.
#### Add Sub Categories
- URL: `http://127.0.0.1:8000:/exams/addcategory/`
- Method: `POST`
- Parameters: `{"category": <string: new category>, "attachTo": <string: parent category or exam>}`
- Returns: <string: new category id>
- Constraints: 
    - It will only create unique category.
    - It will not create sub-category if subject is already present at that node, and will respond with `Method Not Allowed` in such situation.

#### Add Subjects
- URL: `http://127.0.0.1:8000:/exams/addsubject/`
- Method: `POST`
- Parameters: `{"subject": <string: new subject>, "attachTo": <string: parent category or exam>}`
- Returns: <string: new subject id>
- Constraints: 
    - It will only create unique subjects.
    - It will only add subject to lowest-level sub-category or exam with no sub-category. 
    - If `attachTo` points to inner sub-category or exam with sub-category it will respond with `Method Not Allowed`.

#### Add Topics
- URL: `http://127.0.0.1:8000:/exams/addtopic/`
- Method: `POST`
- Parameters: `{"topic": <string: new topic>, "attachTo": <string: parent topic or subject>}`
- Returns: <string: new topic id>
- Constraint: 
    - It will only create unique topics
            

### TASK 4: Get the entire hierarchy of an exam, its sub-categories their subjects and topics.
- URL: `http://127.0.0.1:8000:/exams/getexamdetails/`
- Method: `GET`
- Parameters: `exam=<string: exam>`
- Returns: Json data

## Database
### Database: **edubook**
### Tables:
- **exam**: For exam information
- **category**: For category and their sub-categories information
- **subject**: For subject information
- **topic**: For topic and their sub-topics information