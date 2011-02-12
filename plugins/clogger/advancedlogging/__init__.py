# -*- coding: utf-8 -*-
""" This is the advanced logging main file, which contains the basic classes, developed originally from Hoborg and inspired by Clark-Kent, #archlinux-il offical bot """
__all__ = [
           'BasicMessagesLogger',
           'htmllogger'
           ]
__version__ = '0.1'
from lxml import etree
from time import localtime, strftime
import os
class BasicMessagesLogger:
    """ The basic logger, useful if you would like to use Hoborg as a log bot and you like text logs """
    def __init__(self,logdir,autolog=False):
        self.logdir = logdir
        self.logging = autolog
    def LogMessage(self,sender,msg):
        if self.logging and sender != 'NickServ':
            self.d = strftime("%d",localtime())
            self.m = strftime("%m",localtime())
            self.y = strftime("%Y",localtime())
            self.h = strftime("%H:%M:%S",localtime())
            if os.path.exists(self.logdir+self.y+'/'+self.m+'/'+self.d+'.log') or os.path.isdir(self.logdir+self.y+self.m):
                self.logf = open(self.logdir+self.y+'/'+self.m+'/'+self.d+'.log','ab')
            elif os.path.isdir(self.logdir+self.y):
                os.mkdir(self.logdir+self.y+'/'+self.m)
                self.logf = open(self.logdir+self.y+'/'+self.m+'/'+self.d+'.log','ab')
            elif os.path.isdir(self.logdir):
                os.mkdir(self.logdir+self.y)
                os.mkdir(self.logdir+self.y+'/'+self.m)
                self.logf = open(self.logdir+self.y+'/'+self.m+'/'+self.d+'.log','ab')
            else:
                os.mkdir(self.logdir)
                os.mkdir(self.logdir+self.y)
                os.mkdir(self.logdir+self.y+'/'+self.m)
                self.logf = open(self.logdir+self.y+'/'+self.m+'/'+self.d+'.log','ab')
            self.logf.write('(%s) <%s> %s\n' % (self.h,sender,msg))
            self.logf.flush()
    def Run(self):
        self.logging = True
    def Stop(self):
        self.logging = False