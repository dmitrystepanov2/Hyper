from collections import defaultdict
from collections import Counter
import nltk
import random
import re

heads_dict = defaultdict(list)
bigrams = list()


def file_read(name):
    with open(name, 'r', encoding="utf-8") as file:
        text = file.read()
    bigrams = nltk.WhitespaceTokenizer().tokenize(text)
    bigrams = list(nltk.ngrams(bigrams, 3))
    for ram in bigrams:
        heads_dict[f"{ram[0]} {ram[1]}"].append(ram[2])


def markov_func(head):
    next_words = Counter(heads_dict[head]).most_common()
    next_word = next_words[0][0]
    key = head.split()[-1] + ' ' + next_word
    key = key.split()
    return key


def choise_head():
    heads = list(heads_dict.keys())
    head = random.choices(heads)
    return head[0]


def head_up():
    while True:
        head = choise_head()
        if bool(re.match('^[A-Z]', head)) and not bool(
                re.match('[A-Za-z|a-z]+[\.|\?|\!]', head)):
            break
    return head


def main():
    file_name = input('введите имя файла исходного текста:')
    file_read(file_name)
    out_file = open('out_file.txt', 'w')
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
        out_file.write(string + '\n')
    out_file.close()


if __name__ == "__main__":
    main()
