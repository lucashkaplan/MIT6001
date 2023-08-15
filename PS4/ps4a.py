# Problem Set 4A
# Name: Lucas Kaplan
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # list containing set of permutations for current sequence
    newPermList = []
    
    # base case: have sequence of length 1, only permutation is itself
    if len(sequence) == 1:
        return sequence
    
    # store first letter 
    letter = sequence[0]
    
    # find all permutations for sequence of length (n-1)
    permList = get_permutations(sequence[1:])
    
    # iterate through each element in sequence
    for perm in permList:
        # for each existing permutation, place the first letter at index 0 -> len(perm)
        # len(newElement) = len(perm) + 1 (b/c newElement must have the entire original permutation + the stored first letter)
        for idx in range(len(perm) + 1):
            newElement = perm[:idx] + letter + perm[idx:]

            if newElement not in permList:
                newPermList.append(newElement)
    
    return newPermList

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # Test Case 1
    print("\n\nTest Case 1")
    
    input = 'abcd'
    print('Input:', input)
    expectedOutput = ['abcd', 'abdc', 'acbd', 'acdb', 'adbc', 'adcb', 'badc', 'bacd', 'bcda', 'bcad', 'bdca', 'bdac', 'cabd', 'cadb', 'cbad', 'cbda', 'cdab', 'cdba', 'dacb', 'dabc', 'dbca', 'dbac', 'dcba', 'dcab']
    expectedOutput.sort()
    print('Expected Output:', expectedOutput)
    print('Actual Output:', get_permutations(input))

    sortedActualOutput = get_permutations(input)
    sortedActualOutput.sort()

    if expectedOutput != sortedActualOutput:
        print("Permutations not correctly generated!")

    # Test Case 2
    print("\n\nTest Case 2")
    
    input = 'fuz'
    print('Input:', input)
    expectedOutput = ['zuf', 'zfu', 'uzf', 'ufz', 'fzu', 'fuz']
    expectedOutput.sort()
    print('Expected Output:', expectedOutput)
    print('Actual Output:', get_permutations(input))

    sortedActualOutput = get_permutations(input)
    sortedActualOutput.sort()

    if expectedOutput != sortedActualOutput:
        print("Permutations not correctly generated!")

   
