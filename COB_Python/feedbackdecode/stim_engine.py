# -*- coding: utf-8 -*-
import numpy as np
import xipppy as xp
import feedbackdecode as fd
import time
import math
def stim_engine(SS):
    
    SS['active_stim'] = SS['stim_params'][np.logical_and(SS['stim_params'][:,7] == 1, # col 7: experimenter enabled
                                                         SS['stim_params'][:,8] == 1),0:7] # col 8: user enabled
    
    # for filesaving, set stim amp and freq for inactive chans to 0
    active_mask = np.zeros(SS['stim_freq_save'].size, dtype=bool)
    active_chan = np.array(SS['active_stim'][:,0], dtype=int)

    # chans are [0:95, 128:223, 256:351] inclusive, but idx are [0:95, 96:191, 192:287] inclusive
    active_chan[(active_chan > 95) & (active_chan <= 223) ] -= 32 # subtract for USEA #2
    active_chan[(active_chan > 256) & (active_chan <= 351) ] -= 64 # subtract for USEA #3
    active_mask[active_chan] = True
    SS['stim_freq_save'][~active_mask] = 0
    SS['stim_amp_save'][~active_mask] = 0
    
    # SS['stim_seq'] = [] # list of Ripple's StimSeq class (for each chan)
    SS['StimIdx'] = np.zeros(SS['active_stim'].shape[0], dtype=bool) # which chan to stim on this iteration
    charge = 0;
    maxElectrodes = 11;
    for i in range(SS['active_stim'].shape[0]):
        if i > maxElectrodes:  #FDA Stimulation Settings
            # print("More than 12 Electrodes")
            break
        StimChan = SS['active_stim'][i,0]
        
        # set stim values
        if SS['manual_stim']:
            # CSF = SS['active_stim'][i,5] # set to min frequency
            if SS['active_stim'][i,2] == 5: # algorithm is vibrotactile
                CSF = 255
                CSA = 0
            else:
                CSF = SS['active_stim'][i,5]
                CSA = SS['active_stim'][i,3] # set to min amplitude
        else:
            CSF, CSA = fd.DEKA2StimCOB(SS,i)
        CSF = fd.clip(CSF, 0, 300) ##TODO: Confirm FDA limit on frequency Do we want to print?
        CSA = fd.clip(CSA, 0, 100) ##TODO: Confirm FDA limit on amplitude Do we want to print?
               
        # update arrays to be saved to disk
        if StimChan <= 95: # USEA 1
            StimIdx = StimChan
        elif StimChan <= 223: # USEA 2
            StimIdx = StimChan - 32
        else: # USEA 3 (<= 351)
            StimIdx = StimChan - 64
        SS['stim_freq_save'][StimIdx] = CSF
        SS['stim_amp_save'][StimIdx] = CSA
        
        if SS['active_stim'][i,2] == 5: # algorithm is vibrotactile
            if StimChan<=5:
                SS['VT_stim'][StimChan] = CSF
                    
        else: # electrotactile
            if CSF > 0: # stimulate
                #calculating number of NIP cycles between current time and next pulse
                
                NextPulseDiff = max([math.floor(SS['next_pulse'][StimIdx] - SS['cur_time']),1])
               
                if NextPulseDiff<math.floor(0.033 * 30000): # if we need to stim before next loop would start
                    
                    SS['stim_seq'][i].electrode = int(StimChan)
                    SS['stim_seq'][i].period = int(math.floor(30000/CSF))
                    SS['stim_seq'][i].repeats = int(math.ceil(0.033 * CSF))
                    
                    if NextPulseDiff == 1 and CSF < (1/0.033):
                        # print('immed')
                        SS['stim_seq'][i].action = 0 # 'immed'
                    else:
                        # print('curcyc')
                        SS['stim_seq'][i].action = 1 # 'curcyc'=1 #TODO: keep this 0 for now until production xipppy is released
                    
                    # SS['stim_seq'][i].segments[0].length = # fixed at 200 us
                    SS['stim_seq'][i].segments[0].amplitude = int(CSA)
                    # SS['stim_seq'][i].segments[2].length = # fixed at 200 us
                    SS['stim_seq'][i].segments[2].amplitude = int(CSA)
                    SS['next_pulse'][StimIdx] = SS['cur_time'] + NextPulseDiff + math.floor(30000/CSF)
                    
                    newCharge = 0.2 * int(CSA) # pulse width in seconds times current in Amps = microAmps
                    if charge + newCharge < 144:
                        SS['StimIdx'][i] = True
                        charge += newCharge
                    else:
                        maxElectrodes += 1 # Allow one more electrode since we skipped this electrode
                        print("over 144 nC! total charge is " + str(charge) + " new charge trying to append is = " + str(newCharge) + " Searching for smaller magnitude pulse")
                    
                    
    if any(SS['StimIdx']):
        try: # could really clean up this try
            true_seqs = []
            for i in range(len(SS['StimIdx'])):
                if SS['StimIdx'][i] == True:
                    true_seqs.append(SS['stim_seq'][i])
            xp.StimSeq.send_stim_seqs(true_seqs)
        except:
            print('unable to send stim in stim_engine.py')
            
    if SS['VT_ard'] is not None:
        SS['VT_ard'].write(SS['VT_stim'])
    
    
    
    
    return SS
