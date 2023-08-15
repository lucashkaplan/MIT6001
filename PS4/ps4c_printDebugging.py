# Problem Set 4C
# Name: Lucas Kaplan
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations
import math

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    # class var valid_words = list containing all valid words, determined using helper function load_words
    valid_words = load_words(WORDLIST_FILENAME)

    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has one attribute:
            self.message_text (string, determined by input text)
        '''
        self.message_text = text
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text
        
    @classmethod
    def get_valid_words(cls):
        '''
        Used to safely access a copy of valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of valid_words
        '''
        return cls.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        transposeDict = {}

        # assert that all elements of vowels_permutation are vowels
        assert [(char in VOWELS_LOWER or char in VOWELS_UPPER) for char in vowels_permutation], "Invalid character in string vowels_permutation. All letters must be vowels."
        # assert that no element in vowels_permutation is repeated
        assert len(set(vowels_permutation)) == len(vowels_permutation), "Character repeated in string vowels_permutation."
        # assert that vowels_permutation has 5 elements
        assert len(vowels_permutation) == 5, "string vowels_permutation must have a length of 5."
        
        # make input string all lowercase
        vowels_permutation = vowels_permutation.lower()
        
        # each vowel in VOWELS_LOWER is key, and each vowel in vowels_permutation is value
        for idx, vowel in enumerate(VOWELS_LOWER):
            # map all lowercase vowels
            transposeDict[vowel] = vowels_permutation[idx]
            # map all uppercase vowels
            transposeDict[vowel.upper()] = vowels_permutation[idx].upper()
        
        # map all consonants to themselves
        for consonant in CONSONANTS_LOWER:
            transposeDict[consonant] = consonant
            transposeDict[consonant.upper()] = consonant.upper()
        
        return transposeDict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        encryptedText = ''

        # for all letters in self.message_text, apply the shift
        # by definition, shift will only be applied to vowels
        for char in self.message_text:
            if char in transpose_dict:
                encryptedText += transpose_dict[char]
            else:
                encryptedText += char
        
        return encryptedText
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
        '''
        super().__init__(text)

    @classmethod
    def validWordCounter(cls, decodedText):
        '''
        Counts the number of valid words in the decoded text.

        Inputs:
            decodedText (string): the decrypted text
        Returns:
            currValidWords (int): number of valid words in the text
        '''
        currValidWords = 0
        
        # make all words lower case
        decodedText = decodedText.lower()
        
        # split the string into list of "words", separated by space
        decodedText = decodedText.split()

        for word in decodedText:
            # remove non-alphanumeric symbols from "word"
            # filter(): iterates over each element in word (string).
            #           if str.isalnum() returns True, adds the element to an iterator
            # ''.join(): joins all the elements in the iterator together w/ '' b/w them
            word = ''.join(filter(str.isalnum, word))

            print("word:", word)

            if word in cls.valid_words:
                currValidWords += 1

            print("Number of valid words:", currValidWords)

        return currValidWords
    
    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        maxValidWords = 0
        
        # get all permutations of vowels
        vowelPerms = get_permutations('aeiou')

        print("Number of vowel permutations:", len(vowelPerms))
        print("Expected number of vowel permutations:", math.factorial(5))
        
        # try all vowel permutations as shift and count resulting number of valid words
        for vowelPerm in vowelPerms:
            # build transpose dict
            transposeDict = super().build_transpose_dict(vowelPerm)

            print("Current transpose dict:", transposeDict, sep='\n')

            # apply transpose
            decryptedText = super().apply_transpose(transposeDict)

            # find number of valid words
            currValidWords = self.validWordCounter(decryptedText)

            print("\n------------------------------------------------------")
            print("Current Valid Words in decrypt_message:", currValidWords)
            print("Max Valid Words in decrypt_message:", maxValidWords)
            
            # track shift that stores max number of words
            if currValidWords > maxValidWords:
                bestPerm = vowelPerm
                maxValidWords = currValidWords
        
        # build transpose dict and return transposed message from best vowel permutation
        transposeDict = super().build_transpose_dict(bestPerm)
        return super().apply_transpose(transposeDict)
    

if __name__ == '__main__':

    # Example test case
    # message = SubMessage("Hello World!")
    # permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    # print("Decrypted message:", enc_message.decrypt_message())
    
    # SubMessage Class Test Cases
    # Test Case 1
    # print("\nSubMessage class test case 1.")
    # message = SubMessage("The vowels will be changed.")
    # # original order: aeiou
    # permutation = "oiuea"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "\nPermutation:", permutation)
    # print("Expected encryption:", "Thi vewils wull bi chongid.")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    # print("Decrypted message:", enc_message.decrypt_message())

    # Test Case 2
    print("\nSubMessage class test case 2.")
    message = SubMessage("What? He did not say that!")
    # original order: aeiou
    permutation = "uoiea"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "\nPermutation:", permutation)
    print("Expected encryption:", "Whut? Ho did net suy thut!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
