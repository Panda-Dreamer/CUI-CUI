import csv
from signal import signal
import requests
import os
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import time
import wave



file = open('Birds-IDF.csv')
csvreader = csv.reader(file)

header = []
header = next(csvreader)

url  = "https://xeno-canto.org/"
parentDir = "./birds/"
n=1
segments_length = 3000

for row in csvreader:
    print('------------------------------------------------------------------------')
    print('Processing file n°{}:{}'.format(n,row[0]))
    dl = url + row[14] + "/download"
    specie = row[1]
    path = os.path.join(parentDir, specie)
    isDir = os.path.isdir(path)
    if not isDir:
        os.mkdir(path)
    
    r =requests.get(dl)
    with open('./temp/temp.mp3', 'wb') as f:
        f.write(r.content)
    sound = AudioSegment.from_mp3(r'D:\Github\CUI-CUI\temp\temp.mp3')
    sound.set_channels(1)
    segments = len(sound)//7000
    print('{} segments found'.format(segments))
    for i in range(segments):
        print('Processing segment n°{}'.format(i))
        segment = sound[i*7000:(i+1)*7000]
        
        segment.export('./temp/temp.wav', format="wav")
        spf = wave.open("./temp/temp.wav", "r")

        signalData = spf.readframes(-1)
        signalData = np.frombuffer(signalData, dtype='int16')
        left, right = signalData[0::2], signalData[1::2]

        samplingFrequency = spf.getframerate()

        plt.specgram(right, NFFT=256, Fs=samplingFrequency, noverlap=100)
        plt.axis('off')
        plt.savefig(path+'/out-'+str(i)+'-'+row[14], bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()
    n=n+1
    