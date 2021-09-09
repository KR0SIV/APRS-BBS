#PersonalAPRSServer

import aprslib
from random import randint
from datetime import datetime
startTime = datetime.now()
from hamcall import callsign_start as callinfo
from aprsc import aprscrafter
aprsc = aprscrafter()

import requests
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

mycall = config['user']['mycall']
myphone = config['user']['myphone']
mysmskey = config['user']['mysmskey']


menuenabled = config['features']['menu']
menutext = config['features']['menutext']
aboutenabled = config['features']['about']
abouttext = config['features']['abouttext']
uptimeenabled = config['features']['uptime']
callenabled = config['features']['call']


def app():
    try:
        AIS = aprslib.IS(mycall, aprslib.passcode(mycall), port=14580)
        AIS.connect()
        AIS.sendall(aprsc.status(mycall, 'Starting Personal Mailbox APRS Service - Beta '))

        def callback(packet):
            parsed = aprsc.parsemsg(packet)##Parsed array is fromcall, tocall, message, ack, timestamp or location
            print(packet)
            print(parsed)
            rxcall = parsed[0]
            rxmsg = parsed[2]
            rxack = parsed[3]
        ##HANDLES ACK
            ack = '{' + str(randint(1,999))

            if 'TCP' in rxack:##If TCP* in ACK field we ignore and dont send an ack response
                pass
            else:
                AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message='ack' + rxack))###Send ACK
        ##END ACK HANDLING
                rxmsg = str(rxmsg).lower()
            if 'menu' in rxmsg and menuenabled == 'on':
                AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message=menutext + ack))
            if 'about' in rxmsg and aboutenabled == 'on':
                AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message=abouttext + ack))
            if 'uptime' in rxmsg and uptimeenabled == 'on':
                AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message=str(datetime.now() - startTime) + ack))
            if 'call' in rxmsg and callenabled == 'on':
                try:
                    callreq = rxmsg.split( )[1]
                    AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message=callinfo(callreq) + ack))
                except:
                    AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message='MSG Format: CALL callsign' + ack))#if all else fails, send ack lol
            if 'sms' in rxmsg:
                try:
                    smsmsg = rxmsg
                    resp = requests.post('https://textbelt.com/text', {
                        'phone': myphone,
                        'message': rxcall + ' ' + smsmsg,
                        'key': mysmskey,
                    })
                    print(resp.json())
                    AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message='Sending your message to ' + mycall + ack))
                except:
                    AIS.sendall(aprsc.msg(fromcall=mycall, tocall=rxcall, message='MSG Format: SMS your_message_here' + ack))#if all else fails, send ack lol


        AIS.consumer(callback, raw=True)
    except:
        app()

app()
