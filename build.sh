set -e
set -x
mkdir -p out
(cd out && cmake -G Ninja ..)
(cd out && ninja install)
