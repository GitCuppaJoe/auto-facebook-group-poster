Auto-FacebookPoster - The Listener that Posts 
===========================

 Auto-FBPoster is a simple tool for posting directly to Facebook groups from incoming HTTP requests. This version is currently written to support [Tautulli](https://github.com/Tautulli/Tautulli) HTTP requests only.

Auto-FBPoster provides you with the following main functions:
- Easy configuration with docker
- Automatic posting to a particular Facebook group
- Live posting support provided by the [Selenium](https://github.com/SeleniumHQ/docker-selenium) base image
    - You can watch the bot in real time open the browser and post! S/O to Selenium!

Auto-FBPoster can be used to:
- Listen for incoming requests from various applications and post the content. Use Case: Plex Recently added Movie -> Tautulli Trigger -> Tautulli Notify -> Auto-FBPoster
- Retrofit the code to work with other applications.
- Post to other social media sites by inheriting from the SocialBot class. i.e. Instagram or Twitter

My Problem:

Tautulli currently can send out newsletters, discord notifications, pushover, pushbullet and various other mediums of notifications. One that cannot be accomplished is Facebook notifications. This is because Facebook removed the capability from their API. 

What I did:

In order to circumvent the problem, I learned how to write some Python over the weekend and used Selenium (past experience with C#) to "Robo" my postings when Tautulli notifies the bot.


Auto-FBPoster Flow:
1) Movie gets added to library that Plex scans
2) Plex gets notified that a movie was added
3) Plex notifies Tautulli
4) Tautulli gets triggered and notifies Auto-FacebookPoster that a movie was recently added
5) Tautulli notifies Auto-FBPoster
5) Auto-FBPoster receives notification and publishes the IMDB url sent from Tautulli to a Facebook group.
6) Users are notified from Facebook that a new movie has been released on Plex.

The Docker container is currently based off of the `selenium/chrome-standalone` Ubuntu focal image.

## Quick Start
DO NOT USE YOUR PERSONAL ACCOUNT OR ADMIN ACCOUNT IN CONJUNCTION WITH THIS TOOL. See [Special Considerations](#special-considerations) below for more information.

Start a Docker container with Chrome

``` bash
$ docker run -d --rm -it -e BOT_USERNAME="noadmin@email.com" -e BOT_PASSWORD="superDup3rSecUReP4ssword" -e BOT_GROUP_ID="4329004643848233" -p 4444:4444/tcp -p 5000:5000/tcp gitcuppajoe/fbposter:latest
```

Send a request using the `examples/example.request.http` file or construct your own HTTP request:

``` bash
$ curl -X POST http://localhost:5000
   -H 'Content-Type: application/json'
   -d '{"imdb_url":"https://www.imdb.com/title/tt0111161/"}'
```

## Dependencies

 - Python 3.x ([Install](https://www.python.org/downloads/))
 - To install requirements run 'python3 -m pip install -r requirements.txt' from the project root

Auto-FBPoster can be used for running many commands. You will need to ensure that the required dependencies for those commands are installed.

## Install and Run

It is recommended to run this application with Docker. Although, you can run this application by hand-rolling Selenium with the necessary Python dependencies, it isn't recommended.

```
docker run -d --rm -it \
    -e BOT_USERNAME=<fb username/email> \
    -e BOT_PASSWORD=<fb password> \
    -e BOT_GROUP_ID=<fb group id> \
    -e PUID=${PUID} \
    -e PGID=${PGID} \
    -p 4444:4444 \
    -p 5000:5000 \
    -p 5900:5900 \
    -p 7900:7900 \
    --name=fbposter \
    gitcuppajoe/fbposter:latest
```
&nbsp;
Please replace all user variables in the above command defined by <> with the correct values.

## Tautulli Configuration

Example text here...

## Special Considerations

Currently, the username and password are saved in the docker container as Environment variables. Users that have access to Environment variables will be able to see the U/N and Password in plain text.

It is best practice to create a "dummy" account that will manage your auto Facebook postings. This account should NOT be given admin rights to the Facebook group in case it is compromised. This allows the FB Group Administrator the ability to remove a malicious account.

This tool currently uses FLASK in development mode. With this consideration, do not use this tool with a Reverse Proxy. Keep this in your internal network at this time.

## Troubleshooting
"So uh... the tool is broken now. I get a no such element?"

Hah. Facebook updated their UI again! No sweat.

This project was a weekend of "I'm bored, let's do this." I may already have abandoned the project. Luckily, you can fix it! The bulk of the code is found in `fb_poster/socialbot/__init__.py`.

Log files can be found in `/app/logs/FBPostLogging.log` in the container.

## License and Contribution

This project contains libraries imported from external authors.
Please refer to the source of these libraries for more information on their respective licenses.

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) to learn how to contribute to Unmanic.