import re
import numpy as np

def import_dict(file):
    """
    Import English word dictionary
    """
    dictionary = set()
    
    with open(file, "r") as f:
        for word in f:
            dictionary.add(word.split('\n')[0])
    return dictionary

def tokenization(text):
    """
    Split the text into tokens
    """
    return re.split(' ', text)

def check_spell(token, dictionary):
    """
    Check whether the token is in the dictionary
    """
    if len(token) == 0:
        return True
    if token.lower() not in dictionary:
        return False
    else: 
        return True

def lev_dist(string1,string2):
    """
    Apply Levenshtein distance algorithm
    """
    
    matrix1 = np.zeros((len(string1) +1,len(string2)+1),dtype = int)
    
    for i in range(1,len(string1) +1):
        for j in range(1,len(string2)+1):
            matrix1[i][0] = i
            matrix1[0][j] = j
    
    for x in range(1,len(string1) +1):
        for y in range(1,len(string2)+1):
            cost = 0 if string1[x-1] == string2[y-1] else 1
            matrix1[x][y] = min(matrix1[x-1][y] + 1, matrix1[x][y-1] + 1, matrix1[x-1][y-1] + cost) # lev algorithm
            
            
    return matrix1[x][y]

def smallest_lev_dist(text, dictionary):
    """
    Find a word with smallest Levenshtein distance to the input text in dictionary
    """

    sample = dictionary.pop()
    sample_dist = lev_dist(text, sample)
    
    for i in dictionary:
        dist = lev_dist(text, i)
        
        if dist < sample_dist:
            sample = i
            sample_dist = dist
        if sample_dist == 1:
            return sample
    return sample

def modifying(tokens, dictionary):
    """
    Modify the mis-spelled token with a word in the dictionary who has the smallest Levenshtein distance
    to the target token
    """
    for i, word in enumerate(tokens):
        # consider two cases:
        # 1. the word is the first word of a sentence, followed by '\n'
        # 2. the word is followed by a punctuation
        # first remove those characters, including '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' and '\n'
        # then add them back when using join function in the following
        if word[:1] == '\n':
            word = word[1:]
        
        if word[-1] in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
            word = word[:-1]
            
        # check the spelling, if it is not correct, find a replaced one
        if not check_spell(word, dictionary):
            word_mod = smallest_lev_dist(word, dictionary)
            if word[0].isupper():
                word_mod = word_mod[0].upper()+word_mod[1:]
                tokens[i] = tokens[i].replace(word,word_mod)
            else:
                tokens[i] = tokens[i].replace(word,word_mod)
                
        if tokens[i][:1] == '\n':
            tokens[i][1] == tokens[i][1].upper()
            
    final_str = " ".join(tokens)
    # assume the first character in a text is a capital letter
    # in case the first word is mis-spelled
    # capitalize the first letter of the first word because all words
    # in our dictionary is in lower case
    final_str = final_str[0].upper() + final_str[1:]
    return final_str

def tobemodified(tokens, dictionary):
    """
    Return mis-spelled tokens list
    """
    error_list = []
    for word in tokens:
        if word[:1] == '\n':
            word= word[1:]
        
        if word[-1] in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
            word = word[:-1]
    
        if not check_spell(word, dictionary):
            error_list.append(word)
    return error_list

def correction_function(text,dictionary):
    """
    Aggregate the above functions
    Print out the original text
    List mis-spelled words
    Print out the corrected version
    """
    word_dict = import_dict(dictionary)
    tokens = tokenization(text)
    err = tobemodified(tokens, word_dict)
    res = modifying(tokens, word_dict)
    print ("The original text is:")
    print(text)
    print("\n")
    print("The following words may be mis-spelled:")
    print(err)
    print("\n")
    print("The text after correction is:")
    print(res)
    print("\n")

## test two cases
EXAMPLE_STR = "The intersting fact is that the areas with higher economac mobility ratios is the same as \nthe Rich Places Index, showing the rich families are moree likely to have \nhigher mobility. Although American Dream states thaat everyone has an equal \nopportunity to gain money from a same beginning, the wealth barrier makes the equality \namong diffirent economic positions. In an extreme case, a child from a rich family can focus \non advanced research opportunities while a kid from a lower class has to consider paying back \nthe student loan."
test_case = 'Spellling correction is not an easy problem. Feel freee to assk questuions. \nI love answerring.'

correction_function(EXAMPLE_STR,'dict.txt')
correction_function(test_case,'dict.txt')


