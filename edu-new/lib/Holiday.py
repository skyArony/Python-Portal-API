#!/usr/bin/env python    
# -*- coding: utf-8 -*-

# Holiday.py
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

#2015-2016 2015为pre 2016为next 2017位nnext

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
            self.getHolidayInfo()

    def getHolidayInfo(self):
        posturl = 'http://202.197.224.171/dwr/call/plaincall/xlAjax.getCurrentXnxqList.dwr'
        #构造post数据
        postData = {
            'callCount' : 1,
            'page' : '/xiaoli.html',
            'httpSessionId':'276421AE18B011F4C391CBFAFC2986E1',
            'scriptSessionId':'16D8E756C167473679D300CFD091DAAB30',
            'c0-scriptName':'xlAjax',
            'c0-methodName':'getCurrentXnxqList',
            'c0-id':0,
            'batchId':0
        }
        #编码post数据
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, self._headers)
        response = urllib2.urlopen(request)
        json = response.read()

        match = re.search(r's\d{1,2}\.fjrq="(.*?)";s\d{1,2}\.jqmc="\\u5BD2\\u5047";s\d{1,2}\.kxrq="(.*?)";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xq="\\u4E00"', json)     #2016上学年
        upYearStart = match.group(2)
        upYearEnd = match.group(1)
        upYearStart += u' 至 '
        upYearStart += upYearEnd
        self._studentData["upYear_next"] = upYearStart

        match = re.search(r's\d{1,2}\.fjrq="(.*?)";s\d{1,2}\.jqmc="\\u6691\\u5047";s\d{1,2}\.kxrq="(.*?)";s\d{1,2}\.xn="(.*?)-(.*?)";s\d{1,2}\.xq="\\u4E8C"', json)     #2016下学年
        downYearStart = match.group(2)
        downYearEnd = match.group(1)
        downYearStart += u' 至 '
        downYearStart += downYearEnd
        self._studentData["downYear_next"] = downYearStart
        sjStart_2016 = downYearEnd   #获取2016暑假的开始日期
        pre_year = match.group(3)      #获取开始念
        next_year = match.group(4)      #获取结束年

        match = re.search(r's\d{1,2}\.xn="(.*?)"', json)
        self._studentData["range"] = match.group(1)

        posturl = 'http://202.197.224.171/dwr/call/plaincall/xlAjax.getNextXnkxrq.dwr'
        #构造post数据
        postData = {
            'callCount' : 1,
            'page' : '/xiaoli.html',
            'httpSessionId':'276421AE18B011F4C391CBFAFC2986E1',
            'scriptSessionId':'16D8E756C167473679D300CFD091DAAB30',
            'c0-scriptName':'xlAjax',
            'c0-methodName':'getNextXnkxrq',
            'c0-id':0,
            'batchId':4
        }
        #编码post数据
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, self._headers)
        response = urllib2.urlopen(request)
        json = response.read()

        match = re.search(r'kxrq:"(.*?)"', json)   #2017上学年
        upYearStart = match.group(1)
        sjEnd_2016 = upYearStart    #获取2016暑假结束日期
        match = re.search(r'fjrq:"(.*?)"', json)
        upYearEnd = match.group(1)
        upYearStart += u' 至 '
        upYearStart += upYearEnd
        self._studentData["upYear_nnext"] = upYearStart

        sjStart_2016 += u' 至 '      #2016暑假
        sjStart_2016 += sjEnd_2016
        self._studentData["sj_next"] = sjStart_2016

        posturl = 'http://202.197.224.171/dwr/call/plaincall/xlAjax.getXlrqListByDate.dwr'
        #构造post数据
        postData = {
            'callCount' : 1,
            'page' : '/xiaoli.html',
            'httpSessionId':'276421AE18B011F4C391CBFAFC2986E1',
            'scriptSessionId':'16D8E756C167473679D300CFD091DAAB30',
            'c0-scriptName':'xlAjax',
            'c0-methodName':'getXlrqListByDate',
            'c0-id':0,
            'c0-param0':'string:' + pre_year + '-09-01',
            'c0-param1':'string:' + next_year + '-01-31',
            'batchId':1
        }
        #编码post数据
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, self._headers)
        response = urllib2.urlopen(request)
        json = response.read()

        match = re.search(r's\d{1,2}\.bt="\d{1,4}\\u5BD2\\u5047";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="0";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u5BD2\\u5047"', json)   #2016寒假
        hjStart = match.group(2)
        hjEnd = match.group(1)
        hjStart += u' 至 '
        hjStart += hjEnd
        self._studentData["hj_next"] = hjStart

        match = re.search(r's\d{1,2}\.bt="\\u6691\\u5047";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="0";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u6691\\u5047"', json)   #2015暑假
        sjStart = match.group(2)
        sjEnd = match.group(1)
        sjStart += u' 至 '
        sjStart += sjEnd
        self._studentData["sj_pre"] = sjStart

        match = re.search(r's\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u5143\\u65E6"', json)   #2016元旦    、、、、、
        ydStart = match.group(2)
        ydEnd = match.group(1)
        ydStart += u' 至 '
        ydStart += ydEnd
        self._studentData["yd_next"] = ydStart

        match = re.search(r's\d{1,2}\.bt="\\u56FD\\u5E86\\u8282";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u56FD\\u5E86\\u8282"', json)   #2015国庆    、、、、、
        gqStart = match.group(2)
        gqEnd = match.group(1)
        gqStart += u' 至 '
        gqStart += gqEnd
        self._studentData["gq_pre"] = gqStart

        match = re.search(r's\d{1,2}\.bt="\\u4E2D\\u79CB\\u8282";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u4E2D\\u79CB\\u8282"', json)   #2015中秋    、、、、、
        zqStart = match.group(2)
        zqEnd = match.group(1)
        zqStart += u' 至 '
        zqStart += zqEnd
        self._studentData["zq_pre"] = zqStart

        posturl = 'http://202.197.224.171/dwr/call/plaincall/xlAjax.getXlrqListByXn.dwr'
        #构造post数据
        postData = {
            'callCount' : 1,
            'page' : '/xiaoli.html',
            'httpSessionId':'276421AE18B011F4C391CBFAFC2986E1',
            'scriptSessionId':'16D8E756C167473679D300CFD091DAAB30',
            'c0-scriptName':'xlAjax',
            'c0-methodName':'getXlrqListByXn',
            'c0-id':0,
            'c0-param0':'string:2015-2016',
            'batchId':3
        }
        #编码post数据
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, self._headers)
        response = urllib2.urlopen(request)
        json = response.read()

        match = re.search(r's\d{1,2}\.bt="\d{1,4}\\u56FD\\u5E86\\u8282";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u56FD\\u5E86\\u8282"', json)   #2016国庆节    、、、、、
        gqStart = match.group(2)
        gqEnd = match.group(1)
        gqStart += u' 至 '
        gqStart += gqEnd
        self._studentData["gq_next"] = gqStart

        match = re.search(r's\d{1,2}\.bt="\d{1,4}\\u4E2D\\u79CB\\u8282";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u4E2D\\u79CB\\u8282"', json)   #2016中秋节    、、、、、
        zqStart = match.group(2)
        zqEnd = match.group(1)
        zqStart += u' 至 '
        zqStart += zqEnd
        self._studentData["zq_next"] = zqStart

        match = re.search(r's\d{1,2}\.bt="\d{1,4}\\u7AEF\\u5348\\u8282";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u7AEF\\u5348\\u8282"', json)   #2016端午节    、、、、、
        dwStart = match.group(2)
        dwEnd = match.group(1)
        dwStart += u' 至 '
        dwStart += dwEnd
        self._studentData["dw_next"] = dwStart

        match = re.search(r's\d{1,2}\.bt="\d{1,4}\\u52B3\\u52A8\\u8282";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u52B3\\u52A8\\u8282"', json)   #2016端午节    、、、、、
        ldStart = match.group(2)
        ldEnd = match.group(1)
        ldStart += u' 至 '
        ldStart += ldEnd
        self._studentData["ld_next"] = ldStart

        match = re.search(r's\d{1,2}\.bt="\d{1,4}\\u6E05\\u660E";s\d{1,2}\.jssj="(.*?)";s\d{1,2}\.kssj="(.*?)";s\d{1,2}\.lb="1";s\d{1,2}\.xn="(.*?)";s\d{1,2}\.xsmc="\\u6E05\\u660E\\u8282"', json)   #2016清明节    、、、、、
        qmStart = match.group(2)
        qmEnd = match.group(1)
        qmStart += u' 至 '
        qmStart += qmEnd
        self._studentData["qm_next"] = qmStart