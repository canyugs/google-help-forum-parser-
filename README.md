# Google Help Forum Parser
Tested on Drive forum

## Requirement
* Python 3.6
* Selenium
* Chrome or PhantomJS driver in PATH

## Usage
Each scroll with load 30 topics, basically
and save detail to posts.result

```
$ python google_forum.py <scroll times>

# get 30 topics and detail
$ python google_forum.py 1 

# get 60 topics and detail
$ python google_forum.py 2
```


## TODO
* each topic with UUID
* same topic not save again
* database can increase
* Implement in JS?