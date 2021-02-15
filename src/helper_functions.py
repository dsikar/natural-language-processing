import os
import argparse
import fnmatch
import librosa
import soundfile as sf
import random

random.choice([1,2,3,4,5,6,7,8,9,10])

def get_random_files(filemask, s=False):
    '''
    Use a filemask and search a path recursively for matches, generating a cp command to be executed by script
    Inputs
        filemask: string passed as command line option, must not be enclosed in quotes
        s: boolean, sort by create date flag
    Returns
        none

    '''
    filemask = os.path.expanduser(filemask)
    path, mask = os.path.split(filemask)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, mask):
            matches.append(os.path.join(root, filename))
    if (s == True):
        matches = sorted(matches, key=os.path.getmtime)
    # return matches

    for file in matches:
        # copy one in ten
        if(random.choice([1,2,3,4,5,6,7,8,9,10]) == 1):
            cpfile = file.split('/')
            mystr = "cp {} ../dataset/testing/no/{}".format(file, cpfile[-1])
            print(mystr)
            #print(print("cp {} ../dataset/training/yes/{}".format(file, cpfile[-1])))


def get_files(filemask, s=False):
    '''
    Use a filemask and search a path recursively for matches
    Inputs
        filemask: string passed as command line option, must not be enclosed in quotes
        s: boolean, sort by create date flag
    '''

    filemask = os.path.expanduser(filemask)
    path, mask = os.path.split(filemask)

    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, mask):
            matches.append(os.path.join(root, filename))
    if (s == True):
        matches = sorted(matches, key=os.path.getmtime)
    return matches

def subsample(inputs, outputs):
    """
    Subsample audio files and save
    Inputs
        inputs: string, path to 16k files
        outputs: string, path to 8k outputs
    Example:
        subsample('16k/subset/training_data/no', '8k/subset/training_data/no')
    """
    # low sample rate
    lowSR = 8000
    files = get_files(inputs)
    for file in files:
        samples, sample_rate = librosa.load(file)
        lowSample = librosa.resample(samples, sample_rate, lowSR)
        filename = file.split('/')
        filename = filename[-1]
        filename = outputs + filename
        try:
            sf.write(filename, lowSample, lowSR)
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Audio pre-processing functions')
    #parser.add_argument('--inputs', default='../data/16k/subset/training_data/yes/*.wav', help='input mask to gather audio files')
    #parser.add_argument('--outputs', type=str, default='../data/8k/subset/training_data/yes/', help='output directory')
    parser.add_argument('--inputs', default='../data/8k/input/training_data/no/*.wav', help='input mask to gather audio files')
    parser.add_argument('--outputs', type=str, default='../data/subset/testing_data/', help='output directory')
    args = parser.parse_args()

# 16k/subset/training_data/no
# 8k/subset/training_data/no
# 16k/subset/training_data/yes
# 8k/subset/training_data/yes
# 16k/subset/testing_data/
# 8k/subset/testing_data/

    # subsample(args.inputs, args.outputs)
    # 1. copy from  '../data/8k/input/training_data/yes/*.wav' to ../dataset/training/yes/
    # 2. copy from  '../data/8k/input/training_data/no/*.wav' to ../dataset/training/no/
    # 3. copy from  '../data/8k/input/training_data/yes/*.wav' to ../dataset/testing/yes/
    # 4. copy from  '../data/8k/input/training_data/no/*.wav' to ../dataset/testing/no/
    get_random_files(args.inputs)