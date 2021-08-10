import unittest
import random
import os
import numpy as np
import shutil

import configparser
import makeDS

class testSpectro(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'configTest.cfg')
        self.dsName = self.config.get('Dataset', 'name')
        self.fftLength = int(self.config.get('Dataset', 'fftLength'))
        self.nFreq = int(self.config.get('Dataset', 'nFreq')) 
        self.numFeatures = int(self.config.get('Dataset', 'numFeatures'))
        self.numEx = int(self.config.get('Dataset', 'numEx'))

        makeDS.debugFlag = True
        makeDS.main()

    def test_dsExist(self):
        self.assertTrue(os.path.exists(self.dsName))
        self.assertTrue(os.path.exists(self.dsName + "/train/"))
        self.assertTrue(os.path.exists(self.dsName + "/test/"))

    def test_trainFilesExist(self):
        self.trainFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(self.dsName + "/train/") for name in files] 
        self.assertFalse(len(self.trainFiles) == 0)

    def test_testFilesExist(self):
        self.testFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(self.dsName + "/test/") for name in files] 
        self.assertFalse(len(self.testFiles) == 0)

    def test_correctNumOfExamples(self):
        self.testFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(self.dsName + "/test/") for name in files] 
        self.trainFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(self.dsName + "/train/") for name in files] 
        self.assertTrue(len(self.trainFiles) + len(self.testFiles) == self.numEx)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.dsName)

if __name__ == '__main__':
    unittest.main()

