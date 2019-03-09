#!/bin/bash
function usage {
    echo "Usage: [-c] [-h]"
    echo " "
    echo "Optional:"
    echo "-c         : create and install venv"
    echo "-h         : please run the following command/s - extending this script is easy.."
}

## Configure variables and set stage
for var in "$@"
do
    case "$var" in
        -c* | --create_venv*)
            echo "Creating virtual environment called venv"
            virtualenv ./venv/ -p python3.7
            source ./venv/bin/activate
            echo "Updating pip"
            pip install -U pip
            echo "Install environment"
            pip install -e .
            ;;
        -h* | -help*)
            usage
            exit 1
    esac
done

if [[ $# = 0 ]]; then
    usage
    exit 1
fi
