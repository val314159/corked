virtualenv .v
. env.sh
pip install git+https://github.com/val314159/bottle-cork.git
pip install flask
pip install gevent

(cd authsvr ; python populate.py)

echo '=== READY! ==='
