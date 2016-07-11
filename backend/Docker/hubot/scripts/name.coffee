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
        msg.send process.env.HUBOT_CONTAINER_NAME
