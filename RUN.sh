
echo "[artifice] configuring logging"
echo "" > flask.log
echo "" > celery.log
echo "[artifice] starting celery service"
python3 -m artifice.scraper.background &
echo "[artifice] starting flask service"
echo "TO KILL AN ORPHANED FLASK SERVER:     kill -9 \`lsof -i:8080 -t\`"
python3 -m artifice.scraper.foreground
