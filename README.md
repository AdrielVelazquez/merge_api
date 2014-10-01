On the root directory (where Makefile is)

#will setup virtualenv and pip requirements
make install

#will run unittests
make test

#Initiate virtualenv - after make install
. ./bin/activate 

#Run program
python server.py
