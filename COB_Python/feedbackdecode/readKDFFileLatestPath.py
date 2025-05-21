# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:51:57 2022

Grabs the latest KDF file from the specified folder in the root directory provided

@author: TNT
"""


import glob
import os
import numpy as np
def readKDFFileLatestPath( RootDir, FolderName ):

    # load most recent training file
    list_of_files = glob.glob(RootDir + FolderName)
    latest_file = max(list_of_files, key=os.path.getctime)
 
    train_FID = open(latest_file, 'br', buffering=0)  
    print(train_FID)
    train_contents = np.fromfile(train_FID, dtype='single')
    train_FID.close()
    
    # parse file
    header = train_contents[:3].astype('int')
    train_data = train_contents[3:]
    train_data = train_data.reshape(-1,sum(header))
    idxs = np.cumsum(header)
    NIP_times = train_data[:,:idxs[0]]
    features = train_data[:,idxs[0]:idxs[1]]
    kinematics = train_data[:,idxs[1]:idxs[2]]
    
     
    
    return kinematics, features