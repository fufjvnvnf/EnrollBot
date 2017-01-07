import sys
import requests
from bs4 import BeautifulSoup

netid = input('NetID: ')
pwd = input('Password: ')

def login(neitid, pwd):
    
    s = requests.session()
    
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
    
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
    hidden = BeautifulSoup(r2.content,"lxml").form.input.get('value')
    data3 = {'wa': hidden}
    ccookies = {
        'SignOnDefault': netid.upper(),}
    headers = {
        'Origin': weburl,
        'Referer': url2,
        'Host': 'css.adminapps.cornell.edu'}
    r3 = s.post(url3, data=data3, cookies = ccookies, headers = headers)
    print (r3.content)

login(netid, pwd)

