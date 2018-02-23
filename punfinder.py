#!/bin/python
import nltk
import string
import pickle
from collections import defaultdict
from Levenshtein import distance

def getSyllables(queryword, entries):
    try:
        return entries[queryword]
    except KeyError:
        return None;

def nsyl(word):
  return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 

if __name__ == "__main__":
        
    entries = nltk.corpus.cmudict.dict()
    movie_syllables = dict()
    fish_syllables = dict()
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
            syllables = getSyllables(m, entries)
            if syllables is not None:
                print((m,syllables))
                for s in syllables:
                    movie_syllables[m] = s

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
            syllables = getSyllables(f, entries)
            if syllables is not None:
                print((f,syllables))
                for s in syllables: 
                    fish_syllables[f] = s
       
        with open(fish_file, "wb") as f:
            pickle.dump(fish_syllables, f, pickle.HIGHEST_PROTOCOL)

    level = 3
    for mw, ms in movie_syllables.items():
        for fw, fs in fish_syllables.items():
            min_len = min(len(ms), len(fs), level)
            max_len = max(len(ms), len(fs), level)
            if mw != fw and (ms[-min_len:] == fs[-min_len:] or ms[:min_len] == fs[:min_len] or distance(mw, fw) < int(max_len/3)):
                print("\n" + str((mw, fw)))
                for movie in movie_words[mw]:
                    pun = movie.lower().replace(mw, fw)
                    print(pun, end='')
