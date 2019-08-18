rm flask.log
python3 -m artifice.scraper.foreground --drop_tables 1 --loglevel ERROR --logfile flask.log --stdout 0
