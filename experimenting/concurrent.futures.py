# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 18:29:54 2022

@author: Joe
"""

import concurrent.futures
import time
def foo(bar):
    print('hello {}'.format(bar))
    time.sleep(1)
    #return 'foo'
    
def bar(bar):
    print('hello {}'.format(bar))
    time.sleep(2)
    #return 'foo'

while True:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(foo, 'world!')
        #return_value = future.result()
        #print(return_value)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(bar, '2!')  
    