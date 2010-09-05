#!/usr/bin/env python
# coding: utf-8

import unittest
from datetime import datetime, timedelta

from togrog import settings

settings.APP_NAME = 'testapp'

from togrog.manager import Manager
from togrog.model import Model

class ManagerTest(unittest.TestCase):
    
    def testManager(self):
        class TM(object):
            x = Manager()
            
        tm = TM()
        
        assert(tm.x.model == tm.__class__)
            
    def testModelManager(self):
            
        m = Model()
        
        assert(m.objects.model == m.__class__)
            
    def testSubclassModelManager(self):
            
        class SM(Model):
            pass
            
        sm = SM()
        
        assert(sm.objects.model == sm.__class__)
            
            
    def testManagerNew(self):
        class TModel(Model):
            pass
            
        tmod = TModel.objects.new()
        
        nowish = datetime.utcnow()
        thenish = nowish - timedelta(seconds=1)
        
        assert(thenish < tmod.fields['created'].value < nowish)
        assert(thenish < tmod.created < nowish)
        
        tmod.created = nowish
        assert(tmod.fields['created'].value == nowish)
        assert(thenish < tmod.created == nowish)
        
    def testModelSave(self):
        class TModel(Model):
            pass
            
        tmod = TModel.objects.create()
                
        tmod1 = TModel.objects.get(tmod._id)
                
        self.assertEqual(tmod.created, tmod1.created)
        
            

if __name__ == '__main__':
    unittest.main()
    
#end
