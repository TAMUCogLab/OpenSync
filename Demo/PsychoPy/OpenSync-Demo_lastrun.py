#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.1.4),
    on October 24, 2021, at 23:20
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

import OpenSync
import time
print(OpenSync.OpenSync_path())

mouse_object = OpenSync.i_o.Mouse("OpenSyncMouse", clickable_object=True, position=True, click_type=True)
stimulus_object = OpenSync.markers.marker("StimMarker")



EEG = OpenSync.sensors.EEG()
EEG.OpenBCI_Cyton(daisy=True, port="COM3")

# For eyetracking you need to do calibration which starts automatically,
# Make sure Gazepoint Control is installed (https://www.gazept.com/downloads/)
Eye_Tracking = OpenSync.sensors.EyeTracking()
Eye_Tracking.Gazepoint(biometrics=True)

OpenSync.record_data("OpenSyncTest.xdf") #record data will wait 3 seconds to detect all the streams
time.sleep(5)


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.1.4'
expName = 'OpenSync-Demo'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\user\\Desktop\\Demo_Experiment\\Both\\OpenSync-Demo_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "initialization"
initializationClock = core.Clock()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='Focus on the center arrow and using mouse, indicate the direction of the center arrow.\nThis experiment includes only 4 trials. If you want to make it longer, click on "trials" loop and change nReps.\nTo start, press "Space" bar.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()

# Initialize components for Routine "fixation"
fixationClock = core.Clock()
fix = visual.TextStim(win=win, name='fix',
    text='+',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "stimulus"
stimulusClock = core.Clock()
flankers = visual.TextStim(win=win, name='flankers',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
Mouse = event.Mouse(win=win)
x, y = [None, None]
Mouse.mouseClock = core.Clock()
right_arrow = visual.Rect(
    win=win, name='right_arrow',
    width=(0.2, 0.1)[0], height=(0.2, 0.1)[1],
    ori=0.0, pos=(0.6, 0.4),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
left_arrow = visual.Rect(
    win=win, name='left_arrow',
    width=(0.2, 0.1)[0], height=(0.2, 0.1)[1],
    ori=0.0, pos=(-0.6, 0.4),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-3.0, interpolate=True)
right_arrow_text = visual.TextStim(win=win, name='right_arrow_text',
    text='->',
    font='Open Sans',
    pos=(0.6, 0.4), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
left_arrow_text = visual.TextStim(win=win, name='left_arrow_text',
    text='<-',
    font='Open Sans',
    pos=(-0.6, 0.4), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);

# Initialize components for Routine "finish_experiment"
finish_experimentClock = core.Clock()
finish_text = visual.TextStim(win=win, name='finish_text',
    text='"End of Experiment"',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "initialization"-------
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
initializationComponents = []
for thisComponent in initializationComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
initializationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "initialization"-------
while continueRoutine:
    # get current time
    t = initializationClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=initializationClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in initializationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "initialization"-------
for thisComponent in initializationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "initialization" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "instructions"-------
continueRoutine = True
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# keep track of which components have finished
instructionsComponents = [text, key_resp]
for thisComponent in instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instructionsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        text.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text.started', text.tStartRefresh)
thisExp.addData('text.stopped', text.tStopRefresh)
# check responses
if key_resp.keys in ['', [], None]:  # No response was made
    key_resp.keys = None
thisExp.addData('key_resp.keys',key_resp.keys)
if key_resp.keys != None:  # we had a response
    thisExp.addData('key_resp.rt', key_resp.rt)
thisExp.addData('key_resp.started', key_resp.tStartRefresh)
thisExp.addData('key_resp.stopped', key_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Stimulus\\\\trials.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "fixation"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationComponents = [fix]
    for thisComponent in fixationComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    fixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "fixation"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixationClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=fixationClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            fix.setAutoDraw(True)
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix, 'tStopRefresh')  # time at next scr refresh
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "fixation"-------
    for thisComponent in fixationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('fix.started', fix.tStartRefresh)
    trials.addData('fix.stopped', fix.tStopRefresh)
    
    # ------Prepare to start Routine "stimulus"-------
    continueRoutine = True
    routineTimer.add(3.000000)
    # update component parameters for each repeat
    flankers.setText(stim)
    # setup some python lists for storing info about the Mouse
    Mouse.x = []
    Mouse.y = []
    Mouse.leftButton = []
    Mouse.midButton = []
    Mouse.rightButton = []
    Mouse.time = []
    Mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    stimulus_object.stream_marker(condition)
    Mouse.setPos([0,-0.45])
    # keep track of which components have finished
    stimulusComponents = [flankers, Mouse, right_arrow, left_arrow, right_arrow_text, left_arrow_text]
    for thisComponent in stimulusComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    stimulusClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "stimulus"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = stimulusClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=stimulusClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *flankers* updates
        if flankers.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            flankers.frameNStart = frameN  # exact frame index
            flankers.tStart = t  # local t and not account for scr refresh
            flankers.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(flankers, 'tStartRefresh')  # time at next scr refresh
            flankers.setAutoDraw(True)
        if flankers.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > flankers.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                flankers.tStop = t  # not accounting for scr refresh
                flankers.frameNStop = frameN  # exact frame index
                win.timeOnFlip(flankers, 'tStopRefresh')  # time at next scr refresh
                flankers.setAutoDraw(False)
        # *Mouse* updates
        if Mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Mouse.frameNStart = frameN  # exact frame index
            Mouse.tStart = t  # local t and not account for scr refresh
            Mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Mouse, 'tStartRefresh')  # time at next scr refresh
            Mouse.status = STARTED
            prevButtonState = Mouse.getPressed()  # if button is down already this ISN'T a new click
        if Mouse.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Mouse.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                Mouse.tStop = t  # not accounting for scr refresh
                Mouse.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Mouse, 'tStopRefresh')  # time at next scr refresh
                Mouse.status = FINISHED
        if Mouse.status == STARTED:  # only update if started and not finished!
            x, y = Mouse.getPos()
            Mouse.x.append(x)
            Mouse.y.append(y)
            buttons = Mouse.getPressed()
            Mouse.leftButton.append(buttons[0])
            Mouse.midButton.append(buttons[1])
            Mouse.rightButton.append(buttons[2])
            Mouse.time.append(globalClock.getTime())
            buttons = Mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    for obj in [right_arrow, left_arrow]:
                        if obj.contains(Mouse):
                            gotValidClick = True
                            Mouse.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # *right_arrow* updates
        if right_arrow.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_arrow.frameNStart = frameN  # exact frame index
            right_arrow.tStart = t  # local t and not account for scr refresh
            right_arrow.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_arrow, 'tStartRefresh')  # time at next scr refresh
            right_arrow.setAutoDraw(True)
        if right_arrow.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > right_arrow.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                right_arrow.tStop = t  # not accounting for scr refresh
                right_arrow.frameNStop = frameN  # exact frame index
                win.timeOnFlip(right_arrow, 'tStopRefresh')  # time at next scr refresh
                right_arrow.setAutoDraw(False)
        
        # *left_arrow* updates
        if left_arrow.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_arrow.frameNStart = frameN  # exact frame index
            left_arrow.tStart = t  # local t and not account for scr refresh
            left_arrow.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_arrow, 'tStartRefresh')  # time at next scr refresh
            left_arrow.setAutoDraw(True)
        if left_arrow.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > left_arrow.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                left_arrow.tStop = t  # not accounting for scr refresh
                left_arrow.frameNStop = frameN  # exact frame index
                win.timeOnFlip(left_arrow, 'tStopRefresh')  # time at next scr refresh
                left_arrow.setAutoDraw(False)
        
        # *right_arrow_text* updates
        if right_arrow_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_arrow_text.frameNStart = frameN  # exact frame index
            right_arrow_text.tStart = t  # local t and not account for scr refresh
            right_arrow_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_arrow_text, 'tStartRefresh')  # time at next scr refresh
            right_arrow_text.setAutoDraw(True)
        if right_arrow_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > right_arrow_text.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                right_arrow_text.tStop = t  # not accounting for scr refresh
                right_arrow_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(right_arrow_text, 'tStopRefresh')  # time at next scr refresh
                right_arrow_text.setAutoDraw(False)
        
        # *left_arrow_text* updates
        if left_arrow_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_arrow_text.frameNStart = frameN  # exact frame index
            left_arrow_text.tStart = t  # local t and not account for scr refresh
            left_arrow_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_arrow_text, 'tStartRefresh')  # time at next scr refresh
            left_arrow_text.setAutoDraw(True)
        if left_arrow_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > left_arrow_text.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                left_arrow_text.tStop = t  # not accounting for scr refresh
                left_arrow_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(left_arrow_text, 'tStopRefresh')  # time at next scr refresh
                left_arrow_text.setAutoDraw(False)
        mouse_object.stream_pos(Mouse)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in stimulusComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "stimulus"-------
    for thisComponent in stimulusComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('flankers.started', flankers.tStartRefresh)
    trials.addData('flankers.stopped', flankers.tStopRefresh)
    # store data for trials (TrialHandler)
    trials.addData('Mouse.x', Mouse.x)
    trials.addData('Mouse.y', Mouse.y)
    trials.addData('Mouse.leftButton', Mouse.leftButton)
    trials.addData('Mouse.midButton', Mouse.midButton)
    trials.addData('Mouse.rightButton', Mouse.rightButton)
    trials.addData('Mouse.time', Mouse.time)
    trials.addData('Mouse.clicked_name', Mouse.clicked_name)
    trials.addData('Mouse.started', Mouse.tStart)
    trials.addData('Mouse.stopped', Mouse.tStop)
    trials.addData('right_arrow.started', right_arrow.tStartRefresh)
    trials.addData('right_arrow.stopped', right_arrow.tStopRefresh)
    trials.addData('left_arrow.started', left_arrow.tStartRefresh)
    trials.addData('left_arrow.stopped', left_arrow.tStopRefresh)
    trials.addData('right_arrow_text.started', right_arrow_text.tStartRefresh)
    trials.addData('right_arrow_text.stopped', right_arrow_text.tStopRefresh)
    trials.addData('left_arrow_text.started', left_arrow_text.tStartRefresh)
    trials.addData('left_arrow_text.stopped', left_arrow_text.tStopRefresh)
    mouse_object.stream_clicktype(Mouse)
    mouse_object.stream_click(Mouse)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'


# ------Prepare to start Routine "finish_experiment"-------
continueRoutine = True
routineTimer.add(2.000000)
# update component parameters for each repeat
# keep track of which components have finished
finish_experimentComponents = [finish_text]
for thisComponent in finish_experimentComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
finish_experimentClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "finish_experiment"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = finish_experimentClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=finish_experimentClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *finish_text* updates
    if finish_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        finish_text.frameNStart = frameN  # exact frame index
        finish_text.tStart = t  # local t and not account for scr refresh
        finish_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(finish_text, 'tStartRefresh')  # time at next scr refresh
        finish_text.setAutoDraw(True)
    if finish_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > finish_text.tStartRefresh + 2.0-frameTolerance:
            # keep track of stop time/frame for later
            finish_text.tStop = t  # not accounting for scr refresh
            finish_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(finish_text, 'tStopRefresh')  # time at next scr refresh
            finish_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in finish_experimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "finish_experiment"-------
for thisComponent in finish_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('finish_text.started', finish_text.tStartRefresh)
thisExp.addData('finish_text.stopped', finish_text.tStopRefresh)
OpenSync.stop_record()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
