import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
highlightOn = "[[HIGHLIGHT]]"
highlightOff = "[[ENDHIGHLIGHT]]"
snippetLen = 400

def boyer_more_string_search(haystack, needle):
    """
    Implementation of the Boyer-Moore string search algorithm. 
    This finds all occurrences of P in T, and  encloses each occurrence of P in T within the highlight tag
    This implementation performs a case-insensitive search on ASCII alphabetic characters.
    Args: 
        haystack     Sentence to be highlighted (string)
        needle       Multiword/single word search query (string)
    Returns:
        Sentence with the instance of query enclosed within the highlight tag, if a match is found
        Else, returns an empty string   
    """
    match = []
    #Return if the haystack or needle is empty
    if not len(haystack) > 0 or not len(needle) > 0:
        return match
    needleLen = len(needle)
    #Preprocessing: Initialize tables as defined in the good suffix and bad character rule in the Boyer-Moore algorithm   
    badCharTable = init_bad_char_table(needle)
    goodSuffixTable = init_good_suffix_table(needle)
    #Initialize iterator to point to character in haystack given by the needle length such that needle is aligned with the start of haystack
    i = needleLen - 1
    outputText = ""
    endOfPreviousMatch = 0
    while i < len(haystack):
        j = needleLen - 1
        #Continue comparison until there's a mismatch or all characters have been matched
        while needle[j].lower() == haystack[i].lower():
            #All the characters in needle have matched with all the characters in haystack
            #Returns the index 'i' as the starting index of the first occurrence of needle in haystack
            if j == 0:
                match.append(i)
                #The needle could be matched with a substring in haystack, find the startpos and endpos of the string
                #which encloses the matched needle, so that the string can be highlighted rather than the substring
                #The process can be skipped if partial highlighting is desirable
                
                #Assumes that the words are separated by whitespaces 
                #Returns the position of the first whitespace before the current word
                startOfWord = haystack[:i].rfind(r" ")
                #Base case if the match is in the first word in the haystack
                startOfWord = max(0, startOfWord+1) 
                endOfWord = haystack.find(r" ", i + needleLen)
                #insert the begin highlight tag before the first character of the current word
                if endOfWord > 0:
                    i = endOfWord + needleLen - 1
                    outputText += haystack[endOfPreviousMatch:startOfWord] + highlightOn + haystack[startOfWord:endOfWord] + highlightOff
                else:
                    i = len(haystack)
                    outputText += haystack[endOfPreviousMatch:startOfWord] + highlightOn + haystack[startOfWord:] + highlightOff
                    return outputText
                #Update 'endOfPreviousMatch' so that the next match in the same sentence appends the slice of str[endIndexOfPreviousMatch:startingIndexOfCurrentMatch]
                #to the output string
                endOfPreviousMatch = endOfWord
                break
            i -= 1
            j -= 1
        if j != 0:
            #In case of a mismatch calculate the number of positions in haystack that can be skipped
            #The value of 'i' indicates the index in haystack which will align with the last character in needle
            i += max(goodSuffixTable[needleLen - 1 - j], badCharTable[ord(haystack[i])])
    return outputText + haystack[endOfPreviousMatch:] if len(match) > 0 else ""

def init_bad_char_table(needle):
    """
    Bad character rule defines the number of positions to shift so that the mismatched character is aligned with the last occurrence of that 
    character in the initial part of the pattern (pattern minus last pattern character), if there is such an occurrence, or one position
    before the pattern if the mismatched character doesn't appear in the initial part of the pattern at all.
    Args:
        needle    The search query (string)
    Returns:
        Bad character table as initialized as per the rule outlined above   
        If there are no instances of a character in the prefix, shift length of needle positions
        Else shift number of positions given by the offset of difference in the index positions of the mismatched character and the last
        occurrence of the character in the prefix of needle 
        
        -    -    -    -    X    -    -    K    -    -    -
        A    N    P    A    N    M    A    N    A    M    -
        -    N    N    A    A    M    A    N    -    -    -
        -    -    -    N    N    A    A    M    A    N    -
        Demonstration of bad character rule with pattern NNAAMAN.
    """
    ALPHABET_SIZE = 256
    needleLen = len(needle)
    badCharTable = [needleLen]*ALPHABET_SIZE
    for i in range(0, needleLen - 1):
        badCharTable[ord(needle[i])] = needleLen - 1 - i
    return badCharTable

def init_good_suffix_table(needle):
    """
    The good suffix rule, aligns the matched part of the text, P, with the rightmost occurrence of that character sequence in the pattern 
    that is preceded by a different character (including none, if the matched suffix is also a prefix of the pattern) than the matched 
    suffix P of the pattern - if there is such an occurrence.
    Args:
        needle    The search query (string)
    Returns:
        Good suffix table as defined by the rules above. 
        For each i, L[i] is the largest position less than n such that string P[i..n] matches a suffix of P[1..L[i]] and such that the
        character preceding that suffix is not equal to P[i-1]. L[i] is defined to be zero if there is no position satisfying the condition.
        
        -    -    -    -    X    -    -    K    -    -    -    -    -
        M    A    N    P    A    N    A    M    A    N    A    P    -
        A    N    A    M    P    N    A    M    -    -    -    -    -
        -    -    -    -    A    N    A    M    P    N    A    M    -
        Demonstration of good suffix rule with pattern ANAMPNAM.
    """
    needleLen = len(needle)
    goodSuffixTable = [0]*needleLen
    lastPrefixPos = needleLen
    for i in range(needleLen - 1, 0, -1):
        if is_prefix(needle, i + 1):
            lastPrefixPos = i + 1
        goodSuffixTable[needleLen - 1 - i] = lastPrefixPos - i + needleLen - 1
    for i in range(0, needleLen - 1):
        suffix_len = get_suffix_len(needle, i)
        goodSuffixTable[suffix_len] = needleLen - 1 - i + suffix_len
    return goodSuffixTable

 
def is_prefix(needle, startIndex):
    """
    Args:
        needle        The search query (string)
        startIndex    Starting index of the substring which is being checked for being a prefix
    Returns:
        True if the substring needle[startIndex:] is a prefix in needle
        False, otherwise
    """
    needleLen = len(needle)
    j = 0
    for i in range(startIndex, needleLen - 1):
        if needle[i] != needle[j]:
            return False
        j += 1
    return True

def get_suffix_len(needle, startIndex):
    """
    Args:
        needle        The search query (string)
        startIndex    Starting index of the suffix
    Returns:
        Number of characters in the needle[:startIndex] which matches the suffix
    """
    needleLen = len(needle)
    suffixLen = 0
    i = startIndex
    j = needleLen - 1
    while i >= 0 and needle[i] == needle[j]:
        i -= 1
        j -= 1
        suffixLen += 1
    return suffixLen

def remove_dup_highlights(output):
    formattedOutput = re.sub("%s %s" %(re.escape(highlightOff), re.escape(highlightOn)), " ", output)
    return formattedOutput

def remove_common_words_from_query(query):
    commonWords = set(stopwords.words('english'))
    return filter(lambda word: not word in commonWords, query.split())

def highlight_doc(doc,query):
    """
    Args: 
        doc     Document to be highlighted (string)
        query   Multiword/single word search query (string)
    Returns:
        The most relevant snippet of length 400 characters with the query terms highlighted (string)
        Searches for the exact match for the query in the doc and returns the snippet if an exact match is found
        Else removes some common words from the query and tries to match as many individual words in the resultant query
        in the doc
        Matches substrings in doc which match a word or words in the query
        Example: Query: "Pill" matches both "Pillar" and "Pillow" 
    """
    notFound = "No matching results found"
    #Remove any whitespace characters from the doc and query
    doc = doc.strip()
    query = query.strip()
    if not len(doc) > 0 or not len(query) > 0:
        return notFound
    #Extract words from the query and remove common words to increase the chances of finding a more appropriate match
    #and to prevent from returning a unrelated snippet
    queryWords = remove_common_words_from_query(query)
    #remove duplicate words from query
    queryWords = list(set(queryWords))
    outputText = ""
    outputSentence = ""
    #Tokenize document into sentences which are separated by '.!?'
    for sentence in sent_tokenize(doc): 
        outputSentence = ""
        #Try to match the entire query in the doc 
        outputSentence = boyer_more_string_search(sentence, query.strip())
        if len(outputSentence) > 0:
            outputText += outputSentence
        else:
            #If there's no match for the entire query, try matching as many words in query with the doc after removing the commons
            #from the query, so as to refine the search  
            outputSentence = highlight_words(sentence, queryWords)
            outputText += outputSentence
    if len(outputText) > 0:
        #Adjust tags around adjacent words so that they are enclosed within the same tag so as to prevent a scenario of
        #....[[HIGHLIGHT]]str1[[ENDHIGHLIGHT]] [[HIGHLIGHT]]str2[[ENDHIGHLIGHT]]....
        outputText = re.sub("%s %s" %(re.escape(highlightOff), re.escape(highlightOn)), " ", outputText)
    #Truncate the snippet if longer than the threshold length
    return (outputText[:snippetLen] + "..." if len(outputText) > snippetLen else outputText) if len(outputText) > 0 else notFound
    
def highlight_words(sentence,queryWords):
    """
    Args: 
        sentence    Sentence to be highlighted (string)
        queryWords  Multiword/single word search query (list of strings)
    Returns:
        Sentence with the matching query words enclosed within the highlight tags, if a match is found
        Returns an empty string otherwise
    """
    haystack = sentence
    outputSentence = ""
    outputText = ""
    #Dictionary to prevent appending a sentence more than once, if the sentence contains more than one matching query words
    outputDict = {}
    for word in queryWords: 
        if sentence in outputDict:
            #Sentence was already modified
            haystack = outputDict[sentence]
        outputSentence = boyer_more_string_search(haystack, word)
        if len(outputSentence) > 0:
            outputDict[sentence] = outputSentence
    #Append all values in the dictionary to be returned as the output snippet
    if sentence in outputDict:
        outputText += outputDict[sentence]
    return outputText



    
      

    
