import re
from urllib.request import urlopen

##Shameless code resue from another repo of mine

#Function to input code from bot and return the response
def callsign_start(call):
    callsign = call
    url = ('http://radioreference.com/apps/ham/callsign/%s' % callsign)
    callsign_query = urlopen(url)
    content = callsign_query.read()

    rel = '<span style="font-size: 16px; font-weight: bold;">(.*?)</span>'
    rg = re.compile(rel, re.IGNORECASE | re.DOTALL)
    m = rg.search(content.decode('utf-8'))
    if m:
        ham_name = m.group(1)
        #print("Name: (" + ham_name + ")" + "\n")

    re2 = '<img src="http://s.radioreference.com/assets/flags_iso/64/(.*?).png">'
    rg = re.compile(re2, re.IGNORECASE | re.DOTALL)
    m = rg.search(content.decode('utf-8'))
    if m:
        ham_country = m.group(1)
        #print("Country: (" + ham_country + ")" + "\n")

    # regex for the hams license status, print to screen

    re3 = '<tr><th>License Status</th><td>(.*?)</td></tr>'
    rg = re.compile(re3, re.IGNORECASE | re.DOTALL)
    m = rg.search(content.decode('utf-8'))
    if m:
        ham_lic = m.group(1)
        #print("License: (" + ham_lic + ")" + "\n")

    # regex for hams license class, print to screen

    re4 = '<tr><th>Operator Class</th><td>(.*?)</td></tr>'
    rg = re.compile(re4, re.IGNORECASE | re.DOTALL)
    m = rg.search(content.decode('utf-8'))
    if m:
        ham_lic_class = m.group(1)
        #print("Class: (" + ham_lic_class + ")" + "\n")

    # regex for ham license grant date, print to screen
    re5 = '<tr><th>Granted</th><td>(.*?)</td></tr>'
    rg = re.compile(re5, re.IGNORECASE | re.DOTALL)
    m = rg.search(content.decode('utf-8'))
    if m:
        ham_lic_granted = m.group(1)
        #print("Granted: (" + ham_lic_granted + ")" + "\n")

    # regex for expiration date, print to screen
    re6 = '<tr><th>Expires</th><td>(.*?)</td></tr>'
    rg = re.compile(re6, re.IGNORECASE | re.DOTALL)
    m = rg.search(content.decode('utf-8'))
    if m:
        ham_lic_expires = m.group(1)
        #print("Expires: (" + ham_lic_expires + ")" + "\n")


    send_back = ham_name + "   " + ham_lic_class + "   " + ham_lic
    return send_back

#print(callsign_start('kr0siv'))
