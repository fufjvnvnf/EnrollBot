import sys
import requests
from bs4 import BeautifulSoup

netid = input('NetID: ')
pwd = input('Password: ')

def login(neitid, pwd):
    
    s = requests.Session()
    
    #initially going to studentcenter.cornell.edu
    url1 = "http://studentcenter.cornell.edu"
    r1 = s.get(url1)
    weburl = r1.url[:30]
    url2 = weburl+'/'+BeautifulSoup(r1.content,"lxml").form.get('action')
    values2 = {
        'netid': netid,
        'password': pwd,
        'Submit': 'Login'
    }
    r2 = s.post(url2, data=values2)
    
    try:
        cookie = s.cookies['cuwlrelogin']
        print ("Success")

    except KeyError:
        print ("Login fails.")
        sys.exit()
        
    url3 = BeautifulSoup(r2.content,"lxml").form.get('action')
    data3 = {'wa': cookie}
    r3 = s.post(url3, data=data3)
    print (s.cookies['CornellUniv_SID23122_cookie_persist'])
    print (s.cookies['cuwltgttime'])
    print (s.cookies['SignOnDefault'])
    
    
    
    
   #  prepare to post to web1
#     posturl = "https://web1.login.cornell.edu/loginAction?SID=E59932FB1C9F98BC&WAK0Service=https/css.adminapps.cornell.edu@CIT.CORNELL.EDU&WAK2Name=&WAK0Realms=&ReturnURL=https://css.adminapps.cornell.edu/E59932FB1C9F98BC/cuwal2.c0ntinue&VerP=3&VerC=2.3.0.229/idmbuild@fox02.serverfarm.cornell.edu/RedHat6-64bit-55/2.2.15&VerS=Apache%2020161127-0144&VerO=Linux%20m223122lweb2002%202.6.32-642.6.2.el6.x86_64%20%231%20SMP%20Mon%20Oct%2024%2010:22:33%20EDT%202016%20x86_64%20x86_64%20x86_64%20GNU/Linux%20AT&T%20Hosting%20Linux%20Reference%20System%20%20RHEL%206%20%20-%20installed%2008-02-14%2012:35%20UTC%20&Accept=K2&WANow=1483685814&WAK2Flags=0&WAreason=1"
# 
#     values = {
#         'netid': netid,
#         'password': pwd,
#         'Submit': 'Login'
#     }
#     
#     r1 = s.post(posturl, data=values)
#     

#         
#     go to continue
#     geturl = r1.headers['Location']
#     data2 = {'wa': cookie}
#         
#     r = s.post(geturl, data = data2)
#     print (r.headers)
#     print (s.cookies)
    

login(netid, pwd)

