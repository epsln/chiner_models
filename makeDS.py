#Create a dataset of normalised spectrograms from files
import os
import numpy as np
import librosa
import random
import audiofile as af

import configparser

from utils.audioTools import getSpectro

debugFlag = False 


def main():
    config = configparser.ConfigParser()
    if debugFlag == True:
        config.read(r'configTest.cfg')
    else:
        config.read(r'config.cfg')

    dsName = config.get('Dataset', 'name')
    fftLength = int(config.get('Dataset', 'fftLength'))
    nFreq = int(config.get('Dataset', 'nFreq')) 
    numFeatures = int(config.get('Dataset', 'numFeatures'))
    numEx = int(config.get('Dataset', 'numEx'))
    musicFilesDir = config.get('Dataset', 'musicFilesDir')

    #Might want to expand this somewhat
    acceptableFormats = [".wav", ".flac", ".mp3"]

    #Might want to rename data to fit whatever user might want
    musicFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(os.path.expanduser(musicFilesDir)) for name in files] 
    random.shuffle(musicFiles)

    #Remove the undesirables formats
    for music in musicFiles:
        if os.path.splitext(music)[1] not in acceptableFormats:
            musicFiles.remove(music)
 #   for path, subdirs, files in os.walk(musicFilesDir):
 #       for name in files:
 #           print(os.path.join(path, name))
 #           musicFiles.append(os.path.join(path, name))
    if len(musicFiles) == 0:
        raise ValueError("No music file detected...")

            
    #If folder already exist, quit
    if os.path.exists(dsName):
        #TODO: Raise an actual (appropriate) error
        print("ERROR:  The folder '" + dsName + "' already exists ! either delete it or rename it and try again")
        #return -1

    else:
        #Else create folder 
        os.makedirs(dsName)
        os.makedirs(dsName + "/train")
        os.makedirs(dsName + "/test/")
         
    #Finally create the dataset 
    for i in range(numEx):
        song = musicFiles[i]
        S = getSpectro(song, fftLength)
        if np.random.uniform(0, 1) > 0.8:
            print("Saving " + dsName + "/test/"+os.path.basename(song)[:-4]+".npy")
            print("[",i + 1,"/", numEx, "]")
            np.save(dsName + "/test/"+os.path.basename(song)[:-4]+".npy", S)
        else:
            print("Saving " + dsName + "/train/"+os.path.basename(song)[:-4]+".npy")
            print("[",i + 1,"/", numEx, "]")
            np.save(dsName + "/train/"+os.path.basename(song)[:-4]+".npy", S)

if __name__ == "__main__":
    main()
