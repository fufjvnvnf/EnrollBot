import sys
import requests

netid = input('NetID: ')
pwd = input('Password: ')

def login(neitid, pwd):

    posturl = "https://web1.login.cornell.edu/loginAction?SID=E59932FB1C9F98BC&WAK0Service=https/css.adminapps.cornell.edu@CIT.CORNELL.EDU&WAK2Name=&WAK0Realms=&ReturnURL=https://css.adminapps.cornell.edu/E59932FB1C9F98BC/cuwal2.c0ntinue&VerP=3&VerC=2.3.0.229/idmbuild@fox02.serverfarm.cornell.edu/RedHat6-64bit-55/2.2.15&VerS=Apache%2020161127-0144&VerO=Linux%20m223122lweb2002%202.6.32-642.6.2.el6.x86_64%20%231%20SMP%20Mon%20Oct%2024%2010:22:33%20EDT%202016%20x86_64%20x86_64%20x86_64%20GNU/Linux%20AT&T%20Hosting%20Linux%20Reference%20System%20%20RHEL%206%20%20-%20installed%2008-02-14%2012:35%20UTC%20&Accept=K2&WANow=1483685814&WAK2Flags=0&WAreason=1"

    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Content-Length":"48",
        "Content-Type":"application/x-www-form-urlencoded",
        "Cookie":"_gat=1; _ga=GA1.2.540418443.1483432046",
        "Host":"web1.login.cornell.edu",
        "Origin":"https://web1.login.cornell.edu",
        "Referer":"https://web1.login.cornell.edu/?SID=E59932FB1C9F98BC&WAK0Service=https/css.adminapps.cornell.edu@CIT.CORNELL.EDU&WAK2Name=&WAK0Realms=&ReturnURL=https://css.adminapps.cornell.edu/E59932FB1C9F98BC/cuwal2.c0ntinue&VerP=3&VerC=2.3.0.229/idmbuild@fox02.serverfarm.cornell.edu/RedHat6-64bit-55/2.2.15&VerS=Apache%2020161127-0144&VerO=Linux%20m223122lweb2002%202.6.32-642.6.2.el6.x86_64%20%231%20SMP%20Mon%20Oct%2024%2010:22:33%20EDT%202016%20x86_64%20x86_64%20x86_64%20GNU/Linux%20AT&T%20Hosting%20Linux%20Reference%20System%20%20RHEL%206%20%20-%20installed%2008-02-14%2012:35%20UTC%20&Accept=K2&WANow=1483685814&WAK2Flags=0&WAreason=1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}

    values = {
        'netid': netid,
        'password': pwd,
        'Submit': 'Login'
    }
    s = requests.Session()

    r = s.post(posturl, data=values, headers=header)

    try:
        r.cookies['cuwlrelogin']
        print ("Success")

    except KeyError:
        print ("Login fails.")
        sys.exit()

login(netid, pwd)
