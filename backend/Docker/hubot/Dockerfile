FROM alpine
MAINTAINER nasa9084
RUN apk --no-cache add nodejs &&\
    npm install -g npm &&\
    npm install -g yo generator-hubot hubot coffee-script &&\
    adduser -h bot -D bot
USER bot
WORKDIR /bot
RUN yes | yo hubot --owner="user" --description="No Description" --name="Hubot" --adapter=slack
CMD ["/bot/bin/hubot", "--adapter", "slack"]
