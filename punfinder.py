#!/bin/python
import nltk
import string
import pickle

movie_words = set() 
fish_words = set() 

def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def getSyllables(queryword, entries):
    for word, syl in entries: 
        if word == queryword:
            return syl

def doTheyRhyme(word1, word2):
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find ( word2 ) == len(word1) - len ( word2 ):
        return False
    if word2.find ( word1 ) == len ( word2 ) - len ( word1 ): 
        return False

    return word1 in rhyme ( word2, 3 )

if __name__ == "__main__":
        
    movie_syllables = dict()
    fish_syllables = dict()
    movie_file = "movie_syllables.pickle"
    fish_file = "fish_syllables.pickle"

    try:
        movie_syllables = pickle.load( open(movie_file, "rb"))
        fish_syllables = pickle.load( open(fish_file, "rb"))
    except (OSError, IOError) as e:


        with open("movies_small.txt", "r") as f:
            for line in f:
                x = line.split('\t', 1)[1]
                for s in x.split():
                    s = s.translate(string.punctuation).lower()
                    s = s.replace(':', '')
                    if len(s) > 2:
                        movie_words.add(s)
                        print(s)

        with open("fish.txt", "r") as f:
            for line in f:
                for x in line.split():
                    fish_words.add(x)


        print("finding movie syllables")
        entries = nltk.corpus.cmudict.entries()
        for m in movie_words:
            s = getSyllables(m, entries)
            if s is not None:
                print((m,s))
                movie_syllables[m] = s

        print("finding fish syllables")

        for f in fish_words:
            s = getSyllables(f, entries)
            if s is not None:
                print((f,s))
                fish_syllables[f] = s

        with open(movie_file, "wb") as f:
            pickle.dump(movie_syllables, f, pickle.HIGHEST_PROTOCOL)

        with open(fish_file, "wb") as f:
            pickle.dump(fish_syllables, f, pickle.HIGHEST_PROTOCOL)

    print(movie_syllables)
    print("FISH")
    print(fish_syllables)

    level = 2
    for mw, ms in movie_syllables.items():
        for fw, fs in fish_syllables.items():
            if ms[-level:] == fs[-level:]:
                print((mw, fw))
            

