#Christopher M. Church
#PhD Candidate, History Department
#Social Sciences Data Lab (D-Lab)
#University of California, Berkeley

#The following python code creates an EDGES table for characters in TOM STOPPARD's ROSENCRANTZ AND GUILDENSTERN ARE DEAD
#It is part of a network used in Gephi for Humanists, a manual on using network analysis in the humanities
#
#notes and known limitations:
#     WEIGHTING -- (1) the way the weights are calculated will exponentially increase the "weight" for speakers who talk frequently within the overlapping windows
#                      this is accounted for by using a "logarithmic" Force Atlas 2 layout
#                      while no real quantitative conclusions can be drawn from weighting in this way, 
#                      it nevertheless approximates the relative strength of the connections between the characters by showing the "size" of their conversations over the course of the play
#                  (2) another limitation is that this does not take stage directions into account
#                      since it sets weight based upon a mere counting of words, it also leaves out the quality, relative importance, or context of the words spoken
#
#Revision notes:
#     2013-11-14 - Code First Written
#
#*******************************************************************************************************

#set working path
path = "c:\\Users\\Church\\Desktop\\"


#*************
#****INPUT****
#*************

#initialize empty arrays -- note, we are separating the lines into acts, so that our window doesn't cross the boundaries of the acts
acts_raw = []
lines = []

#open our source text (Tom Stoppard's Rosencrantz and Guildenstern are Dead -- text transcript, cleaned and standardized using regex)
f = open(path+'stoppard_ros-guild-dead_full-text_cleaned.txt')

#read each line in the file
for line in f:
    line_lower = line.lower() #normalize it all to lowercase
    lines.append(line_lower) #add it to our lines array
    if "ACT" in line: #if the act has changed, append these lines to the acts array and clear the lines array
        acts_raw.append(lines)
        lines=[]
acts_raw.append(lines) #append the last bunch of lines to our nexted array
f.close() #close the opened filed


#**************
#**PROCESSING**
#**************

#import regex
import re

#create a regular expression for characters starting a line that end in a colon (i.e. "GUIL:" or "ROS:")
regex=re.compile("^\w+:")

#initialize an empty array of the acts with a nested tuple split between the speaker and the words spoken
acts_processed = []
for act in acts_raw: #go through each act individually, to keep ACT boundaries intact
    temp_line_array = [] #temporary array for holding the lines that we are working with in each act
    for line in act: #go through each line in the act
        match = regex.search(line) #match on the speaker (i.e. "GUIL:")
        if (match): #if a match, then
            speaker = match.group()[:-1] #assign the speakers's name (regex match minus the colon) to the first position of the tuple
            temp_line_array.append((speaker, line[match.end():])) #then assign the rest of the line to second position in the tuple
    acts_processed.append(temp_line_array) #push each list of tuples into our a new acts array
    
#**************
#****OUTPUT****
#**************

import itertools #import iterative tools to use the combinations method

f=open(path+'edges.txt','w') #open a file to store the edges information
f.write('SOURCE,TARGET,WEIGHT\n') #create a header

for act in acts_processed: #go through each act (again, to maintain the ACT boundaries)
    i=0 #counter set to zero
    j=len(act) #counter set the length of the act (how many lines)
    for i in range(j): #iterate i until j (i < length of the number of lines)
        window=[] #create a blank list that contains speakers from our sliding window
        total_words=0 #set our word counter to zero
        for x in act[i:i+5]: #for each tuple in the act sliced from i to i+5 (a sliding window of the speakers)
            words = x[1].split(' ') #explode the words into an array
            num_of_words = len(words) #count the words
            total_words += num_of_words #add the words to our total count
            window.append(x[0]) #add the speaker to the window list (list of the speakers inside our window)
        for subset in itertools.combinations(window, 2): #for each combination of speakers in the window, write the TARGET,SOURCE, and WEIGHT  -- note weight is defined by the number of words spoken during this window to approximate the depth of the character's connection (involvement)
            edge = subset[0] +',' + subset[1] + ',' + str(total_words) +'\n'
            f.write(edge) #write the edge
f.close() #close the output file