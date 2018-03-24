#!/usr/bin/env python    
# -*- coding: utf-8 -*-

# EduStudentInfo.py
# Author:       Yang
# Data:         2016/07/21
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

import EduCore

class Edu_Student_Info(EduCore.Edu_Core):
    def __init__(self, sid = '', password = ''):
        self._sid = sid
        self._password = password
        self.checkValid();
        if self.loginStatus == 1:
            self.getStudentInfo()

    def getStudentInfo(self):
        posturl = 'http://202.197.224.171/zfca/login'
        #构造post数据
        postData = {
            'yhlx' : 'student',
            'login' : '122579031373493679',
            'url' : 'stuPage.jsp'
        }
        #编码post数据
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, self._headers)
        response = urllib2.urlopen(request)

        #构造post数据3
        postData = {
            'xh' : '2015551509'
        }
        posturl = 'http://202.197.224.175/xgxt/xsxx_xsxxgl.do?method=xsxxglCk&type=query'
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, self._headers)
        response = urllib2.urlopen(request)

        json = response.read().decode('gbk').encode('utf-8')
        json = json.replace('null', '"null"')  #处理json中的null
        match = re.search(r'"xm":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["name"] = match.group(1)
        match = re.search(r'"xb":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["sex"] = match.group(1)
        match = re.search(r'"csrq":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["date_of_birth"] = match.group(1)
        match = re.search(r'"xymc":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["college"] = match.group(1)
        match = re.search(r'"zymc":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["major"] = match.group(1)
        match = re.search(r'"bjmc":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["class"] = match.group(1)
        else:
            self._studentData["nation"] = u'没有数据'
        match = re.search(r'"bzrList":(.*?):"null","zgh":"(.*?)","xm":"(.*?)"', json)
        if match.group(3) != 'null' and match.group(3) != '':
            self._studentData["classmaster"] = match.group(3)
        match = re.search(r'"mzmc":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            self._studentData["nation"] = match.group(1)
        match = re.search(r'"sfzh":"(.*?)"', json)
        if match.group(1) != 'null' and match.group(1) != '':
            num = match.group(1)[0:2]
            if num == '11':
                self._studentData["location"] = u"北京市"
            elif num == '12':
                self._studentData["location"] = u"天津市"
            elif num == '13':
                self._studentData["location"] = u"河北省 "
            elif num == '14':
                self._studentData["location"] = u"山西省"
            elif num == '15':
                self._studentData["location"] = u"内蒙古自治区"
            elif num == '21':
                self._studentData["location"] = u"辽宁省"
            elif num == '22':
                self._studentData["location"] = u"吉林省"
            elif num == '23':
                self._studentData["location"] = u"黑龙江省"
            elif num == '31':
                self._studentData["location"] = u"上海市"
            elif num == '32':
                self._studentData["location"] = u"江苏省"
            elif num == '33':
                self._studentData["location"] = u"浙江省"
            elif num == '34':
                self._studentData["location"] = u"安徽省"
            elif num == '35':
                self._studentData["location"] = u"福建省"
            elif num == '36':
                self._studentData["location"] = u"江西省"
            elif num == '37':
                self._studentData["location"] = u"山东省"
            elif num == '41':
                self._studentData["location"] = u"河南省"
            elif num == '42':
                self._studentData["location"] = u"湖北省"
            elif num == '43':
                self._studentData["location"] = u"湖南省"
            elif num == '44':
                self._studentData["location"] = u"广东省"
            elif num == '45':
                self._studentData["location"] = u"广西壮族自治区"
            elif num == '46':
                self._studentData["location"] = u"海南省"
            elif num == '50':
                self._studentData["location"] = u"重庆市"
            elif num == '51':
                self._studentData["location"] = u"四川省 "
            elif num == '52':
                self._studentData["location"] = u"贵州省"
            elif num == '53':
                self._studentData["location"] = u"云南省"
            elif num == '54':
                self._studentData["location"] = u"西藏自治区"
            elif num == '61':
                self._studentData["location"] = u"陕西省"
            elif num == '62':
                self._studentData["location"] = u"甘肃省"
            elif num == '63':
                self._studentData["location"] = u"青海省"
            elif num == '64':
                self._studentData["location"] = u"宁夏回族自治区"
            elif num == '65':
                self._studentData["location"] = u"新疆维吾尔自治区"
            elif num == '71':
                self._studentData["location"] = u"台湾省"
            elif num == '81':
                self._studentData["location"] = u"香港特别行政区"
            elif num == '91':
                self._studentData["location"] = u"澳门特别行政区"
            else:
                self._studentData["location"] = u"没有数据"
        else:
            self._studentData["location"] = u"没有数据"
            self._studentData["id"] = u"没有数据"
            