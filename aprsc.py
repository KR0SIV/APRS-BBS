#including current copy of my aprscrafting library to ensure I don't break this down the road
import zulu
import re
import time


class aprscrafter:

    def parsemsg(self, rawmsg):  # PARSE Doesn't Understand Non-Message Types or Messages that include location data
        msg = rawmsg.decode("utf-8")
        sendingcall = re.findall("\A(.*)(?:>)", msg)[0]
        tocall = re.findall("(?:::)(.*)(?::)", msg)[0].strip()
        fullmessage = re.findall("(?:::)(?:.{10})(.*)", msg)[
            0]  # captures full message including ack string which must be handled.

        if "{" in fullmessage:
            msg = re.findall("(.*)(?:{)", fullmessage)[0]
            msgID = re.findall("(?:{)(.*)", fullmessage)[0]
            rxack = ""
            # print("msgID: " + msgID)
        elif "ack" in fullmessage:
            rxack = fullmessage
            msgID = ""
            # print("rxack: " + rxack)
        else:
            msg = fullmessage
            msgID = ""
            rxack = ""

        array = (sendingcall + "," + tocall + "," + msg + "," + msgID + "," + rxack).split(
            ",")  # Creates an array starting at 0 containing all components of a message
        return array

    def padCall(self, callsign):    #Pads a callsign to 9 spaces, truncates if longer. APRS101 Chapter 14 Messages
        padded = callsign.ljust(9)
        if len(padded) > 9:
            return padded[:9]
        else:
            return padded

    def truncMsg(self, msg):   #Truncates messages to 67 characters. APRS101 Page 71
        return msg[:67]

    def msg(self, fromcall, tocall, message, *ack): #Creates a message packet following APRS101 Page 71
        if str(ack) == '()':
            ack = ''
        else:
            ack = '{' + str(ack[0])
        return fromcall.upper() + '>APRS' + '::' + self.padCall(tocall.upper()) + ':' + self.truncMsg(message) + ack[:6]

    def bln(self, fromcall, blnID, *groupID, msg, announce=False):    #Creates bulletin packet with optional groupID and annoucement flag. APRS101 Page 73
        if not announce:
            pass
        if announce:
            blnID = 'X'
        else:
            pass
        if str(groupID) == '()':
            groupID = '     '
        else:
            groupID = str(groupID[0])

        return fromcall.upper() + '>APRS' + '::' + 'BLN' + blnID[:1] + groupID[:5] +':' + self.truncMsg(msg)

    def status(self, fromcall, statustext, timestamp=False):    #APRS101 Page 80 Status Reports; only basic at this time
        if not timestamp:
            statustext = statustext[:62]
            return fromcall.upper() + '>APRS:>' + statustext
        if timestamp:
            statustext = statustext[:55]
            dt = zulu.parse(zulu.now())
            zt = re.findall("\d{6}", str(dt))
            return fromcall.upper() + '>APRS:>' + zt[0] + 'z' + statustext

    class parser:
        def sendcall(self, rawmsg):
            msg = rawmsg.decode("utf-8")
            return re.findall("\A(.*)(?:>)", msg)[0]

        def fromcall(self, rawmsg):
            msg = rawmsg.decode("utf-8")
            return re.findall("(?:::)(.*)(?::)", msg)[0].strip()


        def message(self, rawmsg):
            msg = rawmsg.decode("utf-8")
            fullmessage = re.findall("(?:::)(?:.{10})(.*)", msg)[0]
            if "ack" in fullmessage:
                return ""
            elif "{" in fullmessage:
                return re.findall("(.*)(?:{)", fullmessage)[0]
            return ""

        def rxack(self, rawmsg):
            pass

        def ack(self, rawmsg):
            pass

aprsc = aprscrafter()
