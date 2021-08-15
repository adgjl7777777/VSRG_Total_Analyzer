# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 07:53:43 2021

@author: Transcendence
"""
import numpy as np

def findkey(x = 0): #그 시간대에 어떤 키를 눌렀나 보는 함수
    keyset = [0 for i in range(18)]
    (a, keyset[0]) = (x//2, x%2)
    j = 1
    while a != 0:
        (a, keyset[j]) = (a//2, a%2)
        j += 1
    return np.array(keyset)