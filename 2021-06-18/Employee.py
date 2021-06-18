from datetime import datetime
import json

task=[]
class Employee:
     def __init__(self, emp_name, emp_id):
         self.emp_name = emp_name
         self.emp_id = emp_id

     def login_time(self):
         return datetime.now().strftime("%Y-%m-%d %H:%M")

     def logout_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M")

     def start_task(self,task_title , task_description):
        return task_title,task_description

     def end_task(self,task_success):
        return task_success

     def start_time(self):
         return datetime.now().strftime("%Y-%m-%d %H:%M")

     def end_time(self):
         return datetime.now().strftime("%Y-%m-%d %H:%M")


e1=Employee('Anisha',1)
task_title1, task_description1 = e1.start_task('Python class','program to display the details of a student')
task_title2, task_description2 = e1.start_task('Python basics and operations','create a python class that will be used by each employee to log their task and create a json file for the same')
task_title3, task_description3 = e1.start_task('string sorting','program to sort the string into lists of numeric ,alphanumeric and digits ')
status1=e1.end_task('True')
status2=e1.end_task('False')
status3=e1.end_task('True')


task1={
    'task_title':task_title1,
    'task_description':task_description1,
    'start_time':e1.start_time(),
    'end_time':e1.end_time(),
    'task_sucess':status1
}
task2={
    'task_title':task_title2,
    'task_description':task_description2,
    'start_time':e1.start_time(),
    'end_time':e1.end_time(),
    'task_sucess':status3
 }
task3={
    'task_title':task_title3,
    'task_description':task_description3,
    'start_time':e1.start_time(),
    'end_time':e1.end_time(),
    'task_sucess':status3
 }
task.append(task1)
task.append(task2)
task.append(task3)


details = {
    'name': e1.emp_name,
    'emp_id':e1.emp_id,
    'login_time': e1.login_time(),
    'logout_time':e1.logout_time(),
    'task': task
}
print(details)

with open("2021-06-18 Anisha.json","w") as fp:
     json.dump(details,fp)