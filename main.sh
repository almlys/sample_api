#!/usr/bin/env bash

# This script controls start, restart and stop of the sample API service.
#

function start() {

    # Start up and provision vagrant box
    vagrant up

}

function stop() {
    vagrant halt
}


function restart() {
    stop
    start
}

function destroy() {
    vagrant destroy -f
}

case $1 in
    start)
        echo "Starting Test..."
        start
    ;;
    stop)
        echo "Stopping Test..."
        stop
    ;;
    restart)
        echo "Restarting Test..."
        restart
    ;;
    destroy)
        echo "Destroy test..."
        destroy
    ;;
    *)
        echo "Please, call $0 with start/stop/restart/destroy, thanks"
esac

