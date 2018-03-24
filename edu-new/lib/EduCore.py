#!/usr/bin/env python    
# -*- coding: utf-8 -*-

# EduCore.py
# Author:       Yang
# Data:         2016/07/20
# Description:  Get Student Info
# Input:
#         sid       Student Id Num
#         password  Password
# Output:
#         code     Status Code
#         msg      Status Message
#         Data     Student Info Data

import re
import urllib2
import urllib
import cookielib

import json

class Edu_Core(object):
    loginStatus = ''
    _sid = '0'
    _password = ''
    _checkUrl = 'http://202.197.224.171/zfca/login'
    _cookies = cookielib.CookieJar()
    _lt = ''
    _headers = ''
    _postData = ''
    _text = ''
    _name = ''
    _code = ''
    _msg = ''
    _studentData = {"status":"ok"}

    def __init__(self, sid='', password=''):
        self._sid = sid
        self._password = password
        self.checkValid()

    def setCookies(self):
        handler = urllib2.HTTPCookieProcessor(self._cookies)
        opener = urllib2.build_opener(handler, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        urllib2.urlopen(self._checkUrl)
        return 0

    def getLtKey(self):
        response = urllib2.urlopen(self._checkUrl)
        self._text = response.read().decode('gbk').encode('utf-8')
        match = re.search(r'<input\s+type="hidden"\s+name="lt"\s+value="(.*?)"\s+/>', self._text)
        self._lt = match.group(1)
        if self._lt and self._lt != '':
            return self.setMsg(3)
        return 0

    def makeHeader(self):
        self._headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.640.400 QQBrowser/9.4.8309.400',
        }
        return 0

    def makePostData(self):
        self._postData = {
            'username' : self._sid,
            'password' : self._password,
            'lt' : self._lt,
            '_eventId' : 'submit'
        }
        self._postData = urllib.urlencode(self._postData)
        return 0

    def setMsg(self, retVal):
        retValToMsg = {
            0 : u'成功',
            1 : u'密码错误',
            2 : u'超时',
            3 : u'网络故障',
            4 : u'未知错误',
            65535 : u'缺失参数'
        }
        self._code = retVal
        self._msg = retValToMsg[retVal]
        return self._code

    def checkValid(self):
        if self._sid == '' or self._password == '':
            return self.setMsg(65535)
        self.setCookies()
        self.getLtKey()
        self.makePostData()
        self.makeHeader()
        request = urllib2.Request(self._checkUrl, self._postData, self._headers)
        response = urllib2.urlopen(request)
        statusCode = urllib2.urlopen(self._checkUrl).getcode()
        self._text = response.read().decode('gbk').encode('utf-8')
        if statusCode != 200:
            return self.setMsg(3)
        if self.checkIfError() != 0:
            return 0
        if self.getName() != 0:
            return 0

    def checkIfError(self):
        if re.search(r'用户名或密码错误', self._text):
            return self.setMsg(1)
        elif re.search(r'超时', self._text):
            return self.setMsg(2)
        elif re.search(r'校历', self._text):
            return 0
        else:
            self.setMsg(4)

    def getName(self):
        match = re.search(r'CurrentUserName\s+=\s+\'(.*?)\';', self._text)
        if match.group(1) and match.group(1) != '':
            self._name = match.group(1)
            self.loginStatus = 1
            return self.setMsg(0)
        return self.setMsg(3)

 
    def getData(self):
        jsonArray = {
            'code' : self._code,
            'msg' : self._msg,
            'data' : self._studentData
        }
        jsonData = json.dumps(jsonArray)
        return jsonData
