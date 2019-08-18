echo "[artifice] configuring logging"
echo "" > flask.log
echo "" > celery.log
echo "[artifice] starting celery service"
python3 -m artifice.scraper.background &
echo "[artifice] starting flask service"
python3 -m artifice.scraper.foreground --drop_tables 1 --loglevel ERROR --logfile flask.log --stdout 0 &
