# Description
#   container name
#
# Config
#  HUBOT_CONTAINER_NAME
#
# Commands
#   hubot tell your name
#
# Notes
#   Only for hubot_service
#
# Author
#   nasa9084

module.exports = (robot) ->
    robot.respond /tell your name/, (msg) ->
        env = process.env.HUBOT_CONTAINER_NAME.split(':')
        hubotContainer = env[0]
        redisContainer = env[1]
        msg.send """My name is #{hubotContainer}.
        My brain name is #{redisContainer}."""
