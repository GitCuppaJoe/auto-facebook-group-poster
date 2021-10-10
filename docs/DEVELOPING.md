# FBPoster Development

## Dev Environment

### Option 1: Docker
Docker is by far the simplest way to develop for this project. Because this Dockerfile is using [Multi-Stage Builds](https://docs.docker.com/develop/develop-images/multistage-build/), you can set the target of the image at build time to use the Debug Image. This provides many benefits like setting breakpoints, viewing request data and more, all inside of the docker container.

The development image requires:

1) [Visual Studio Code](https://code.visualstudio.com/)

2) [VSCode - Remote Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

To create a Developer Docker image, you can use the script found in `../devops/` directory.

Example:
```
# Build Developer Docker Image
devops/build_docker.sh --debug
```

Alternatively, you can run the docker build command yourself and select the target.

Example:
```
# Build Developer Docker Image
docker build --pull --rm -f ./docker/Dockerfile --target=debug -t gitcuppajoe/fbposter:debug .
```

# Debugging

## Using a VNC client

Because the base image is derived from the [Selenium](https://github.com/SeleniumHQ/docker-selenium) docker image, VNC is supported.

The VNC server is listening to port 5900, you can use a VNC client and connect to it. Feel free to map port 5900 to any free external port that you wish.

The internal 5900 port remains the same because that is the configured port for the VNC server running inside the container.

```
docker run -d --rm -it -e BOT_USERNAME="test@email.com" -e BOT_PASSWORD="securepassword" -e BOT_GROUP_ID="0000000000000000" -p 4444:4444/tcp -p 5000:5000/tcp -p 5900:5900/tcp -p 5678:5678/tcp gitcuppajoe/fbposter:debug
```

## Run Development Image with VNC Added

This project uses [noVNC](https://github.com/novnc/noVNC) to allow users the ability to inspect visually the container activity with their browser. This might come handy if you cannot install a VNC client on your machine. Port 7900 is used to start noVNC, so you will need to connect to that port with your browser.

```
docker run -d --rm -it -e BOT_USERNAME="test@email.com" -e BOT_PASSWORD="securepassword" -e BOT_GROUP_ID="0000000000000000" -p 4444:4444/tcp -p 5000:5000/tcp -p 7900:7900/tcp -p 5678:5678/tcp gitcuppajoe/fbposter:debug
```

## Run Development Image with Debugpy

The dev solution uses [debugpy](https://github.com/microsoft/debugpy) and listens on port 5678. VS Code will attach to this port when attempting to run the container from a debug image and launch the Flask application on port 5000. In order to accomplish this, you must create a `.vscode\launch.json` using [Launch Configuration](https://code.visualstudio.com/docs/editor/debugging#_launch-configurations) documentation.

``` json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/fb_poster/",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

Once you have this file, you will build the debug image, run the container from the image, then attach to the process.

### One Click Deployments

You can configure VSCode to build, run, attach, and launch the application using the dev/debug image with a single press of F5. I will not go into much detail about this, other that you can use tasks with the launch configuration mentioned above.

Launch Steps: 
1) Launch the application. 
2) Execute prelaunch tasks.

``` json
{
    // launch.json
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "preLaunchTask": "docker-run",
            "postDebugTask": "cleanup",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/fb_poster/",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

Docker build, run & cleanup. Note: you must modify the environment variables in this file that are being passed to docker.

``` json
{
    // tasks.json
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "docker-build",
            "type": "shell",
            "command": "docker build --pull --rm -f ./docker/Dockerfile --target=debug -t gitcuppajoe/fbposter:debug ."
        },
        {
            "label": "docker-run",
            "type": "shell",
            "command": "docker run -d --rm -it -e BOT_USERNAME='email@email.com' -e BOT_PASSWORD='superdupersecurepassword' -e BOT_GROUP_ID='groupid' -p 4444:4444/tcp -p 5000:5000/tcp -p 5900:5900/tcp -p 7900:7900/tcp -p 5678:5678/tcp --name fb_poster gitcuppajoe/fbposter:debug",
            "dependsOn":["docker-build"]
        },
        {
            "label": "docker-build-run",
            "dependsOn":["docker-run"]
        },
        {
            "label": "cleanup",
            "type": "shell",
            "command": "docker kill fb_poster"
        }
    ]
}
```

After creating the files above, you can safely and reliably press F5 to build, run and attach to debugpy in order to debug some python code!