#!/bin/bash

SCRIPT_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd );
PROJECT_BASE=$(realpath ${SCRIPT_PATH}/..);

for ARG in ${@}; do
    case ${ARG} in
        --debug)
            pushd $PROJECT_BASE
            echo "Building debug..."
            docker build --pull --rm -f ./docker/Dockerfile --target=debug -t gitcuppajoe/fbposter:debug .
            popd
            exit 1
            ;;
        *)
            ;;
    esac
done

pushd $PROJECT_BASE
echo "Building release..."
docker build --pull --rm -f ./docker/Dockerfile --target=release -t gitcuppajoe/fbposter:latest .
popd