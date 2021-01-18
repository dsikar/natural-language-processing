import os
import argparse
import fnmatch
import librosa
import soundfile as sf

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
    parser.add_argument('--inputs', default='../data/16k/subset/testing_data/*.wav', help='input mask to gather audio files')
    parser.add_argument('--outputs', type=str, default='../data/subset/testing_data/', help='output directory')
    args = parser.parse_args()

# 16k/subset/training_data/no
# 8k/subset/training_data/no
# 16k/subset/training_data/yes
# 8k/subset/training_data/yes
# 16k/subset/testing_data/
# 8k/subset/testing_data/

    subsample(args.inputs, args.outputs)