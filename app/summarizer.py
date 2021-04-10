from random import randint
# from newsfetch.google import google_search
# from newsfetch.news import newspaper
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
from .models import *
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

from .question_generation.pipelines import pipeline
from random import randint

nlp = pipeline("question-generation")


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

def get_random_news():
    googlenews = GoogleNews()
    googlenews.set_lang('en')
    googlenews.search('Digital Privacy')
    result = googlenews.result()
    print(len(result),"WTF")
    news = None
    while len(news)!=1:
        try:
            index = randint(0, len(result) - 1)
            url = result[index]['link']
            snippet_title = result[index]['title']
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            news_snippet = get_summarized(article.text)
            json_result = nlp(news_snippet)
            break
        except ValueError as e:
            print(e,news_snippet)
            continue

    # news_snippet = news_snippet.replace("\n", ". ")
    # news_snippet1 = article.summary
    # print(news_snippet, '-----', news_snippet1, sep='\n')
    return news_snippet, snippet_title


def get_summarized(text):
    summary = None
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 10)
    combined = ''
    for sentence in summary:
        combined += str(sentence) + ' '
    summary = combined
    return summary


def get_summarized_content(news):
    summaries = []
    for n in range(1):
        parser = PlaintextParser.from_string(news, Tokenizer('english'))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 5)
        combined = ''
        for sentence in summary:
            combined += str(sentence) + ' '
        summaries.append(combined)
    return summaries


def get_snippet():
    try:
        snippet_text, snippet_topic = get_random_news()
    except:
        return get_snippet()

    new_snippet = Snippet.objects.create(title=snippet_topic, content=snippet_text)
    new_snippet.save()
    return new_snippet
