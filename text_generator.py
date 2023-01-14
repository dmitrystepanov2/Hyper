from collections import defaultdict
from collections import Counter
import nltk
import random
import re

heads_dict = defaultdict(list)
bigrams = list()


def file_read(name):
    global bigrams
    file = open(name, 'r', encoding="utf-8")
    text = file.read()
    file.close()
    bigrams = nltk.WhitespaceTokenizer().tokenize(text)
    bigrams = list(nltk.ngrams(bigrams, 3))
    for ram in bigrams:
        heads_dict[f"{ram[0]} {ram[1]}"].append(ram[2])


def markov_func(head):
    global heads_dict
    a = Counter(heads_dict[head]).most_common()
    next_word = a[0][0]
    key = head.split()[-1] + ' ' + next_word
    key = key.split()
    return key


def choise_head():
    global heads_dict
    heads = list(heads_dict.keys())
    head = random.choices(heads)
    return head[0]


def head_up():
    while True:
        head = choise_head()
        if bool(re.match('^[A-Z]', head)) and not bool(
                re.match('[A-Za-z|a-z]+[\.|\?|\!]', head)):  # and not bool(re.match('[\.|\?|\!]$', head)):
            break
    return head


def main():
    file_name = input('введите имя файла исходного текста:')
    file_read(file_name)
    for _ in range(10):
        sentences = 2
        head = head_up()
        string = head + ' '
        while True:
            markov = markov_func(head)
            string += markov[-1] + ' '
            sentences += 1
            if bool(re.findall('[\.|\?|\!]', markov[-1])):
                if sentences >= 5:
                    break
            head = markov[0] + ' ' + markov[-1]
        print(f"{string}")


if __name__ == "__main__":
    main()
