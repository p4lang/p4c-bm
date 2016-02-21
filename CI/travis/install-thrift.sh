#!/bin/sh
set -e
# check to see if thrift folder is empty
if [ ! -d "$HOME/thrift/lib" ]; then
    wget http://archive.apache.org/dist/thrift/0.9.2/thrift-0.9.2.tar.gz;
    tar -xzvf thrift-0.9.2.tar.gz;
    cd thrift-0.9.2;
    ./configure --prefix=$HOME/thrift --with-cpp=yes --with-python=no --with-c_glib=no --with-java=no --with-ruby=no --with-erlang=no --with-go=no --with-nodejs=no;
    make && make install;
    cd ..;
else
    echo 'Using cached thrift directory.'
fi
