# -*- coding: utf-8 -*- 
'''
@author:       cherry
@license:      GNU General Public License 2.0 or later
@contact:      chery.wb@gmail.com
'''
import sys, os, random

class Stack: 
    """模拟栈""" 
    def __init__(self): 
        self.items = [] 
         
    def isEmpty(self): 
        return len(self.items)==0  
     
    def push(self, item): 
        self.items.append(item) 
     
    def pop(self): 
        return self.items.pop()  
     
    def peek(self,index): 
        if not self.isEmpty(): 
            return self.items[len(self.items)-index] 
         
    def size(self): 
        return len(self.items)  