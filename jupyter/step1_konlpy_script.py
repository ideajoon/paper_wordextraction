from collections import Counter
from konlpy.tag import Kkma, Twitter, Hannanum

class KkmaWrapping:
    def __init__(self):
        self.kkma = Kkma()
    def tf(self, doc):
        words = Counter(self.kkma.pos(doc))
        words = [('%s/%s'%(word, tag), freq) for (word, tag), freq in words.items() if tag[0] == 'N' or tag[0] == 'V']
        return words
    
class TwitterWrapping:
    def __init__(self):
        self.twitter = Twitter()
    def tf(self, doc):
        words = Counter(self.twitter.pos(doc))
        words = [('%s/%s'%(word, tag), freq) for (word, tag), freq in words.items() if tag == 'Noun' or tag == 'Verb' or tag == 'Adjective']
        return words
    
class HannanumWrapping:
    def __init__(self):
        self.hannanum = Hannanum()
    def tf(self, doc):
        words = Counter(self.hannanum.pos(doc))
        words = [('%s/%s'%(word, tag), freq) for (word, tag), freq in words.items() if tag[0] == 'N' or tag[0] == 'P']
        return words


import sys
sys.path.append('../py/')
sys.path.append('../../soynlp/')
import configuration as config
from soynlp.utils import DoublespaceLineCorpus

corpus_fnames = config.normalized_corpus_fnames()
#taggers = [('twitter', TwitterWrapping()), ('hannanum', HannanumWrapping()), ('kkma', KkmaWrapping())]
taggers = [('kkma', KkmaWrapping())]
for name, tagger in taggers:
    for n_corpus, corpus_fname in enumerate(corpus_fnames):
        corpus_name = corpus_fname.split('/')[-1][:-4]
        if n_corpus < 3:
            print('skip corpus = %s' % corpus_name)
            continue
            
        corpus = DoublespaceLineCorpus(corpus_fname, iter_sent=False)        
        tokenized_corpus_fname = '%s/%s_%s.txt' % (config.model_folder, corpus_name, name)
        with open(tokenized_corpus_fname, 'w', encoding='utf-8') as f:
            for n_doc, doc in enumerate(corpus):
                try:
                    tf = tagger.tf(doc)
                    tf = ' '.join(['%s//%d'%t for t in tf])
                    f.write('%s\n' % tf)
                except:
                    f.write('\n')
                    continue
                if (n_doc + 1) % 100 == 0:
                    sys.stdout.write('\rtokenizing ... (%d in %d)' % (n_doc+1, len(corpus)))
            print('\r%s tokenized with %s' % (corpus_name, name))