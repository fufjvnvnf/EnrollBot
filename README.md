# EnrollBot

This python script is intended to be used by Cornell students, especially those affiliated with CS department who are troubled by 
school's overpopulated state to efficiently enrolled into their desired classes. The project is wrote in python 3 along with the 
requests and bs4 library. It continuously checks for availibilities of the students desired classes, and once one of
them is open, models over a student's actions of enrolling into his classes with python codes to almost instantly enroll in it.

# Required

User of this script need to have all his desired classes put in the student center shopping cart manually before running the script.
It is also recommneded that the user does not modify the shopping cart during the running of the script.

# User Manual

Run the python code. Put in your netid and password as asked, and wait for the program to close.

# General Strategy

Upon recieved the netid and password of the student, the script first log in on student center and acquire the list of classes in the 
student's shopping cart. It then goes to cornell class roster (classes.cornell.edu) to check for those classes' availabilities. When any
of the class is available in all the sections that the student chooses, it logs back in on student center to perform the actual enrollment.
It then records the shopping cart again and repeat the process until the shopping cart is empty. 

# Safety
The script does not perform bombarding requests to student center, which would otherwise be noticed by school's network monitor and ends
up in network policy violation; the script on logs in the student center upon the start of the script, and every time a spot of the class
is open up, which is not often. Rather, the script performs bombarding requests to the class roster website, which does not require a
logged-in netid to view the availibities of the classes, and thus would not leave obvious evidence of bombardment, even when the requests
got noticed by the school. In general, the script should be safe to use in policy-wise, unless the school reads what I'm writing here.
