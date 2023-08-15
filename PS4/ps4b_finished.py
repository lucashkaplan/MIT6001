# Problem Set 4B
# Name: Lucas Kaplan
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'
# lists containing all UPPERCASE and lowercase letters
alphabetUpper = list(string.ascii_uppercase) 
alphabetLower = list(string.ascii_lowercase)

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            1. self.message_text (string, determined by input text)
            2. self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # ensure that 0 <= shift < 26
        assert (0 <= shift < 26), "Invalid shift amount entered. Shift must be in range: [0, 26]"

        # dict containing corresponding shift for all letters, both upper and lowercase
        shiftDict = {}
        
        for letter in alphabetUpper:
            # index for new letter
            newLetterIndex = ord(letter) + shift - ord('A')
        
            if (ord(letter) + shift) > ord('Z'):
                shiftDict[letter] = alphabetUpper[newLetterIndex - 26]
                shiftDict[letter.lower()] = alphabetLower[newLetterIndex - 26]
            else:
                shiftDict[letter] = alphabetUpper[newLetterIndex]
                shiftDict[letter.lower()] = alphabetLower[newLetterIndex]
        
        return shiftDict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: string: the message text in which every character is shifted
                 down the alphabet by the input shift
        '''
        # ensure that 0 <= shift < 26
        assert (0 <= shift < 26), "Invalid shift amount entered. Shift must be in range: [0, 26]"
        
        # string containing shifted message (ciphertext)
        ciphertext = ''

        # build the shift dictionary for the given shift amount using the build_shift_dict method of the Message class
        shiftDict = self.build_shift_dict(shift)
        
        # for all char in input text
        for char in self.message_text:
            # if char is a letter, add its shifted counterpart to ciphertext
            if char in shiftDict:
                ciphertext += shiftDict[char]
            # o.w. add char to ciphertext
            else:
                ciphertext += char

        return ciphertext



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # intialize self.message_text and self.valid_words through superclass (Message class)
        super().__init__(text)
        
        # initialize instance vars
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        # update shift
        self.shift = shift
        # update all data attributes dependent on shift
        self.encryption_dict = Message.build_shift_dict(self.shift)
        self.message_text_encrypted = Message.apply_shift(self.shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # init. shift that leads to max number of valid words and amount of matching words
        bestShiftVal = 0
        maxValidWords = 0
        
        # try all shifts in range: [0, 26)
        for shift in range(26):
            # valid words for curr shift value
            currValidWords = 0

            # apply shift
            decodedText = super().apply_shift(shift)

            # split the string into list of "words", separated by space
            decodedText = decodedText.split()

            for word in decodedText:
                # remove non-alphanumeric symbols from "word"
                # filter(): iterates over each element in word (string).
                #           if str.isalnum() returns True, adds the element to an iterator
                # ''.join(): joins all the elements in the iterator together w/ '' b/w them
                word = ''.join(filter(str.isalnum, word))

                if word in self.valid_words:
                    currValidWords += 1

            # track shift that stores max number of words
            if currValidWords > maxValidWords:
                bestShiftVal = shift
                maxValidWords = currValidWords
        
        # return tuple: ([best shift val to decrypt the message], [decrypted message])
        return (bestShiftVal, super().apply_shift(bestShiftVal))

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    # Message Test Cases
    # Message Test Case 1
    print('Message Class Test Case 1')
    text = 'Hello, World!'
    shift = 4
    originalMsg = Message(text)
    print('Expected Output: Lipps, Asvph!')
    print('Actual Output:', originalMsg.apply_shift(shift))

    # PlaintextMessage Test Cases
    # Test Case 1
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # Test Case 2
    plaintext = PlaintextMessage("My friend's in there.", 13)
    print("Expected Output: Zl sevraq'f va gurer.")
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # CiphertextMessage Test Cases
    # Test Case 1
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Test Case 2
    ciphertext = CiphertextMessage("Zl sevraq'f va gurer.")
    print('Expected Output:', (26-13, "My friend's in there."))
    print('Actual Output:', ciphertext.decrypt_message())

    # decrypt the story
    cipheredStory = get_story_string()
    cipheredStoryObj = CiphertextMessage(cipheredStory)
    (bestShift, decryptedStory) = cipheredStoryObj.decrypt_message()
    
    print("\n-------------------------------------------------------")
    print('Best Shift Value:', bestShift)
    print("Decrypted Story:", decryptedStory, sep='\n')


    
