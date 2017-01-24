import sys
import requests
from bs4 import BeautifulSoup

def login():
    
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
    
    #initially going to studentcenter.cornell.edu
    url1 = "http://studentcenter.cornell.edu"
    r1 = s.get(url1)
    weburl = r1.url[:30] #web*.cornell.edu
    url2 = weburl+'/'+BeautifulSoup(r1.content,"lxml").form.get('action')
    global netid
    global pwd
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

    except KeyError:
        print ("Login fails.")
        netid = input('NetID: ')
        pwd = input('Password: ')
        login()
    
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
            login()
        else:
            sys.exit()
    
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
def recordCart():
    login()
    #click enroll on student center main page
    url4 = 'https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None'
    r4 =  s.get(url4)
    soup = BeautifulSoup(r4.content,"lxml")
    if (soup.title.string)!= 'Enrollment Shopping Cart':
        print('Error in code')
        sys.exit()
    classes = soup.find_all('span', id = lambda x: x and x.startswith('P_CLASS_NAME$span$'))
    rtn = []
    for each in classes:
        rtn.append(each.text.rsplit('\r', 1)[0])
    print('You currently want to enroll in: ')
    print(rtn)
    s.cookies.clear()
    return rtn
    
# return true if there is a class with open spot
def checkEmpty(classes):
    #todo
    url = 'https://classes.cornell.edu/search/ajax/roster/SP17'
    i = 0;
    headers = {
        'Referer': 'https://classes.cornell.edu/browse/roster/SP17',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'}
    while i<len(classes):
        allsecs = [classes[i]]
        i+=1
        while(i<len(classes) and classes[i-1].rsplit('-', 1)[0]==classes[i].rsplit('-', 1)[0]):
            allsecs.append(classes[i])
            i+=1
        payload = {
            'q': allsecs[0].rsplit('-', 1)[0],
            'days-type': 'any',
            'pi': ""}
        
        soup = BeautifulSoup(requests.get(url, headers = headers, params=payload).content, 'lxml')
        classname = allsecs[0].rsplit('-', 1)[0]
        print('Checking availability for '+classname+' ...')
        sections = soup.find('div', attrs={"class": 'node', "data-subject": classname.split()[0],"data-catalog-nbr":classname.split()[1]}).find('div',class_ = 'sections')
        open = True
        for each in allsecs:
            sec = each.rsplit('-', 1)[1]
            secsoup = sections.find('ul', attrs={"aria-label":lambda x: x and x.endswith(sec)})
            status = secsoup.find('i', attrs = {"class":lambda x: x and x.startswith('fa fa-')})
            if(status['class'][2]=="open-status-closed"):
                open = False
                break
        if(open):
            return True
    return False

# actually enroll into the classes
def enroll():
    login()
    # go to shopping cart
    url4 = 'https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None'
    r4 =  s.get(url4)
    soup = BeautifulSoup(r4.content,"lxml")
    if (soup.title.string)!= 'Enrollment Shopping Cart':
        print('Error in code')
        sys.exit()
    # proceeding to step 2
    url5 = BeautifulSoup(r4.content,"lxml").find('form', {'name': 'win0'}).get('action')
    step1inputs = ['ICType','ICElementNum','ICStateNum','ICXPos','ICYPos','ResponsetoDiffFrame',
    'TargetFrameName','FacetPath','ICFocus','ICSaveWarningFilter','ICChanged','ICResubmit','ICSID','ICActionPrompt', 
    'ICFind','ICAddCount','ICAPPCLSDATA']
    step1data =  findHidden(step1inputs, r4.content)
    step1data['ICAJAX'] = '1'
    step1data['ICAction'] = 'DERIVED_REGFRM1_LINK_ADD_ENRL$82$'
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
    r5 = s.post(url5, data = step1data, headers = step1headers)
    warning = BeautifulSoup(r5.content,'lxml').find('div',id="win0divDERIVED_SASSMSG_GROUP1")
    while warning!= None:
        print('You do not have a valid enrollment time. Trying again or press ctrl+c to exit.')
        r5 = s.post(url5, data = step1data, headers = step1headers)
        warning = BeautifulSoup(r5.content,'lxml').find('div',id="win0divDERIVED_SASSMSG_GROUP1")
    url6 = 'https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_ADD.GBL?Page=SSR_SSENRL_ADD_C&Action=U&ACAD_CAREER=UG&EMPLID=4371385&ENRL_REQUEST_ID=&INSTITUTION=CUNIV&STRM=2657&TargetFrameName=None'
    r6 = s.get(url6)
    step2inputs = ['ICType','ICElementNum','ICStateNum','ICXPos','ICYPos','ResponsetoDiffFrame',
    'TargetFrameName','FacetPath','ICFocus','ICSaveWarningFilter','ICChanged','ICResubmit','ICSID','ICActionPrompt', 
    'ICFind','ICAddCount','ICAPPCLSDATA']
    step2data =  findHidden(step2inputs, r6.content)
    step2data['ICAJAX'] = '1'
    step2data['ICNAVTYPEDROPDOWN'] = '0'
    num = int(BeautifulSoup(r6.content,'lxml').find('span',style="font-size:80%;").text.split()[2]) - 1
    action = '#ICRow'+ str(num)
    step2data['ICAction'] = action
    url7 = 'https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_ADD.GBL'
    r7 = s.post(url7, data = step2data)
    step3inputs = ['ICType','ICElementNum','ICStateNum','ICXPos','ICYPos','ResponsetoDiffFrame',
    'TargetFrameName','FacetPath','ICFocus','ICSaveWarningFilter','ICChanged','ICResubmit','ICSID','ICActionPrompt', 
    'ICFind','ICAddCount','ICAPPCLSDATA']
    step3data =  findHidden(step2inputs, r7.content)
    step3data['ICAJAX'] = '1'
    step3data['ICNAVTYPEDROPDOWN'] = '0'
    step3data['ICAction'] = 'DERIVED_REGFRM1_SSR_PB_SUBMIT'
    step3data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
    step3data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'
    s.post(url7, data = step3data)
    s.cookies.clear()
    print('Success')

def recordAndCheck():
    classes = recordCart()
    s.cookies.clear()
    while(len(classes)!=0):
        print('Checking if any class opens up')
        if(checkEmpty(classes)):
            print('Yep. Enrolling them')
            enroll()
            print('Relogging to check your classes')
            classes = recordCart()
            continue
        else:
            print('Nope. Checking again')
    print('Done. All classes enrolled.')

# main
def main():
    global s
    s = requests.session()
    global netid
    netid = input('NetID: ')
    global pwd
    pwd = input('Password: ')
    recordAndCheck()

if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        print('\nProgrammed terminated before all classes are enrolled.')
        sys.exit()
    except:
        recordAndCheck()
        
    