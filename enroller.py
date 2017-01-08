import sys
import requests
from bs4 import BeautifulSoup

# Global Session object
s = requests.session()
g_netid = ""
g_pwd = ""
classes = none

def login(n, p):

    netid = n
    pwd = p
    
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
    
    #initially going to studentcenter.cornell.edu
    url1 = "http://studentcenter.cornell.edu"
    r1 = s.get(url1)
    weburl = r1.url[:30] #web*.cornell.edu
    url2 = weburl+'/'+BeautifulSoup(r1.content,"lxml").form.get('action')
    values2 = {
        'netid': netid,
        'password': pwd,
        'Submit': 'Login'
    }
    r2 = s.post(url2, data=values2)
    
    # check cookie for successful login
    try:
        cookie = s.cookies['cuwlrelogin']
        print ("Credential passed.")
        g_netid = n
        g_pwd = p

    except KeyError:
        print ("Login fails.")
        login(input('NetID: '), input('Password: '))
    
    #c0ntinue
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
    if (BeautifulSoup(r3.content,"lxml").title.string)!= 'Student Center':
        print('Server currently down. Failed to enter student center.')
        ans = input('Retry login? [y/n]')
        if ans=='y':
            relogin()
        else:
            sys.exit()
    else: print('Successfully entered student center')
    
def relogin():
    login(g_netid, g_pwd)
    
# used to find hidden values for form data
def findHidden(strs, content):
    data = {}
    for arg in strs:
        try:
            data[arg] = BeautifulSoup(content,"lxml").find('input', {'id': arg}).get('value')
        except:
            pass
    return data

# record classes in the shopping cart; return as string list
def recordCart(content):
    
# return true if there is a class with open spot
def checkEmpty():


# actually enroll into the classes
def enroll():
    # proceeding to step 2
    url5 = BeautifulSoup(r4.content,"lxml").find('form', {'name': 'win0'}).get('action')
    step2inputs = ['ICType','ICElementNum','ICStateNum','ICAction','ICXPos','ICYPos','ResponsetoDiffFrame',
    'TargetFrameName','FacetPath','ICFocus','ICSaveWarningFilter','ICChanged','ICResubmit','ICSID','ICActionPrompt', 
    'ICFind','ICAddCount','ICAPPCLSDATA']
    step1data =  findHidden(step2inputs, r4.content)
    step1data['ICAJAX'] = '1'
    step1data['ICNAVTYPEDROPDOWN'] = '0'
    step1data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
    step1data['DERIVED_REGFRM1_CLASS_NBR'] = ''
    step1data['DERIVED_REGFRM1_SSR_CLS_SRCH_TYPE$249$'] = '06'
    step1data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
    step1headers = {
        'Origin': 'https://css.adminapps.cornell.edu',
        'Referer': url4,
        'Host': 'css.adminapps.cornell.edu',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate, br'}
    r5 = s.post(url4, data = step1data, headers = step1headers)
    ###TODO###
    '''
    Got stuck on proceed to step 2. Does not show warnning div.
    '''
    ###at the end 
#     recordCart(sth)

# main
if __name__ == '__main__':
    login(input('NetID: '), input('Password: '))
    #click enroll on student center main page
    url4 = 'https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None'
    r4 =  s.get(url4)
    classes = recordCart(r4.content)
    while(len(classes)!=0):
        print('Checking if any class opens up')
        if(checkEmpty(classes):
            print('Yep. Enrolling them')
            enroll()
        else:
            print('Nope. Checking again')
            continue
    print('Done. All classes enrolled.')
    
   


    

