virtualenv .v
. env.sh
pip install bottle flask bottle-cork
pip install gevent

(cd authsvr ; python populate.py)

echo '=== READY! ==='
