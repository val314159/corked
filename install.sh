virtualenv .v
. env.sh
pip install bottle flask bottle-cork

(cd authsvr ; python populate.py)

echo '=== READY! ==='
