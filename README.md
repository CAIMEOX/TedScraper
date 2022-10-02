# TedScraper
Download Ted talks as markdown.

## Usage
Ted Scraper is a simple cli program, which requires Python installed.
```bash
python main.py [-h] {talk,page} ...
```
### Subcommand
#### talk
Download a single talk.
```bash
usage: 
python main.py talk [-h] [-u URL] [-l LANG [LANG ...]]
  -h, --help            show this help message and exit
  
  -u URL, --url URL     Link to a single talk
  
  -l LANG [LANG ...], --lang LANG [LANG ...]
                        Languages of transcripts
```

#### page
Download a list of talks.
```bash
usage: 
python main.py page [-h] [-l LANG [LANG ...]] [-u URL] [-p PAGE] [-m MAX]
                    [-n NUMBER]
  -h, --help            show this help message and exit
  -l LANG [LANG ...], --lang LANG [LANG ...]
                        Languages of transcripts
  -u URL, --url URL     Link to the talks page
  -p PAGE, --page PAGE  Page number of the talks list
  -m MAX, --max MAX     Maximum of talks
  -n NUMBER, --number NUMBER
                        Threads count
```

## Why markdown?
You can convert markdown into many other formats by pandoc.