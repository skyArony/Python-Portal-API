#!/usr/bin/env python    
# -*- coding: utf-8 -*-

import sys
from EduStudentInfoAll import Edu_Student_Info_All

sid = sys.argv[1]
password = sys.argv[2]
api = Edu_Student_Info_All(sid, password)
print api.getData()