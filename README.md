# Roni
A bunch of scripts for automating creation of the daily COVID-19 news Rona Report

# Usage

* Save any desired articles to Possible Articles with:
`python save_article.py "New York Times" http://nyt.com/thearticle`

* Copy all Possible Articles marked "Use" to Articles and delete possibles:
`python copy_possible_articles.py`

* Fetch daily stats from The Atlantic:
`python parser.py`

* Print out a test report to report.html:
`python report.py`

* Send out the report emails:
`python report.py 1`
