#!/usr/bin/env python    
# -*- coding: utf-8 -*-

import sys
from Holiday import Edu_Student_Info

sid = sys.argv[1]
password = sys.argv[2]
api = Edu_Student_Info(sid, password)
print api.getData()