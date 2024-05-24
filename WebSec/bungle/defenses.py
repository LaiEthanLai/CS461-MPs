import re, os
from bottle import FormsDict, HTTPError
from hashlib import md5
from random import random

############################################################
# XSS Defenses

class XSSNone(object):
    name = "No defense"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        return input

class XSSRemoveScript(object):
    name = "Remove &quot;script&quot;"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        return re.sub(r"(?i)script", "", input)

# Added in FA15
class XSSRecRemoveScript(object):
    name = "Recursively remove &quot;script&quot;"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        original = input
        filtered = re.sub(r"(?i)script", "", input)
        while original != filtered:
            original = filtered
            filtered = re.sub(r"(?i)script", "", original)
        return filtered

class XSSRemovePunctuation(object):
    name = "Remove &quot; &apos; and ;"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        return re.sub(r"[;'\"]", "", input)

class XSSRemoveSeveralTags(object):
    name = "Remove several tags"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        return re.sub(r"(?i)script|<img|<image|<body|<style|<meta|<embed|<object", "", input)

# Added in FA15
class XSSRecRemoveSeveralTags(object):
    name = "Recursively remove several tags"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        original = input
        filtered = re.sub(r"(?i)script|<img|<image|<body|<style|<meta|<embed|<object", "", input)
        while original != filtered:
            original = filtered
            filtered = re.sub(r"(?i)script|<img|<image|<body|<style|<meta|<embed|<object", "", original)
        return filtered

class XSSBrowser(object):
    name = "Browser&rsquo;s XSS Protection"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "1")
    @staticmethod
    def filter(input):
        return input

class XSSEncodeAngles(object):
    name = "Encode &lt; and &gt;"
    @staticmethod
    def init(response):
        response.set_header("X-XSS-Protection", "0")
    @staticmethod
    def filter(input):
        # TODO
        
        if input is not None:
            input = input.replace('>', '&gt')
            input = input.replace('<', '&lt')
        
        return input

############################################################
# CSRF Defenses

class CSRFNone(object):
    name = "No defense"
    @staticmethod
    def init(request, response):
        return None
    @staticmethod
    def formHTML(token):
        return ""
    @staticmethod
    def validate(request, token):
        pass

class CSRFToken(object):
    name = "Token validation"
    @staticmethod
    def init(request, response):
        token = request.get_cookie("csrf_token")
        # TODO
        if token is None:
            token = ''
            for i in range(32):
                out = int(random() * 15)
                token += str(hex(out))[2]
        
        response.set_cookie("csrf_token", token)

        return token
    @staticmethod
    def formHTML(token):
        return "<input type='hidden' name='csrf_token' value='" + token + "'>"
    @staticmethod
    def validate(request, token):
        if request.forms.get('csrf_token') != token:
            # raise HTTPError(403, output="CSRF Attack Detected (bad or missing token)")
            raise HTTPError(403, body="CSRF Attack Detected (bad or missing token)")

class CSRFReferer(object):
    name = "Referer validation"
    @staticmethod
    def init(request, response):
        return None
    @staticmethod
    def formHTML(token):
        return ""
    @staticmethod
    def validate(request, token):
        referer = request.get_header("referer", "")
        if referer != "" and referer.find("http://permalink.co/") != 0:
            raise HTTPError(403, output="CSRF Attack Detected (bad referer)")

############################################################

xssDefenses = [XSSNone, XSSRemoveScript, XSSRecRemoveScript, XSSRecRemoveSeveralTags, XSSRemovePunctuation, XSSEncodeAngles]
csrfDefenses = [CSRFNone, CSRFToken]

xssDefense = xssDefenses[0]
csrfDefense = csrfDefenses[0]

def setCookies(response):
    response.set_cookie("xssdefense", str(xssDefenses.index(xssDefense)))
    response.set_cookie("csrfdefense", str(csrfDefenses.index(csrfDefense)))

def setup(request, response):
    def getDefense(request, name):
        if name in request.forms:
            return int(request.forms.get(name))
        elif name in request.query:
            return int(request.query.get(name))
        else:
            return int(request.get_cookie(name,0))
    global xssDefense, csrfDefense
    xss = getDefense(request, "xssdefense")
    if xss not in range(len(xssDefenses)):
        raise HTTPError(output="Invalid XSS Defense (%d)" % xss)
    csrf = getDefense(request, "csrfdefense")
    if csrf not in range(len(csrfDefenses)):
        raise HTTPError(output="Invalid CSRF Defense (%d)" % csrf)
    xssDefense = xssDefenses[xss]
    csrfDefense = csrfDefenses[csrf]
    setCookies(response)

def selectors():
    def getSelector(defenseList, selectedDefense=None):
        return "".join("<option value=%d%s>%d - %s</option>" % (i,(defenseList[i].name == selectedDefense.name and " selected" or ""), i, defenseList[i].name) for i in range(len(defenseList)))
    return FormsDict(xssoptions=getSelector(xssDefenses,xssDefense), csrfoptions = getSelector(csrfDefenses,csrfDefense))
