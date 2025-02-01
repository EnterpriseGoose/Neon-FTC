# This program is made to keep track of a team's progress throughout an FTC competition
# Most of it is hard-coded for my team (11248) because that made it a lot easier
# Find the event code here: https://ftc-events.firstinspires.org and paste it below:
EVENT_CODE = "USNJUCM5"

# Then just keep track of your stats!
# First line: color of prev = what your color was - match # - pts in that match
# Second line: curr - match # - wins/losses - current ranking
# Third/fourth lines: color of next = what your color is going to be; match # - teams competing in the match, color-coded
# Last line: team name & num

# That's all! ~EnterpriseGoose / Olive

import random
import time

import board
import displayio
import framebufferio
import rgbmatrix
import requests

# import requests
displayio.release_displays()

# bit_depth=1 is used here because we only use primary colors, and it makes
# the animation run a bit faster because RGBMatrix isn't taking over the CPU
# as often.
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=4,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
palette[2] = 0xFFFFFF
palette[3] = 0xFFFFFF

digitsBitmap = displayio.OnDiskBitmap("digits.bmp")
digitsRedBitmap = displayio.OnDiskBitmap("digits-red.bmp")
digitsBlueBitmap = displayio.OnDiskBitmap("digits-blue.bmp")

staticBitmap = displayio.OnDiskBitmap("static.bmp")

prevBlueBitmap = displayio.OnDiskBitmap("prev-blue.bmp")
prevRedBitmap = displayio.OnDiskBitmap("prev-red.bmp")
nextBlueBitmap = displayio.OnDiskBitmap("next-blue.bmp")
nextRedBitmap = displayio.OnDiskBitmap("next-red.bmp")


staticTile = displayio.TileGrid(staticBitmap, pixel_shader=staticBitmap.pixel_shader)

prevBlueTile = displayio.TileGrid(prevBlueBitmap, pixel_shader=prevBlueBitmap.pixel_shader)
prevRedTile = displayio.TileGrid(prevRedBitmap, pixel_shader=prevRedBitmap.pixel_shader)
nextBlueTile = displayio.TileGrid(nextBlueBitmap, pixel_shader=nextBlueBitmap.pixel_shader)
nextRedTile = displayio.TileGrid(nextRedBitmap, pixel_shader=nextRedBitmap.pixel_shader)


teamDigitsRedTile = displayio.TileGrid(digitsRedBitmap, pixel_shader=digitsRedBitmap.pixel_shader, tile_width=4, tile_height=6, width=5, height=2)
teamDigitsBlueTile = displayio.TileGrid(digitsBlueBitmap, pixel_shader=digitsBlueBitmap.pixel_shader, tile_width=4, tile_height=6, width=5, height=2)

teamScoreRedTile = displayio.TileGrid(digitsRedBitmap, pixel_shader=digitsRedBitmap.pixel_shader, tile_width=4, tile_height=6, width=3, height=1)
teamScoreBlueTile = displayio.TileGrid(digitsBlueBitmap, pixel_shader=digitsBlueBitmap.pixel_shader, tile_width=4, tile_height=6, width=3, height=1)

prevMatchNumTile = displayio.TileGrid(digitsBitmap, pixel_shader=digitsBitmap.pixel_shader, tile_width=4, tile_height=6, width=2, height=1)
nextMatchNumTile = displayio.TileGrid(digitsBitmap, pixel_shader=digitsBitmap.pixel_shader, tile_width=4, tile_height=6, width=2, height=1)

currentMatchTile = displayio.TileGrid(digitsBitmap, pixel_shader=digitsBitmap.pixel_shader, tile_width=4, tile_height=6, width=2, height=1)
winsTile = displayio.TileGrid(digitsBitmap, pixel_shader=digitsBitmap.pixel_shader, tile_width=4, tile_height=6, width=1, height=1)
lossesTile = displayio.TileGrid(digitsBitmap, pixel_shader=digitsBitmap.pixel_shader, tile_width=4, tile_height=6, width=1, height=1)
rankingTile = displayio.TileGrid(digitsBitmap, pixel_shader=digitsBitmap.pixel_shader, tile_width=4, tile_height=6, width=2, height=1)

g1 = displayio.Group()
g1.append(staticTile)

g1.append(currentMatchTile)
g1.append(teamDigitsRedTile)
g1.append(teamDigitsBlueTile)
g1.append(teamScoreRedTile)
g1.append(teamScoreBlueTile)
g1.append(prevMatchNumTile)
g1.append(nextMatchNumTile)
g1.append(winsTile)
g1.append(lossesTile)
g1.append(prevBlueTile)
g1.append(prevRedTile)
g1.append(nextBlueTile)
g1.append(nextRedTile)
g1.append(rankingTile)

teamDigitsRedTile.x = 19
teamDigitsRedTile.y = 14
teamDigitsBlueTile.x = 45
teamDigitsBlueTile.y = 14

teamScoreRedTile.x = 31
teamScoreBlueTile.x = 48

prevMatchNumTile.x = 19
currentMatchTile. x = 19
currentMatchTile.y = 7
nextMatchNumTile.y = 20

winsTile.x = 31
winsTile.y = 7
lossesTile.x = 39
lossesTile.y = 7

nextBlueTile.y = 14
nextRedTile.y = 14

rankingTile.x = 52
rankingTile.y = 7

display.root_group = g1

def dispNumber(number, digits, tile, y = 0):
    number = int(number)
    for i in range(digits):
        if number == 0 and i > 0:
            tile[digits - 1 - i, y] = 10
        else:
            tile[digits - 1 - i, y] = number % 10
        number = int(number / 10)

currentMatch = 0
prevMatch = 5
nextMatch = 19
redTeams = [955, 9853]
blueTeams = [11248, 19252]
redScore = 123
blueScore = 59
prevMatchTeam = "red"
wins = 1
losses = 3
ranking = 36


while True:
    rankingsReq = requests.get('https://ftc-api.firstinspires.org/v2.0/2024/rankings/' + EVENT_CODE + '?teamNumber=11248', auth=('enterprisegoose', '79C48FC7-CEFB-41DB-970E-49E08D7723C1'))
    rankingsInfo = rankingsReq.json()["rankings"][0]
    ranking = rankingsInfo["rank"]

    eventReq = requests.get("https://ftc-api.firstinspires.org/v2.0/2024/schedule/" + EVENT_CODE + "/qual/hybrid", auth=('enterprisegoose', '79C48FC7-CEFB-41DB-970E-49E08D7723C1'))
    eventInfo = eventReq.json()["schedule"]

    prevMatchInfo = {"matchNumber": 0, "scoreRedFinal": 0, "scoreBlueFinal": 0}
    nextMatchSet = False
    wins = 0
    losses = 0
    for match in eventInfo:
        matchRedTeams = []
        matchBlueTeams = []
        for team in match["teams"]:
            if "Blue" in team["station"]:
                matchBlueTeams.append(team["displayTeamNumber"])
            else:
                matchRedTeams.append(team["displayTeamNumber"])
        if "11248" not in matchRedTeams and "11248" not in matchBlueTeams:
            continue
        if match["matchNumber"] < currentMatch:
            prevMatchInfo = match
            if "11248" in matchBlueTeams:
                if match["blueWins"]:
                    wins += 1
                elif match["redWins"]:
                    losses += 1
            else:
                if match["blueWins"]:
                    losses += 1
                elif match["redWins"]:
                    wins += 1
        if match["matchNumber"] > currentMatch and not nextMatchSet:
            blueTeams = matchBlueTeams
            redTeams = matchRedTeams
            nextMatch = match["matchNumber"]
            nextMatchSet = True
        

    prevMatch = prevMatchInfo["matchNumber"]
    redScore = prevMatchInfo["scoreRedFinal"]
    blueScore = prevMatchInfo["scoreBlueFinal"]
    
    dispNumber(currentMatch, 2, currentMatchTile)
    dispNumber(prevMatch, 2, prevMatchNumTile)
    dispNumber(nextMatch, 2, nextMatchNumTile)

    dispNumber(redScore, 3, teamScoreRedTile)
    dispNumber(blueScore, 3, teamScoreBlueTile)

    dispNumber(redTeams[0], 5, teamDigitsRedTile, 0)
    dispNumber(redTeams[1], 5, teamDigitsRedTile, 1)
    dispNumber(blueTeams[0], 5, teamDigitsBlueTile, 0)
    dispNumber(blueTeams[1], 5, teamDigitsBlueTile, 1)

    dispNumber(wins, 1, winsTile)
    dispNumber(losses, 1, lossesTile)
    dispNumber(ranking, 2, rankingTile)

    if (prevMatchTeam == "blue"):
        prevBlueTile.hidden = False
        prevRedTile.hidden = True
    else:
        prevBlueTile.hidden = True
        prevRedTile.hidden = False

    if 11248 in blueTeams:
        nextBlueTile.hidden = False
        nextRedTile.hidden = True
    else:
        nextBlueTile.hidden = True
        nextRedTile.hidden = False
        
    display.refresh()

    currentMatch += 1
    time.sleep(3)