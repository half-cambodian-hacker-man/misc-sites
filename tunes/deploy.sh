rm -rf out/*
make
(cd out/ && git add -A . && git commit -m "[Auto] Deploy $(date)" && git push)
