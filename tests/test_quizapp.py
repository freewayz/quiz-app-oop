from quizapp import(
    __version__,
    Teacher,
    Student,
    Quiz, 
    Option, 
    Submission,
    StudentSubmission,
    Grader,
    Klass,
    Question)
from unittest import mock
import logging
import random



logging.basicConfig(level=logging.DEBUG)
t_log  = logging.getLogger()

def test_version():
    assert __version__ == '0.1.0'


def create_random_options():
    sample_size = random.sample(list('abcdefghijklmnopqrstuvwxyz'), 4)
    # just make all the third options the corrects ones
    return [Option(opt, i==2) for i, opt in enumerate(sample_size)]

def pickRandom(items, qty=1):
    return random.sample(items, qty)


def test_that_student_create():
    student = Student(10,'Peter', 'Edache')
    assert student.lastname == 'Peter'
    assert student.firstname == 'Edache'
    assert student.sid == 10

def test_that_student_can_belong_to_a_klass():
    student1 = Student(1, 'Test', 'Python')
    student2 = Student(2, 'Test', 'Java')
    klass = Klass(name='JSS 1')
    assert klass.name == 'JSS 1'
    klass.add_student(student1)
    klass.add_student(student2)
    assert len(klass.get_students()) == 2
    assert student1.klass == klass

def test_that_teacher_can_teach_a_class():
    t = Teacher(12,'Teacher')
    klass = Klass(name='JSS 2')
    klass.add_teacher(t)
    assert len(klass.get_teachers()) == 1
    klass2 = Klass(name='PRI 1')
    

def test_that_teacher_can_be_created():
    t = Teacher(12, 'Peter')
    assert t is not None
    assert t.name == 'Peter'

def test_that_option_can_be_created():
    option = Option('The Boy')
    assert option.is_correct == False
    assert option.description == 'The Boy'
    correct_option = Option('Coroutine', True)
    assert correct_option.is_correct == True

def test_that_question_can_be_created():
    question = Question(
        uid=12233,
        description='Some question',
    )
    assert question.description == 'Some question'
    

def test_that_quiz_can_be_created():
    q = Quiz(title='Mathematics')
    assert q.title == 'Mathematics'



def test_that_quiz_can_have_question():
    q = Quiz(title='CS101')
    assert q.title == 'CS101'

    for i in range(1, 10):
        q.add_question(Question(i, 'Some random question'))
    assert len(q.get_questions()) == 9


def test_that_teacher_can_be_create_quiz():
    t = Teacher(10, 'Peter Edache')
    assert t is not None
    quiz = Quiz(title='The adventure of python')
    t.create_quiz(quiz)
    assert len(t.get_all_quiz()) == 1

    for i in range(4):
        quiz.add_question(Question(i, 'Question {}'.format(i)))
    assert len(quiz.get_questions()) == 4
    assert len(t.get_all_quiz()) == 1

@mock.patch('quizapp.Quiz')
@mock.patch('quizapp.Student')
def test_that_student_can_take_quiz(Student, quiz):
    student = Student.return_value
    student.get_quizes.return_value =  1
    assert student.sid != None
    student.take_quiz(quiz)
    assert student.get_quizes() == 1
  

@mock.patch('quizapp.Klass')
@mock.patch('quizapp.Teacher')
def test_that_student_can_make_submission(Teacher, Klass):
    student = Student(10, 'Peter', 'Edache', 'Agbo')
    quiz = Quiz(title='This is from Jagaban')
    # create question 
    for i in range(10):
        question = Question(i, 'Question {}'.format(i))
        question.add_options(create_random_options())
        quiz.add_question(question)

    assert len(quiz.get_questions()) == 10
    assert len(student.get_quizes()) == 0
    student.take_quiz(quiz)
    assert len(student.get_quizes()) == 1

    student_submissions = StudentSubmission()
    # make a random submission for this student
    for question in quiz.get_questions():
        # just pick random options from this question and use that 
        # as the student selected choice
        options = question.get_options()
        student_submissions.submit(student, Submission(question,quiz, pickRandom(options, 1)))
    
    mysubmissions = student_submissions.find_submission(student)
    assert len(mysubmissions) == 10
    # do the grading 
    grader = Grader(quiz)
    scores = grader.grade(mysubmissions)
    # check that 10 question where marked
    assert len(scores) == 10

