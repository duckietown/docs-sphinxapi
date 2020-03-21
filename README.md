# Duckietown ROS API docs

This container builds and combines the API docs for several Duckietown containers.

## Quickstart

The command 

    make run
    
will build the container and produce the output in `output-dir` in the current directory.

# Calling from scripts

You can run the code as follows:

    docker run -it --rm -v "DEST:/output" duckietown/docs-sphinxapi:daffy
    
where `DEST` is the absolute path to a directory where you want the output to appear.
 

## Adding a new repository


To add a new repository, edit the `repositories.txt` and `docs/source/index.rst` file. 
