import nltk
import collections
import numpy as np


class EntropyStringMatching:
    """
    This Entropy measurement is the information theory version
    which is designed to find similarity between strings.

    Break strings into ngrams and find the total amount of overlap between
    the two strings.

    Args:
        string_1 and string_2 are two strings that you wish to compare
        how closely related they are.

    Returns:
        A number between 0 and 1. 1 being an exact match while 0 means they have nothing in common.

    """

    def __init__(self):

        self.string_1 = None
        self.string_2 = None

    def set_strings(self, string_1, string_2):

        self.string_1 = string_1
        self.string_2 = string_2

    def run(self, string_1, string_2):

        self.set_strings(string_1, string_2)

        input_1 = self.get_entropy(self.string_1)
        input_2 = self.get_joint_entropy(self.string_1, self.string_2)

        top_value = self.calculate_entropy(input_2)
        bottom_value = self.calculate_entropy(input_1)

        final = top_value / bottom_value

        return final

    def get_entropy(self, input_string):
        bigram = list(nltk.bigrams(input_string.lower()))
        bigram_dict = collections.Counter(bigram)
        values = map(lambda j: self.entropy_score(bigram_dict[j], bigram), bigram_dict)
        return values

    @staticmethod
    def calculate_entropy(string_input):
        entropy = sum(i*np.log2(i) for i in string_input) * -1
        return entropy

    @staticmethod
    def get_joint_entropy(string1, string2):
        bigram1 = list(nltk.bigrams(string1.lower()))
        bigram2 = list(nltk.bigrams(string2.lower()))
        combo = bigram1 + bigram2
        bigram_dict = collections.Counter(combo)
        
        for i in bigram_dict:
            if i in bigram1 and i in bigram2:
                value = float(bigram_dict[i]) / float(len(combo))
                yield value

    @staticmethod
    def entropy_score(item, input_list):
        value = float(item) / float(len(input_list))
        return value


def entropy(string):
    x = []
    bigram = list(nltk.bigrams(string.lower()))
    de_duped = list(set(bigram))
    for i in de_duped:
        count = float(bigram.count(i))/float(len(bigram))
        x.append(count)
    calc = sum(i*np.log2(i) for i in x)*-1
    return calc


def joint_entropy(string1, string2):
    x = []
    bi1 = list(nltk.bigrams(string1.lower()))
    bi2 = list(nltk.bigrams(string2.lower()))
    combo = bi1 + bi2
    yes = list(set(combo))
    for i in yes:
        if i in bi1 and i in bi2:
            count = (float(bi1.count(i))+float(bi2.count(i)))/float(len(combo))
            x.append(count)
    calc = sum(i*np.log2(i) for i in x)*-1
    return calc


def point_mutual_info(joint_count, individual_count_1, individual_count_2, n):
    #n is the length of all jobs considered
    numerator = float(joint_count)/float(n)
    denominator_1 = float(individual_count_1)/float(n)
    denominator_2 = float(individual_count_2)/float(n)
    mutual_info = np.log2(numerator/(denominator_1 * denominator_2))
    return mutual_info


class Entropy:

    def __init__(self, string1, string2):

        first_input = self.get_entropy(string1)
        self.bottom = self.calculate(first_input)
        second_input = self.get_joint_entropy(string1, string2)
        self.top = self.calculate_joint(second_input)
        self.final = self.top / self.bottom

    def get_entropy(self, string1):
        bigram = list(nltk.bigrams(string1.lower()))
        bigram_dict = collections.Counter(bigram)
        values = map(lambda j: self.entropy_score(bigram_dict[j], bigram), bigram_dict)
        return values

    @staticmethod
    def calculate(input):
        entropy = sum(i*np.log2(i) for i in input) * -1
        return entropy

    @staticmethod
    def get_joint_entropy(string1, string2):
        first_bigram = list(nltk.bigrams(string1.lower()))
        second_bigram = list(nltk.bigrams(string2.lower()))
        combo = first_bigram + second_bigram
        bigram_dict = collections.Counter(combo)

        for i in bigram_dict:
            if i in first_bigram and i in second_bigram:
                value = float(bigram_dict[i]) / float(len(combo))
                yield value

    @staticmethod
    def calculate_joint(input2):
        entropy = sum(i*np.log2(i) for i in input2) * -1
        return entropy

    @staticmethod
    def entropy_score(item, fancy_list):
        value = float(item) / float(len(fancy_list))
        return value