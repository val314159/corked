. .v/bin/activate # load python environment

. ~/.email # put your user mail settings here
# examples of mail settings would be:
#export EMAIL_SENDER='robot@nowhere.net'
#export SMTP_URL='starttls://USERNAME:PASSWORD@smtp.gmail.com:587'

export PYTHONUNBUFFERED=1
export DBNAME=authsvr.db

run() {
  (cd authsvr ; python -m serve)
}

run_other() {
  (cd othersvr ; python -m SimpleHTTPServer)
}

$*
