def search4vowels(word: str) -> set:
    """ Display any vowels found in a word """
    vowels = set('aeiou')
    return vowels.intersection(set(word))


def search4letter(phrsae: str, letters: str = 'aeiou') -> set:  
    """Returns a set of letters found in phrases"""
    return set(letters).intersection(set(phrsae))


# print(search4letter(letters='ay', phrsae='ysssa'))
# az = help(search4letter)
# print(az)
