import os
import gzip
import json
import codecs
from optparse import OptionParser
from collections import Counter

import numpy as np
import pandas as pd

from util import *

def read_jsonlist(input_filename):
    data = []
    if input_filename[-3:] == '.gz':
        with gzip.open(input_filename, 'r') as input_file:
            for l_i, line in enumerate(input_file):
                data.append(json.loads(line, encoding='utf-8'))
    else:
        with codecs.open(input_filename, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                data.append(json.loads(line, encoding='utf-8'))
    return data


def main():
    usage = "%prog input.jsonlist output_file"
    parser = OptionParser(usage=usage)
    parser.add_option('--lex', dest='lex', default='EmoLex',
                      help='Lexicon to use [emolex|LIWC2007|LIWC2015|OptPess|Agency|Auth]: default=%default')
    parser.add_option('-p', action="store_true", dest="percentages", default=False,
                      help='Report percentages: default=%default')

    (options, args) = parser.parse_args()
    infile = args[0]
    outfile = args[1]

    lexicon = options.lex.lower()        
    percentages = options.percentages

    if lexicon == 'emolex':
        lex = nrc.parse_emolex()
    elif lexicon == 'liwc2007':        
        lex = liwc.parse_liwc("2007")
    elif lexicon == 'liwc2015':        
        lex = liwc.parse_liwc("2015")
    elif lexicon == 'optpess':
        lex = nrc.parse_optpess()
    elif lexicon == 'agency':
        lex = conno.parse_connotation("agency")
    elif lexicon == 'auth':
        lex = conno.parse_connotation("authority")

    docs = read_jsonlist(infile)
    key_counter = set()

    values_list = []

    for i, doc in enumerate(docs):
        if i % 1000 == 0 and i > 0:
            print(i)
        text = doc['text']
        values = extract(lex, text, percentage=percentages)
        values_list.append(values)
        key_counter.update(values.keys())

    keys = list(key_counter)
    keys.sort()
    df = pd.DataFrame(np.zeros([len(docs), len(keys)]), columns=keys)

    for i, value_dict in enumerate(values_list):
        vec = np.zeros(len(keys))
        for k_i, k in enumerate(keys):
            if k in value_dict:
                vec[k_i] = value_dict[k]
        df.iloc[i] = vec

    df.to_csv(outfile)


if __name__ == '__main__':
    main()
