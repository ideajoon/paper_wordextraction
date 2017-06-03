from itertools import chain, combinations
import configuration as config
engine = config.get_engine()

def get_article_idx(query, date):
    urls = engine.get_article_urls(query, date)
    return parse_article_idx(urls)

def parse_article_idx(urls):
    def parse(url):
        if not ('?' in url):
            return '', ''
        parts = dict(part.split('=') for part in url.split('?')[1].split('&'))
        return parts.get('oid', ''), parts.get('aid', '')

    news_idx = [parse(url) for url in urls]
    news_idx = [idx for idx in news_idx if (idx[0] and idx[1])]
    return news_idx

def iterate_keyword_combination(keywords_candidates, n_keywords):
    if type(n_keywords) == int:
        n_keywords = [n_keywords]
    for keywords in chain(*[combinations(keywords_candidates, n) for n in n_keywords]):
        yield ' '.join(keywords)
    
def get_article_num_of_keywords(keywords_candidates, date):
    if len(keywords_candidates) < 3:
        keywords = ' '.join(keywords_candidates)
        return [(date, keywords, engine.get_article_num(keywords, date))]
    num_articles = []
    for keywords in iterate_keyword_combination(keywords_candidates):
        num = engine.get_article_num(keywords, date)
        num_articles.append((date, keywords, num))
    return num_articles