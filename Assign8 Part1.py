#import
from psychopy import gui, visual, monitors, event, core

# set up monitor and window
mon = monitors.Monitor('myMonitor', width=24.5, distance=60)
mon.setSizePix([1920,1080])
win = visual.Window(monitor=mon)

# number of trials2121
nTrials=5
#trial text
trial_text=visual.TextStim(win)
# fixation cross
fix=visual.TextStim(win, text='+')


# trial loop
for trial in range(nTrials):
    
    # start collecting keys and assign to keys variable
    keys = event.getKeys(keyList=['1','2']) 
    # 211212 trial text aand assign current trial integer into text
    trial_text.text = "trial %i" %trial 
    
    # draw fixation cross
    fix.draw()
    win.flip()
    core.wait(2)
    
    # use clearEvents here to clear innaccurate keypresses
    event.clearEvents() 
    
    #print trial text
    trial_text.draw()
    win.flip()
    core.wait(1)
    
    if keys:
        sub_resp = keys[0]
        print(sub_resp)
    
    
win.close()