class Question():
    _options = []

    def __init__(self, uid,description,options=None):
        self._options = []
        self.uid = uid
        self.description = description
        self._options = []

    def get_options(self):
        return self._options

    def add_option(self, option):
         self._options.append(option)
    

    def add_options(self, options):
        self._options.extend(options)

    def get_correct_options(self):
        return [opt for opt in self._options if opt.is_correct]
    
    def score_response(self, response):
        """
            We calculate student scores by 
            adding one if any of their selected 
            option is in the get_correct_options 
            and reduce one if otherwise

            :Return 0 if count is a negative value else count
        """
        count = 0
        for opt in self.get_correct_options():
            if opt in response:
                count += 1
            else:
                count -= 1

        return count if count >= 0 else 0 

    def __hash__(self):
        return hash(self.uid)
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.uid == other.uid


class Option():
    def __init__(self, description, is_correct=False):
        self.description = description
        self.is_correct = is_correct

    def __str__(self):
        return '{} is correct [{}]'.format(self.description, self.is_correct)

    def __repr__(self):
        return self.__str__()

class Quiz():
    _questions = []

    def __init__(self, title):
        self._questions = []
        self.title = title

    def add_question(self, question: Question) -> Question:
        self._questions.append(question)
        return question
    
    def get_questions(self) -> list:
        return self._questions

    def __str__(self):
        return  "{}".format(self.title)



class Teacher(): 
    _quiz = []
    _class = []

    def __init__(self, sno, name):
        self.sno = sno
        self.name =  name

    def create_quiz(self, quiz: Quiz) -> str:
        self._quiz.append(quiz)
        return "New  Quiz {}".format(quiz)

    def get_all_quiz(self):
        return self._quiz

    def set_klass(self, klass):
        self._class.append(klass)

class Student():
    klass = None
    quizes = []

    def __init__(self, sid, lastname, firstname, othername=None):
        self.sid = sid
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.quizes = []

    def set_klass(self, kls):
        self.klass = kls

    def get_quizes(self):
        return self.quizes

    def take_quiz(self, quiz):
        self.quizes.append(quiz)

    def __hash__(self):
        return hash(self. sid)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and  self.sid == other.sid

class Klass():
    students = []
    teachers  = []

    def __init__(self, name):
        self.name = name
        self.students = []
        self.teachers = []
 
    def add_student(self, student: Student) -> Student:
        student.set_klass(self)
        self.students.append(student)
        return student 

    def get_students(self):
        return self.students

    def add_teacher(self, teacher):
        # add this class to the list of classes this teacher teaches
        teacher.set_klass(self)
        self.teachers.append(teacher)
        return teacher
    
    
    def get_teachers(self):
        return self.teachers


class Submission():
    question = None
    selected_options = []
    quiz = None

    def __init__(self, question, quiz=None, selected_options=None):
        self.question = question
        self.selected_options = selected_options
        self.quiz = quiz


class StudentSubmission():

    _submissions = {}

    def submit(self,student, submission):
        if student in self._submissions:
            self._submissions[student].append(submission)
        else:
            self._submissions[student] = [submission]
        #student.add_submission(submission)
        

    def get_submissions(self):
        return self._submissions

    def find_submission(self, student):
        if student not in self._submissions:
            raise KeyError('Could not find this student submission')
        return self._submissions[student]
        

        

class Grader():

    def __init__(self, quiz=None):
        self.quiz = quiz


    def grade(self, student_submissions):
        # get all the question that belongs to this
        # quiz from the student submission

        scores = []
        for submission in student_submissions:
            question = submission.question
            if submission.quiz == self.quiz:
                # grade this 
                scores.append(question.score_response(submission.selected_options))
        return scores
