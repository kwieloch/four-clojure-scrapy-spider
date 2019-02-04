# four-clojure-scrapy-spider
Scrapy project for downloading 4clojure tasks and saving them as clojure.test files

## Use
The command:
```scrapy crawl 4clojure-login```
will ask for credential, and then save all the problems into the ```output``` directory. The elementary tasks will be marked as skipped,
and tasks with solutions that are not clojure forms will be marked to-fix.
