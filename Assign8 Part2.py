from psychopy import core, event, visual, monitors
import numpy as np
import csv
import os
import json as json
import pandas as pd

#monitor specs
mon = monitors.Monitor('myMonitor', width=24.5, distance=60)
mon.setSizePix([1920,1080])
win = visual.Window(monitor=mon)

filename = 'subject1session1Nov2022CSV'
main_dir = os.getcwd()
data_dir = os.path.join(main_dir,'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
fullAddress = os.path.join(data_dir, filename)
print(fullAddress)

#blocks, trials, stims, and clocks
nBlocks=2
nTrials=4
my_text=visual.TextStim(win)
rt_clock = core.Clock()  # create a response time clock
cd_timer = core.CountdownTimer() #add countdown timer

#prefill lists for responses # but we are going to make it a dictionary in block loop

subjectresp = [[-1]*nTrials]*nBlocks
#sub_acc = [[-1]*nTrials]*nBlocks
prob = [[-1]*nTrials]*nBlocks
correctresp = [[-1]*nTrials]*nBlocks
#resp_time = [[-1]*nTrials]*nBlocks
blocks = [[0, 0, 0, 0], [1, 1, 1, 1]] 
trials = [[0, 1, 2, 3], [0, 1, 2, 3]] 




#create problems and solutions to show
math_problems = ['1+3=','1+1=','3-2=','4-1='] #write a list of simple arithmetic
solutions = [4,2,1,3] #write solutions
prob_sol = list(zip(math_problems,solutions))

for block in range(nBlocks):
    # create dictionary in block loop and use trial indexing
    session_info = {'sub_resp' : [], 'sub_acc' : [], 'corr_resp' : [], 'resp_time' : []}
    for trial in range(nTrials):
        #what problem will be shown and what is the correct response?
        prob[block][trial] = prob_sol[np.random.choice(4)]
        #everything gets appended to dictionary now
        session_info['corr_resp'].append(prob[block][trial][1])
        correctresp[block][trial] = prob[block][trial][1]
        
        rt_clock.reset()  # reset timing for every trial
        cd_timer.add(3) #add 3 seconds

        event.clearEvents(eventType='keyboard')  # reset keys for every trial
        
        count=-1 #for counting keys
        while cd_timer.getTime() > 0: #for 3 seconds

            my_text.text = prob[block][trial][0] #present the problem for that trial
            my_text.draw()
            win.flip()

            #collect keypresses after first flip
            keys = event.getKeys(keyList=['1','2','3','4','escape'])

            if keys:
                count=count+1 #count up the number of times a key is pressed

                if count == 0: #if this is the first time a key is pressed
                    #get RT for first response in that loop
                    session_info['resp_time'].append(rt_clock.getTime())
                    #get key for only the first response in that loop
                    session_info['sub_resp'].append(keys[0]) #remove from list
                    subjectresp[block][trial] = keys[0]

        #record subject accuracy
        #correct- remembers keys are saved as strings
        if subjectresp[block][trial] == str(correctresp[block][trial]):
            session_info['sub_acc'].append(1) #arbitrary number for accurate response
        #incorrect- remember keys are saved as strings              
        elif subjectresp[block][trial] != str(correctresp[block][trial]):
            session_info['sub_acc'].append(0) #arbitrary number for inaccurate response 
                                    #(should be something other than -1 to distinguish 
                                    #from non-responses)
                    
        #print results
        print('problem=', prob[block][trial], 'correct response=', 
              session_info['corr_resp'], 'subject response=',session_info['sub_resp'], 
              'subject accuracy=',session_info['sub_acc'], 'reaction time=',
              session_info['resp_time'])
    # save as JSON also
    filenameJSON = 'subject1session1Nov2022JSON'
    fullAddressJSON = os.path.join(data_dir, filenameJSON)
    with open(data_dir + '_block%i.txt'%block, 'w') as f:
        json.dump(session_info, f, indent=4)

win.close()

data_as_list = [prob, session_info['corr_resp'],session_info['resp_time'], session_info['sub_acc'], session_info['sub_resp']]
print(data_as_list)

# save dictionary as CSV
with open(fullAddress, mode ='w') as sub_data:
    data_writer = csv.writer(sub_data, delimiter=',')
    data_writer.writerow(data_as_list)

# now we read the json
df = pd.read_json(data_dir+'_block1.txt')
# take only accurate trials that had a response
valid_trials = df[(df['sub_acc'] == 1) & (df['sub_resp'] != 0)]
print(valid_trials)
print(valid_trials.mean())
    