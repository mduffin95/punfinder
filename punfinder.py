#!/bin/python
import nltk
import string
import pickle
from collections import defaultdict
from Levenshtein import distance

def getPhonemes(queryword, entries):
    try:
        return entries[queryword]
    except KeyError:
        return None;

#a and b are lists of phonemes
def rhyme(a, b, level):
    asyl = nsyl(a)
    bsyl = nsyl(b)
    syl = min(level, asyl, bsyl)
    length = min(len(a), len(b))
    count = 0
    for i in range(length):
        if a[i] != b[i]:
            break
        if a[i][-1].isdigit():
            count += 1
        if count == syl and (i > 1 or i == (length-1)):
            return True

    count = 0
    for i in range(-1, -(length+1), -1):
        if a[i] != b[i]:
            break
        if a[i][-1].isdigit():
            count += 1
        if count == syl and (i < -2 or i == -length):
            return True
    return False


def nsyl(phonemes):
    count = 0
    for x in phonemes:
        if x[-1].isdigit():
            count += 1
    return count

if __name__ == "__main__":
        
    entries = nltk.corpus.cmudict.dict()
    movie_syllables = defaultdict(list)
    fish_syllables = defaultdict(list)
    movie_words = defaultdict(list) 
    movie_file = "movie_syllables.pickle"
    movie_words_file = "movie_words.pickle"
    fish_file = "fish_syllables.pickle"

    fish_source = "fish.txt"
    movies_source = "movies.txt"

    try:
        movie_words = pickle.load( open(movie_words_file, "rb"))
    except (OSError, IOError) as e:
        with open(movies_source, "r") as f:
            for line in f:
                movie = line.split('\t', 1)[1]
                for s in movie.split():
                    s = s.translate(string.punctuation).lower()
                    s = s.replace(':', '')
                    if len(s) > 2:
                        movie_words[s].append(movie)
                        print(s)

        with open(movie_words_file, "wb") as f:
            pickle.dump(movie_words, f, pickle.HIGHEST_PROTOCOL)


    try:
        movie_syllables = pickle.load( open(movie_file, "rb"))
    except (OSError, IOError) as e:
        print("finding movie syllables")
        for m in movie_words:
            syllables = getPhonemes(m, entries)
            if syllables is not None:
                print((m,syllables))
                movie_syllables[m] = syllables

        with open(movie_file, "wb") as f:
            pickle.dump(movie_syllables, f, pickle.HIGHEST_PROTOCOL)
 
    try:
        fish_syllables = pickle.load( open(fish_file, "rb"))
    except (OSError, IOError) as e:
        fish_words = set() 
        with open(fish_source, "r") as f:
            for line in f:
                for x in line.split():
                    fish_words.add(x)

        print("finding fish syllables")
        for f in fish_words:
            syllables = getPhonemes(f, entries)
            if syllables is not None:
                print((f,syllables))
                fish_syllables[f] = syllables
       
        with open(fish_file, "wb") as f:
            pickle.dump(fish_syllables, f, pickle.HIGHEST_PROTOCOL)

    test = False 
    if (test):
        print(rhyme(entries['pie'][0], entries['pike'][0], 1))
    else:
        level = 1
        for mw, ms_list in movie_syllables.items():
            for fw, fs_list in fish_syllables.items():
                for ms in ms_list:
                    for fs in fs_list:
                        min_len = min(len(ms), len(fs), level)
                        max_len = max(len(ms), len(fs), level)
                        if mw != fw and rhyme(ms, fs, level):
                            print("\n" + str((mw, fw)))
                            for movie in movie_words[mw]:
                                pun = movie.lower().replace(mw, fw)
                                print(pun, end='')
