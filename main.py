import argparse
from datetime import datetime
from functools import reduce
import requests
import logging
from bs4 import BeautifulSoup
logging.basicConfig(format='%(asctime)s - %(message)s',
                    level=logging.INFO, datefmt='[%H:%M:%S]')


class Markdown:
    text = ''

    def title(self, t):
        self.text += '# %s\n' % t

    def doc(self, t):
        self.text += '%s' % '\n\n'.join(t)

    def newline(self):
        self.text += '\n'

    def subtitle(self, t):
        self.text += '### *%s*\n' % t.strip()


def getPageContent(url):
    ted_page = requests.get(url).content
    soup = BeautifulSoup(ted_page, "html.parser")
    media_message = soup.findAll("div", {"class": "media__message"})
    speakers = map(lambda a: a.findAll(
        "h4", {"class": "h12 talk-link__speaker"})[0].get_text(), media_message)
    links = map(lambda a: 'https://www.ted.com' +
                a.find_all(attrs={"data-ga-context": "talks"})[0]['href'], media_message)
    titles = map(lambda t: t.find_all(attrs={
                 "data-ga-context": "talks"})[0].get_text().replace('\n', ''), media_message)
    return list(zip(titles, speakers, links))


def isUselessMessage(a: str):
    return a.startswith('(') or a.startswith("（")


def getTranscript(url: str, lang="en"):
    url = url.split('?')[0] + '/transcript.json?language=' + lang
    j = requests.get(url).json()
    if 'status' in j and j['status'] == 404:
        return []
    return processJson(j)


def processJson(j):
    def r_cues(a): return reduce(lambda b, c: {
        'text': b['text'] + ' ' + c['text']},
        filter(lambda t: not isUselessMessage(t['text']), a['cues']),
        {"text": ""})

    para = filter(lambda a: len(a['text']) > 0, map(r_cues, j['paragraphs']))
    preview = map(lambda a: a['text'].replace('\n', ' '), list(para))
    return list(preview)


def convertMarkDown(raw):
    md = Markdown()
    md.title(raw[0])
    md.subtitle(raw[1])
    md.doc(raw[2])
    md.newline()
    return md.text


def getTitleAndAuthor(link):
    talk_page = requests.get(link).content
    soup = BeautifulSoup(talk_page, "html.parser")
    title = soup.find_all("h1", {
                          "class": "text-textPrimary-onLight font-light text-tui-2xl leading-tui-sm tracking-tui-tight md:text-tui-3xl md:tracking-tui-tightest lg:text-tui-4xl mr-5"})[0].get_text()
    author = soup.find_all("meta", {"name": "author"})[0]['content']
    return (title, author)


def processUnit(p, lang):
    logging.info('Downloading: %s : %s', p[1], p[0])
    trans = map(lambda x: "\n  " + "\n  ".join(x),
                zip(*map(lambda a: getTranscript(p[2], a), lang)))
    return convertMarkDown((p[0], p[1], trans))


def talk(url, lang):
    (title, author) = getTitleAndAuthor(url)
    f = open(title, 'w+')
    f.write(processUnit((title, author, url), lang))
    f.close()


def page(url, lang, page, max):
    pages = getPageContent('https://www.ted.com/talks?page=%s' %
                           (page or 1) if url is None else url)[:int(max)]
    fileName = 'Talks_%s.md' % str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    f = open(fileName, 'a+')
    f.write('\n'.join(map(lambda s: processUnit(s, lang), pages)))
    f.close()
    logging.info('Talks were saved to %s' % fileName)


def runCli():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='sub_parser')
    single_talk_parser = sub.add_parser('talk')
    single_talk_parser.add_argument(
        '-u', '--url', help='Link to a single talk')
    single_talk_parser.add_argument(
        '-l', '--lang', nargs='+', help='Languages of transcripts', default=['en'])
    page_parser = sub.add_parser('page')
    page_parser.add_argument('-l', '--lang', nargs='+',
                             help='Languages of transcripts', default=['en'])
    page_parser.add_argument('-u', '--url', help='Link to the talks page')
    page_parser.add_argument(
        '-p', '--page', help='Page number of the talks list')
    page_parser.add_argument(
        '-m', '--max', help="Maximum of talks"
    )
    args = vars(parser.parse_args())
    globals()[args.pop('sub_parser')](**args)


runCli()
