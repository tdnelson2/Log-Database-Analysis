# Log Analysis
I completed this project as part of the [Udacity Full Stack Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). It demonstrates my understanding of relational databases using PostgreSQL. It also demonstrates my understanding of the HTTP protocol because the data it deals with is a log from a fictional news website.

## Installation
* Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_2). NOTE: [Vagrant](https://www.vagrantup.com/downloads.html) is only compatible with version 5.2 and below.
* Install [Vagrant](https://www.vagrantup.com/downloads.html).
* Clone this repo to your machine.
* Download [the data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
* Unzip the downloaded file and you should have a file called `newsdata.sql`.
* Move `newsdata.sql` to the repo folder.
* In a bash shell (Terminal on macOS or [git bash](https://git-scm.com/downloads) on Windows) `cd` into the repo.
* Run `vagrant up` to launch the VM and install all dependencies. It will take a while because it has to download an entire OS!
* Run `vagrant ssh` to login to the linux environment.
* Once the linux environment has been loaded, change to the shared directory (`cd \vagrant`). This is the same directory as the repo only it's being shared inside the VM as well.
* Run `psql -d news -f newsdata.sql` to setup the database.
* Run `psql -d news -f log_analysis.sql` to setup the views.

## Use
* Inside the linux environment, `cd` to the shared directory (`cd \vagrant`).
* Run `python3 log_analysis.py`. The output should be the following:

```
Most popular three articles of all time:
"Candidate is jerk, alleges rival" — 338647 views
"Bears love berries, alleges bear" — 253801 views
"Bad things gone, say good people" — 170098 views

Most popular article authors of all time:
Ursula La Multa — 507594 views
Rudolf von Treppenwitz — 423457 views
Anonymous Contributor — 170098 views
Markoff Chaney — 84557 views

Days in which more than 1% of requests lead to errors:
July 17, 2016 —  2.3% errors
```

## Modular Use
* Launch the python3 shell.
* Import all functions from the module (`from log_analysis import *`)
* Get most popular articles of all time:

```
>>> topThreeArticles()
[('Candidate is jerk, alleges rival', 338647), ('Bears love berries, alleges bear', 253801), ('Bad things gone, say good people', 170098)]
```

* Get the most popular article authors:

```
>>> popularAuthors()
[('Ursula La Multa', Decimal('507594')), ('Rudolf von Treppenwitz', Decimal('423457')), ('Anonymous Contributor', Decimal('170098')), ('Markoff Chaney', Decimal('84557'))]
```

* Get the days in which more than 1% of requests lead to errors:

```
>>> requestErrorsExceedingOnePercent()
[('July 17, 2016', ' 2.3%')]
```
