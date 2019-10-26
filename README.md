# Back Storage structure

```
├── README.md
├── router.py
├── students
│   └── grade\ 1
│       └── A
│           ├── 10000.json  // student personal ID
│           └── 10001.json  // student personal ID
└── subjects
    ├── literature_4_2019   // custom subject
    │   └── lesson1         // folders with lessons
    │       ├── lesson1.json
    │       ├── media
    │       │   └── e1.jpg
    │       └── tasks
    │           └── task1.json
    └── personal_assessment_2019   // tests to detect personal types for each student
        ├── dyslexia_test
        │   └── tasks
        │       └── test.json
        └── type_of_learner_test
            └── tasks
                └── test.json


```

# Requests API Doc

## Teacher 

These are requests samples that we will implement  (not final system version)
 1. GET lesson content
 2. POST send tasks to students
 
 ## Student
 
 1. GET lesson content (with personalized parameters)
 2. GET assigned active tasks 
 3. POST unclear content (mark a certain place on a slide, slide ID)
 4. POST question  (text and slide ID)
 
 