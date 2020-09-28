import spacy

nlp = spacy.load('en_core_web_sm')

def determine_chunks(pronouns, vals, text,present_tenses = ['VBP', 'VBZ','VBG']):
#     nlp = spacy.load('en')

    present_tenses = ['VBP', 'VBZ','VBG']

    chunks = []

    iterations = len(pronouns)

    for i in range(iterations):

        start = vals[i]
        stop = None

        if i != (iterations - 1):
            stop = vals[i+1]

        if pronouns[i] != 'I':
            chunks.append((str(text[start:stop]),0))
            continue


        present_verbs_change = [word for word in text[start:stop]
                                if word.tag_ in
                                present_tenses]

        if len(present_verbs_change) == 0:
            chunks.append((str(text[start:stop]),0))
            continue

        chunks.append((str(text[start:stop]),1))

    return chunks

def determine_tense_input(sentence, present_tenses = ['VBP', 'VBZ','VBG']):

    """ Seperates words into chunks based on subjects of the sentence
    and sends them to the determine_chunks function to determine
    if that chunk requires further manipulation or not
    param ....
    .....
    ....
    returns: list of tuples (portion, int) where 1 means the chunk
    requires further manipulation and 0 means it can be left as is """

    text = nlp(sentence)

    present = len([word for word in text
                    if word.tag_ in present_tenses])

    if present == 0 :
        return [(sentence,0)]

    sub_toks = list(sorted([ (i, tok) for i, tok
                            in enumerate(text)
                            if tok.dep_ == "nsubj" ]))


    vals = [x[0] for x in sub_toks]
    pronouns = [str(x[1]) for x in sub_toks]

    if 'I' not in pronouns:
        return [(sentence,0)]

    return determine_chunks(pronouns, vals, text)
