#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 23:49:52 2021

@author: m31781
"""
import numpy as np

#final score
bil = 27
col = 24
ram = 30
sea = 20
buc = 31
wft = 23
rav = 20
tit = 13
bea = 9
sai = 21
bro = 48
pit = 37

#pred score
fbil = 30
fcol = 26
fram = 23
fsea = 26
fbuc = 29
fwft = 22
frav = 28
ftit = 25
fbea = 24
fsai = 28
fbro = 25
fpit = 29

#scoring
scores = np.array([bil, col, ram, sea, buc, wft, rav, tit, bea, sai, bro, pit])
pred = np.array([fbil, fcol, fram, fsea, fbuc, fwft, frav, ftit, fbea, fsai, fbro, fpit])

dif = abs(scores - pred)

print(dif.mean())
