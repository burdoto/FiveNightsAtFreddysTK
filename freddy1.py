#!/usr/bin/wish

versionNr = "0.9.1"

#wm title . "Five Nights at Freddy's - Version $versionNr - Entwicklermodus"
#wm minsize . 700 350
#wm maxsize . 700 350

def init(rl):
    global chars, charNames, posList, door, poster, dead, open, blocked, powerLeft, powerUsage, pos, doorBlockDeath, activeCam, camList, camIDs, camActive, goldenFreddy, useImage, light, ai

    chars = ["freddy", "bonnie", "chica", "foxy", "golden"]
    charNames = ["Freddy", "Bonnie", "Chica", "Foxy", "Golden Freddy"]

    posList["freddy"] = ["stage", "dining_room", "restrooms", "kitchen", "east_hall", "east_corner", "none", "office"]
    posList["bonnie"] = ["stage", "dining_room", "backstage", "west_hall", "supply", "west_corner", "left_door", "office"]
    posList["chica"] = ["stage", "dining_room", "restrooms", "kitchen", "east_hall", "east_corner", "right_door", "office"]
    posList["foxy"] = ["cove_back", "cove_peek", "cove_run", "west_hall", "office"]
    posList["golden"] = ["none", "office"]

    for char in chars:
        pos[char] = 0
        ai[char] = 0

    goldenFreddy = "false"

    camList = ["stage", "dining_room", "cove", "west_hall", "west_corner", "supply", "east_hall", "east_corner", "backstage", "kitchen", "restrooms"]
    camIDs = ["1A", "1B", "1C", "2A", "2B", "3", "4A", "4B", "5", "6", "7"]
    activeCam = 0
    camActive = "false"

    useImage["office.dark"] = "img/office/office.dark-state1.png"
    useImage["cam.west_hall"] = "img/cameras/west_hall/light_on.png"

    dead = "false"
    doorBlockDeath = "false"

    for side in ["left", "right"]:
        door[side] = "clear"
        light[side] = "off"
        open[side] = "true"
        blocked[side] = "false"

    poster["west_corner"] = "lets_party"

    powerLeft = 100
    powerUsage = 1

    if (rl == "true"):
        reload()
    else:
        update()
    pass

def trigger(char):
    global chars, charNames, posList, door ,poster ,dead ,open ,blocked ,powerLeft ,powerUsage ,pos ,doorBlockDeath ,activeCam ,camList ,camIDs ,camActive ,goldenFreddy ,useImage ,light

    if (not char == "golden") and (not char == "foxy"):
        if pos[char] < (len(posList[char]) - 2):
            thisPos = pos[char]
            nextPos = thisPos + 1
        else:
            if (char == "freddy") and (pos[char] == (len(posList[char]) - 2)):
                thisPos = pos[char]
                nextPos = pos[char] + 1
                dead = "true"
        } elseif {$char == "bonnie" && $pos($char) >= 5} {
            if {$pos($char) == 5 && $door(left) == "clear"} {
                set door(left) "bonnie"
                set thisPos 5
                set nextPos 6
            } elseif {$pos($char) == 6 && $door(left) == "bonnie"} {
                if {$open(left) == "true"} {
                    set blocked(left) true
                    set thisPos 6
                    set nextPos 6
                } elseif {$open(left) == "false"} {
                    set thisPos 6
                    set nextPos [random 1 3]
                }
            }
        } elseif {$char == "chica" && $pos($char) >= 5} {
            if {$pos($char) == 5 && $door(right) == "clear"} {
                set door(right) "chica"
                set thisPos 5
                set nextPos 6
            } elseif {$pos($char) == 6 && $door(right) == "chica"} {
                if {$open(right) == "true"} {
                    set blocked(right) true
                    set thisPos 6
                    set nextPos 6
                } elseif {$open(right) == "false"} {
                    set thisPos 6
                    set nextPos [random 1 2]
                }
            }
        }
    } elseif {$char == "golden"} {
        set poster(west_corner) "golden_freddy"
        set pos(golden) 1
        set nextPos 1
    } elseif {$char == "foxy"} {
        if {$pos(foxy) == 4} {
            set thisPos $pos(foxy)
            set nextPos 0
        } else {
            set thisPos $pos(foxy)
            set nextPos [expr $pos($char) + 1]
        }
    }

    set pos($char) $nextPos

    if {[lindex $posList(bonnie) $pos(bonnie)] == "left_door"} {
        set door(left) "bonnie"
    } else {
        set door(left) "clear"
    }

    if {[lindex $posList(chica) $pos(chica)] == "right_door"} {
        set door(right) "chica"
    } else {
        set door(right) "clear"
    }
}

proc camera { } {
    global chars charNames posList door poster dead open blocked powerLeft powerUsage pos doorBlockDeath activeCam camList camIDs camActive goldenFreddy useImage light

    if {$camActive == false} {
        set camActive true
        .cam configure -text "Kamera AUS" -bg red

        set goldenTrigger [random 1 9999999]
#		set goldenTrigger 3754
        .info4 configure -text "Nummer: $goldenTrigger"
        if {$goldenTrigger == 3754} {
            trigger golden
            set goldenFreddy true
        }
    } elseif {$camActive == true} {
        set camActive false
        .cam configure -text "Kamera AN" -bg green
    }
}

proc doorToggle { side } {
    global chars charNames posList door poster dead open blocked powerLeft powerUsage pos doorBlockDeath activeCam camList camIDs camActive goldenFreddy useImage light

    if {$camActive == "false"} {
        if {$open($side) == true && $blocked($side) == false} {
            set open($side) false
            .$side\Toggle configure -bg green
        } elseif {$open($side) == false} {
            set open($side) true
            .$side\Toggle configure -bg red
        }
    }
}

proc lightToggle { side } {
    global chars charNames posList door poster dead open blocked powerLeft powerUsage pos doorBlockDeath activeCam camList camIDs camActive goldenFreddy useImage light

#	if {$camActive == "false"} {
        if {$light($side) == on} {
            set light($side) off
            .$side\Light configure -bg green -text "Licht $side\:$light($side)"
        } elseif {$light($side) == off} {
            set light($side) on
            .$side\Light configure -bg red -text "Licht $side\:\n$light($side)"
        }

        if {$side == "left"} {
            if {$light(right) == "on"} {
                set light(right) off
                .rightLight configure -bg green -text "Licht right:$light(right)"
            }
        }
        if {$side == "right"} {
            if {$light(left) == "on"} {
                set light(left) off
                .leftLight configure -bg green -text "Licht left:$light(left)"
            }
        }
#	}
}

proc random { from to } {
    set random [expr ( [clock clicks] % ( $to - $from ) ) + $from]

    if {$random > $to || $random < $from} {
        random $from $to
    } elseif {$random <= $to && $random >= $from} {
        return $random
    }
}

proc processImages { } {
    global chars charNames posList door poster dead open blocked powerLeft powerUsage pos doorBlockDeath activeCam camList camIDs camActive goldenFreddy useImage light

# Image Specify Block
    if {$pos(bonnie) == 0 && $pos(chica) == 0 && $pos(freddy) == 0} { # STAGE
        if {[random 1 100] >= "5"} {
            set useImage(cam.stage) "img/cameras/stage/b,c,f-normal.png"
        } else {
            set useImage(cam.stage) "img/cameras/stage/b,c,f-extra.png"
        }
    } elseif {$pos(bonnie) != 0 && $pos(chica) == 0 && $pos(freddy) == 0} {
        set useImage(cam.stage) "img/cameras/stage/c,f-normal.png"
    } elseif {$pos(bonnie) == 0 && $pos(chica) != 0 && $pos(freddy) == 0} {
        set useImage(cam.stage) "img/cameras/stage/b,f-normal.png"
    } elseif {$pos(bonnie) != 0 && $pos(chica) != 0 && $pos(freddy) == 0} {
        if {[random 1 100] >= "5"} {
            set useImage(cam.stage) "img/cameras/stage/f-normal.png"
        } else {
            set useImage(cam.stage) "img/cameras/stage/f-extra.png"
        }
    } elseif {$pos(bonnie) != 0 && $pos(chica) != 0 && $pos(freddy) != 0} {
        set useImage(cam.stage) "img/cameras/stage/-normal.png"
    }

    if {$pos(bonnie) != 1 && $pos(chica) != 1 && $pos(freddy) != 1} { # DINING_ROOM
        set useImage(cam.dining_room) "img/cameras/dining_room/empty-1.png"
    } elseif {$pos(bonnie) == 1 && $pos(chica) != 1 && $pos(freddy) != 1} {
        if {[random 1 100] >= 25} {
            set useImage(cam.dining_room) "img/cameras/dining_room/bonnie-1.png"
        } else {
            set useImage(cam.dining_room) "img/cameras/dining_room/bonnie-2.png"
        }
    } elseif {$pos(chica) != 1 && $pos(freddy) == 1} {
        set useImage(cam.dining_room) "img/cameras/dining_room/freddy-1.png"
    } elseif {$pos(chica) == 1} {
        if {[random 1 100] >= 25} {
            set useImage(cam.dining_room) "img/cameras/dining_room/chica-1.png"
        } else {
            set useImage(cam.dining_room) "img/cameras/dining_room/chica-2.png"
        }
    }

    if {$pos(foxy) == 0} { # PIRATE_COVE
        set useImage(cam.cove) "img/cameras/pirate_cove/state1.png"
    } elseif {$pos(foxy) == 1} {
        set useImage(cam.cove) "img/cameras/pirate_cove/state2.png"
    } elseif {$pos(foxy) == 2} {
        set useImage(cam.cove) "img/cameras/pirate_cove/state3.png"
    } elseif {$pos(foxy) >= 3} {
        set useImage(cam.cove) "img/cameras/pirate_cove/state4.png"
    }

    if {$pos(bonnie) != 3 && $pos(foxy) != 3} { # WEST_HALL
        if {$useImage(cam.west_hall) == "img/cameras/west_hall/light_on.png"} {
            set useImage(cam.west_hall) "img/cameras/west_hall/light_off.png"
        } elseif {$useImage(cam.west_hall) == "img/cameras/west_hall/light_off.png"} {
            set useImage(cam.west_hall) "img/cameras/west_hall/light_on.png"
        }
    } elseif {$pos(bonnie) == 3 && $pos(foxy) != 3} {
        set useImage(cam.west_hall) "img/cameras/west_hall/bonnie.png"
    } elseif {$pos(foxy) == 3} {
        set useImage(cam.west_hall) "img/cameras/west_hall/foxy_run/foxy_run-full.gif"
    }

    if {$pos(bonnie) != 5} { # WEST_CORNER
        if {$poster(west_corner) == "golden_freddy"} {
            set useImage(cam.west_corner) "img/cameras/west_corner/normal-golden_freddy.png"
        } elseif {$poster(west_corner) == "lets_party"} {
            if {[random 1 100] >= "5"} {
                set useImage(cam.west_corner) "img/cameras/west_corner/normal-freddy1.png"
            } else {
                set useImage(cam.west_corner) "img/cameras/west_corner/normal-freddy2.png"
            }
        }
    } elseif {$pos(bonnie) == 5} {
#		if {$ai(bonnie) >= "10"}
        set useImage(cam.west_corner) "img/cameras/west_corner/bonnie-chill.png"
    }

    if {$pos(bonnie) != 4} { # SUPPLY
        set useImage(cam.supply) "img/cameras/backroom/empty.png"
    } elseif {$pos(bonnie) == 4} {
        set useImage(cam.supply) "img/cameras/backroom/bonnie.png"
    }

    if {$pos(chica) != 4 && $pos(freddy) != 4} { # EAST_HALL
        set thisRandom [random 1 99]
        if {$thisRandom >= 7 && $thisRandom <= 93} {
            set useImage(cam.east_hall) "img/cameras/east_hall/empty-state1.png"
        } elseif {$thisRandom < 7} {
            set useImage(cam.east_hall) "img/cameras/east_hall/empty-state2.png"
        } elseif {$thisRandom > 93} {
            set useImage(cam.east_hall) "img/cameras/east_hall/empty-state3.png"
        }
    } elseif {$pos(chica) == 4 && $pos(freddy) != 4} {
        set useImage(cam.east_hall) "img/cameras/east_hall/chica.png"
    } elseif {$pos(freddy) == 4} {
        set useImage(cam.east_hall) "img/cameras/east_hall/freddy.png"
    }

    if {$pos(chica) != 5 && $pos(freddy) != 5} { # EAST_CORNER
        set thisRandom [random 1 100]
        if {$thisRandom > 0 && $thisRandom <= 25} {
            set useImage(cam.east_corner) "img/cameras/east_corner/empty-state1.png"
        } elseif {$thisRandom > 25 && $thisRandom <= 50} {
            set useImage(cam.east_corner) "img/cameras/east_corner/empty-state2.png"
        } elseif {$thisRandom > 50 && $thisRandom <= 75} {
            set useImage(cam.east_corner) "img/cameras/east_corner/empty-state3.png"
        } elseif {$thisRandom > 75 && $thisRandom <= 100} {
            set useImage(cam.east_corner) "img/cameras/east_corner/empty-state4.png"
        }
    } elseif {$pos(chica) == 5 && $pos(freddy) != 5} {
#		if {$ai(chica) >= 10}
        set useImage(cam.east_corner) "img/cameras/east_corner/chica-chill.png"
    } elseif {$pos(freddy) == 5} {
        set useImage(cam.east_corner) "img/cameras/east_corner/freddy.png"
    }

    if {$pos(bonnie) != 2} { # BACKSTAGE
        if {[random 1 100] >= 5} {
            set useImage(cam.backstage) "img/cameras/parts_room/empty-state1.png"
        } else {
            set useImage(cam.backstage) "img/cameras/parts_room/empty-state2.png"
        }
    } elseif {$pos(bonnie) == 2} {
        if {[random 1 100] >= 15} {
            set useImage(cam.backstage) "img/cameras/parts_room/bonnie-state1.png"
        } else {
            set useImage(cam.backstage) "img/cameras/parts_room/bonnie-state2.png"
        }
    }

    if {$pos(chica) != 2 && $pos(freddy) != 2} { # TOILETS
        set useImage(cam.restrooms) "img/cameras/toilets/empty-state1.png"
    } elseif {$pos(chica) == 2 && $pos(freddy) != 2} {
        if {[random 1 100] >= 50} {
            set useImage(cam.restrooms) "img/cameras/toilets/chica-state1.png"
        } else {
            set useImage(cam.restrooms) "img/cameras/toilets/chica-state2.png"
        }
    } elseif {$pos(freddy) == 2} {
        set useImage(cam.restrooms) "img/cameras/toilets/freddy-state1.png"
    }

    set useImage(office.lightLeft) "img/office/office.left-state1.png"
    set useImage(office.lightLeftBonnie) "img/office/office.bonnie-state1.png"
    set useImage(office.lightRight) "img/office/office.right-state1.png"
    set useImage(office.lightRightChica) "img/office/office.chica-state1.png"

# Image Choose Block
    if {$camActive == "false" && $light(left) == "off" && $light(right) == "off"} {
        set nowVisible $useImage(office.dark)
    } elseif {$camActive == "false" && $light(left) == "on" && $light(right) == "off"} {
        if {$pos(bonnie) == 6} {
            set nowVisible $useImage(office.lightLeftBonnie)
        } else {
            set nowVisible $useImage(office.lightLeft)
        }
    } elseif {$camActive == "false" && $light(left) == "off" && $light(right) == "on"} {
        if {$pos(chica) == 6} {
            set nowVisible $useImage(office.lightRightChica)
        } else {
            set nowVisible $useImage(office.lightRight)
        }
    } elseif {$camActive == "true"} {
        switch $activeCam {
            "0" {
                set nowVisible $useImage(cam.stage)
            } "1" {
                set nowVisible $useImage(cam.dining_room)
            } "2" {
                set nowVisible $useImage(cam.cove)
            } "3" {
                set nowVisible $useImage(cam.west_hall)
            } "4" {
                set nowVisible $useImage(cam.west_corner)
            } "5" {
                set nowVisible $useImage(cam.supply)
            } "6" {
                set nowVisible $useImage(cam.east_hall)
            } "7" {
                set nowVisible $useImage(cam.east_corner)
            } "8" {
                set nowVisible $useImage(cam.backstage)
            } "9" {
                set nowVisible $useImage(cam.kitchen)
            } "10" {
                set nowVisible $useImage(cam.restrooms)
            }
        }
    }

    set imageInfo [image create photo]
    $imageInfo read "$nowVisible"
    .s.a create image 800 360 -image $imageInfo
}

proc reload { } {
    global chars charNames posList door poster dead open blocked powerLeft powerUsage pos doorBlockDeath activeCam camList camIDs camActive goldenFreddy useImage light ai

# AI Processing Block
    for {set i 0} {$i < [llength $chars]} {incr i 1} {
        set thisCharName [lindex $chars $i]

        if {[random 1 40] < $ai($thisCharName)} {
            trigger $thisCharName
        }
    }

    processImages

    if {$camActive == "true" && $light(left) == "on"} {
        lightToggle "left"
    }
    if {$camActive == "true" && $light(right) == "on"} {
        lightToggle "right"
    }

    set powerUsage 1
    if {$light(left) == on} { set powerUsage [expr $powerUsage + 1] }
    if {$light(right) == on} { set powerUsage [expr $powerUsage + 1] }
    if {$open(left) == false} { set powerUsage [expr $powerUsage + 1] }
    if {$open(right) == false} { set powerUsage [expr $powerUsage + 1] }
    if {$camActive == true} { set powerUsage [expr $powerUsage + 1] }

    switch $powerUsage {
        "1" { set powerLeft [expr $powerLeft - 0.104166667]
        } "2" { set powerLeft [expr $powerLeft - 0.208333333]
        } "3" { set powerLeft [expr $powerLeft - 0.3125]
        } "4" { set powerLeft [expr $powerLeft - 0.416666667]
        }
    }

    if {$powerLeft <= 0} {
        set dead true
    }

    if {$open(left) == true && $blocked(left) == true && $camActive == true} {
        set doorBlockDeath true
    }
    if {$open(right) == true && $blocked(right) == true && $camActive == true} {
        set doorBlockDeath true
    }

    if {$goldenFreddy == true && $camActive == true} {
        set doorBlockDeath true
    }

    for {set i 0} {$i < [llength $chars]} {incr i 1} {
        set thisChar [lindex $chars $i]
        set thisCharName [lindex $charNames $i]
        .$thisChar configure -text "$thisCharName\: [lindex $posList($thisChar) $pos($thisChar)]"
    }

    .doorLeft configure -text "State: $door(left)\nOpen: $open(left)\nBlocked: $blocked(left)"
    .doorRight configure -text "State: $door(right)\nOpen: $open(right)\nBlocked: $blocked(right)"
    .posterWestCorner configure -text "Golden Freddy-Poster:\n$poster(west_corner)"
    .dead configure -text "Tot: $dead"
    .powerLeft configure -text "Energie:\n$powerLeft" -relief groove
    .powerUsage configure -text "Verbrauch: $powerUsage" -relief groove
    .deadNext configure -text "doorBlockDeath: $doorBlockDeath"

    .imageArray configure -text "images:\n$useImage(cam.west_corner)"

    if {$dead == true || ( $doorBlockDeath == true && $camActive == false )} {
        set dead true

        .dead configure -text "Tot: $dead"
        .new configure -bg red
    } elseif {$dead == false} {
        after 1000 reload
    }
}

proc hud { } {
    global chars charNames posList door poster dead open blocked powerLeft powerUsage pos doorBlockDeath activeCam camList camIDs camActive goldenFreddy useImage light

    bind . <Escape> "exit"

    button .close -text "Beenden" -command "exit" -relief groove
    button .leftToggle -text "left" -command "doorToggle left" -bg red -relief groove
    button .rightToggle -text "right" -command "doorToggle right" -bg red -relief groove
    button .reload -text "Refresh" -command "reload" -relief groove
    button .new -text "Neu" -command "init doReload" -relief groove
    button .cam -text "Kamera AN" -command "camera" -bg green -relief groove

    button .leftLight -text "Licht\nlinks" -command "lightToggle left" -relief groove
    button .rightLight -text "Licht\nrechts" -command "lightToggle right" -relief groove

    button .useCam00 -command "set activeCam 0" -text "stage"
    button .useCam01 -command "set activeCam 1" -text "dining_room"
    button .useCam02 -command "set activeCam 2" -text "cove"
    button .useCam03 -command "set activeCam 3" -text "west_hall"
    button .useCam04 -command "set activeCam 4" -text "west_corner"
    button .useCam05 -command "set activeCam 5" -text "supply"
    button .useCam06 -command "set activeCam 6" -text "east_hall"
    button .useCam07 -command "set activeCam 7" -text "east_corner"
    button .useCam08 -command "set activeCam 8" -text "backstage"
    button .useCam09 -command "set activeCam 9" -text "kitchen"
    button .useCam10 -command "set activeCam 10" -text "toilets"

#	stage dining_room cove west_hall west_corner supply east_hall east_corner backstage kitchen restrooms

    label .doorLeft -text $door(left) -relief groove
    label .doorRight -text $door(right) -relief groove
    label .posterWestCorner -text $poster(west_corner) -relief groove
    label .dead -text $dead -relief groove
    label .powerLeft -text "Energie: $powerLeft" -relief groove
    label .powerUsage -text "Verbrauch: $powerUsage" -relief groove
    label .deadNext -relief groove
    label .info4 -relief groove

    label .imageArray

    toplevel .s
    wm attributes .s -fullscreen 1
    wm attributes . -topmost 1
    canvas .s.a
    pack .s.a -expand 1 -fill both

    bind .s <Escape> "exit"

    for {set i 0} {$i < [llength $chars]} {incr i 1} {
        set thisChar [lindex $chars $i]
        label .$thisChar -text [lindex $posList($thisChar) 0]
    }

    for {set i 0} {$i < [llength $chars]} {incr i 1} {
        set thisCharName [lindex $charNames $i]
        set thisCharTRIG "[lindex $chars $i]\Trig"
        button .$thisCharTRIG -text "Trigger $thisCharName" -command "trigger [lindex $chars $i]" -relief groove
    }

    grid .new        .close       -         .leftToggle .rightToggle      -sticky news
    grid  x           x           x         .leftLight  .rightLight       -sticky news
    grid .freddy     .bonnie     .chica     .foxy       .golden           -sticky news
    grid .freddyTrig .bonnieTrig .chicaTrig .foxyTrig   .goldenTrig       -sticky news
    grid .reload     .doorLeft   .doorRight .dead       .posterWestCorner -sticky news
    grid .powerLeft  .powerUsage .deadNext  .info4      .cam              -sticky news
    grid .useCam00   .useCam01   .useCam02  .useCam03   .useCam04         -sticky news
    grid .useCam05   .useCam06   .useCam07  .useCam08   .useCam09         -sticky news
    grid .useCam10   -           -          -           -                 -sticky news

    for {set i 0} {$i < 5} {incr i 1} {
        grid rowconfigure    . $i -weight 1 -uniform a
        grid columnconfigure . $i -weight 1 -uniform a
    }
}

init noReload
hud
reload
