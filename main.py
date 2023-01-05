import requests
from tqdm import tqdm
import os
from lm_dataformat import Archive
import shutil
import spacy
import json
import glob
import time
import sys

def get_word_stats(txt):
    if not txt:
        return 0, 0, 0, 0, 0, 0

    sentences = 0
    words = 0
    verbs = 0
    nouns = 0
    punctuations = 0
    symbols = 0

    doc = nlp(txt)

    sentences = len(list(doc.sents))
    words = len([token.text for token in doc if not token.is_punct])
    nouns = len([token.text for token in doc if (not token.is_stop and not token.is_punct and token.pos_ == "NOUN")])
    verbs = len([token.text for token in doc if (not token.is_stop and not token.is_punct and token.pos_ == "VERB")])
    punctuations = len([token.text for token in doc if (token.is_punct or token.pos_ == "PUNCT")])
    symbols = len([token.text for token in doc if (token.pos_ == "SYM")])

    return sentences, words, verbs, nouns, punctuations, symbols


nlp = spacy.load("pl_core_news_md")
txt_datasets = glob.glob('./*.json')

for f in txt_datasets:

    ar = Archive('./data')

    data = None
    with open(f, 'r') as jf:
        data = json.load(jf)

    file_name_zst = './' + data.get("name","") + '.zst'
    file_name_manifest = './' + data.get("name","") + '.manifest'

    total_len = 0
    total_docs = 0
    total_sentences = 0
    total_words = 0
    total_verbs = 0
    total_nouns = 0
    total_punctuations = 0
    total_symbols = 0

    if data:
    
        txt_files = glob.glob(f.replace('.json','') + '/*.txt')
        for txt_file in txt_files:
            with open(txt_file, 'r') as tf:
                print("Processing file: " + txt_file)
                txt = tf.read()
                l = len(txt)
                if l > 100000:
                    nlp.max_length = len(txt) + 100
                sentences, words, verbs, nouns, punctuations, symbols = get_word_stats(txt.strip())
                total_words += words
                total_verbs += verbs
                total_nouns += nouns
                total_len += l
                total_docs += 1
                total_sentences += sentences
                total_punctuations += punctuations
                total_symbols += symbols
                meta = {'name' : txt_file, 'length': l, 'sentences': sentences, 'words': words, 'verbs': verbs, 'nouns': nouns, 'punctuations': punctuations, 'symbols': symbols}
                ar.add_data(txt.strip(), meta = meta)

        ar.commit()

        data_files= glob.glob('./data/*')
        file_size = 0

        for f in data_files:
            if f.endswith('.zst'):
                shutil.copy(f, os.path.join(file_name_zst))
                file_size = os.path.getsize(file_name_zst)

            os.remove(f)

        manifest = {"project" : data.get("project",""), "name": data.get("name",""), "description": data.get("desctiption",""), "license": data.get("license",""), "language": data.get("language",""), "file_size" : file_size, "sources": data.get("sources",[]), "stats": {"documents": total_docs, "sentences": total_sentences, "words" : total_words, "nouns" : total_nouns, "verbs" : total_verbs, "characters": total_len, "punctuations" : total_punctuations, "symbols" : total_symbols}}
        json_manifest = json.dumps(manifest, indent = 4) 

        with open(file_name_manifest, 'w') as mf:
            mf.write(json_manifest)






