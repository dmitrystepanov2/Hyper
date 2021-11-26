from collections import defaultdict
from collections import Counter
import nltk
import random
import re

heads_dict = defaultdict(list)
bigrams = list()

def FileRead(name):
    global bigrams
    file = open(name, 'r', encoding="utf-8")
    text = file.read()
    file.close()
    bigrams = nltk.WhitespaceTokenizer().tokenize(text)
    #bigrams = list(nltk.bigrams(bigrams))
    bigrams = list(nltk.ngrams(bigrams, 3))
    for ram in bigrams:
        heads_dict[f"{ram[0]} {ram[1]}"].append(ram[2])
def Markov(head):
    global heads_dict
    a = Counter(heads_dict[head]).most_common()
    next_word = a[0]
    rr = next_word[0]
    a =head.split()
    key = a[-1] + ' ' + rr
    key = key.split()
    return key

def ChoiseHead():
    global heads_dict
    heads = list(heads_dict.keys())
    head = random.choices(heads)
    return head[0]

def HeadUp():
    while True:
        head = ChoiseHead()
        if bool(re.match('^[A-Z]', head)) and not bool(re.match('[A-Za-z|a-z]+[\.|\?|\!]', head)): #and not bool(re.match('[\.|\?|\!]$', head)):
            break
    return head

def main():

    file_name = input()
    FileRead(file_name)
    for _ in range(10):
        sentences = 2
        head = HeadUp()
        string = head + ' '
        while True:
            sss = Markov(head)
            string += sss[-1] + ' '
            sentences += 1
            if bool(re.findall('[\.|\?|\!]', sss[-1])):
                if sentences >= 5:
                    break
            head = sss[0] + ' ' + sss[-1]
        print(f"{string}")





if __name__ == "__main__":
    main()
