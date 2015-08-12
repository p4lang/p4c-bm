#!/bin/sh
set -e
# check to see if nanomsg folder is empty
if [ ! -d "$HOME/nanomsg/lib" ]; then
    wget http://download.nanomsg.org/nanomsg-0.5-beta.tar.gz;
    tar -xzvf nanomsg-0.5-beta.tar.gz;
    cd nanomsg-0.5-beta;
    ./configure --prefix=$HOME/nanomsg;
    make && make install;
    cd ..;
else
    echo 'Using cached nanomsg directory.'
fi
