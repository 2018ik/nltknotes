from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import nltk.data
from bs4 import BeautifulSoup
import requests
import re
 
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
 
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        simlist = [synset.path_similarity(ss) for ss in synsets2 if synset.path_similarity(ss) is not None]
        if not simlist:
            continue;
        best_score = max(simlist)

    # Check that the similarity could have been computed
        score += best_score
        count += 1

    if count == 0:
        return 0

    # Average the values
    score /= count
    return score

def data_splitter(array):
    output = []
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for x in array:
        data = x.text
        y = tokenizer.tokenize(data)
        for z in y:
            output.append(re.sub('[[0-9]+]', '', z))
    return [x for x in output if x != [] and x != '']

respond = requests.get(input("Enter website link: "))
soup = BeautifulSoup(respond.text, "html.parser")
l = soup.find_all('p')
sourcesents = data_splitter(l)


lines = [line.rstrip('\n') for line in open('notes.txt')]
lines = [x for x in lines if x != [] and x != '']

expansion = lines.copy()

for count, notes in enumerate(lines):
    best = 0;
    for sources in sourcesents:
        new = sentence_similarity(notes,sources)
        if new>best:
            best = new
            print(count)
            expansion[count] = sources

expanded = open('expanded.txt', 'w')
for x,y in zip(lines,expansion):
        expanded.write(x+"\n")
        expanded.write(y+"\n")
        expanded.write("----------\n")
expanded.close()
    



