from flask import Flask, escape, request
from markupsafe import escape

app = Flask(__name__)

class Student:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.courses = []
        self.all_courses = ''  
    def add_classes(self,coursename):
        self.courses.append(coursename)  
        #self.update_all_courses(coursename)  
    def getID(self):
        return self.id    
    def getname(self):
        return self.name
    def update_all_courses(self,coursename):
        self.all_courses= self.all_courses + coursename + '\n'
    def get_all_courses(self):
        return self.all_courses 

class Classes:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.student = []
        self.all_student = ''    
    def add_student(self,studentID):
        self.student.append(studentID)
        self.update_all_student(studentID)
    def getID(self):
        return self.id    
    def getname(self):
        return self.name
    def update_all_student(self,studentID):
        self.all_student = self.all_student+studentID+'\n'
    def get_all_students(self):
        return self.all_student


Student_info_DB = []
class_info_DB = []
current_class_id = 0

@app.route('/')
def index():
    return "hello world"
####################################################
@app.route('/student',methods=['POST'])
def add_student():
    if request.method == 'POST':
        data = request.json
        studentname = data['name']
        ID = data['ID']
        Student_info_DB.append(Student(ID,studentname))
        return """student name {} with ID {} \
            is added""".format(studentname,ID)
        #return Student_info_DB[0].getID()

@app.route('/student/<studentID>')
def get_studentID(studentID):
    for i in range (len(Student_info_DB)):
        if Student_info_DB[i].getID() == studentID:
            #return Student_info_DB
            return """student ID: {} \n
                name: {}""".format(Student_info_DB[i].getID(),
                Student_info_DB[i].getname())
    return ('no student found')
#{"ID" : "0001" , "name" : "YS"}
#######################################################
@app.route('/class',methods = ['POST'])
def add_classes():
    if request.method == 'POST':
        data = request.json
        class_name = data['class_name']
        global current_class_id
        class_info_DB.append(Classes(current_class_id,class_name))
        current_class_id+=1

        return """ID: {}\n name: {}
            """.format(class_info_DB[current_class_id-1].getID()
                ,class_info_DB[current_class_id-1].getname())

@app.route('/class/<courseID>',methods = ['POST','GET'])
def class_check_update(courseID):
    if request.method == 'GET':
        for i in range (len(class_info_DB)):
            if courseID == (str)(class_info_DB[i].getID()):
                return """ course ID: {} \n course name:{}
                """.format(courseID,class_info_DB[i].getname())
        return ('no course found')

    elif request.method == 'POST':
        data = request.json
        student_ID = data['student_id']
        for i in range (len(class_info_DB)):
            #class add student
            if courseID == (str)(class_info_DB[i].getID()):
                class_info_DB[i].add_student(student_ID)
                for j in range (len(Student_info_DB)):
                    if student_ID == (str)(Student_info_DB[j].getID()):
                        Student_info_DB[j].add_classes(class_info_DB[i].getID())
                        return """ course id: {}
                                    course name: {}
                                    student take this course: {}
                                """.format(courseID, 
                                    class_info_DB[i].getname(),
                                    class_info_DB[i].get_all_students())
                return ('student not found')
        return ('class not found')
    return ('method not found')
#add class {"class_name" : "CMPE-273"}
#add student to class {"student_id" : "0003"}




if __name__ =="__main__":
    app.run(debug=True)

