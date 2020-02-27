from flask import Flask, escape, request, jsonify
from ariadne import QueryType, graphql_sync, make_executable_schema,ObjectType,MutationType
from ariadne.constants import PLAYGROUND_HTML

app=Flask(__name__)

type_defs = """
    type Student {
        student_id: Int!
        student_name:String!
    }

    type Classes {
        class_id:Int!
        class_name:String!
        who_take:[Student]
    }

    type Query{
        get_student(student_id:Int!):Student
        get_classes(class_id:Int!):Classes
        get_all_student: [Student]
        get_all_classes:[Classes]
    }

    type Mutation{
        add_student(name:String!):Student!
        add_class(name:String!):Classes!
        update_class(class_id:Int!,student_id:Int!):Classes
    }
"""

query = QueryType()
mutation = MutationType()


DB = {
    "student":[],
    "classes":[]
}

#initial id
sid = 0
cid = 1000
#query student and class
@query.field("get_student")
def resolve_Student(_, info,student_id):
    for Student in DB["student"]:
        if student_id == Student["student_id"]:
            return Student
    return None

@query.field("get_classes")
def resolve_Classes(_, info,class_id):
    for Classes in DB["classes"]:
        if class_id == Classes["class_id"]:
            return Classes     
    return None

@query.field("get_all_student")
def resolve_get_all_student(_,info):
    return DB["student"]

@query.field("get_all_classes")
def resolve_get_all_classes(_,info):
    return DB["classes"]

#new student, new classes, add student to class

@mutation.field("add_student")            # mutation{
def resolve_add_student(_,info,name):     # add_student(name:"YS"){
    global sid                            # student_id}}
    Student = {'student_id' : sid,
                'student_name' : name}
    sid+=1
    DB['student'].append(Student)
    return Student

@mutation.field("add_class")             # mutation{
def resolve_add_class(_,info,name):      # add_class(name:"CMPE-273"){
    global cid                           # class_id}}
    Class = {'class_id' : cid,
             'class_name' : name,
             'who_take': []
            }
    cid+=1 
    DB['classes'].append(Class)
    return Class
 
@mutation.field("update_class")                          # mutation{
def resolve_update_class(_,info,class_id,student_id):    # update_class(class_id:1001,student_id:1){
    for Class in DB["classes"]:
        if class_id == Class["class_id"]:
            for Student in DB["student"]:
                if student_id == Student["student_id"]:
                    Class["who_take"].append(Student)
                    return Class
            return None
    return None















schema = make_executable_schema(type_defs,[query,mutation])


@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)