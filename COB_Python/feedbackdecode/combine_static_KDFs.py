# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:48:44 2022

Combines KDFs from static folders into one training

@author: TNT
"""

import numpy as np
import feedbackdecode as fd
def combine_static_KDFs(SS, RootDir):
    
    try:
        
        if SS['num_EMG_chans'] == 16:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/individual_KDFs/*.kdf')
            
        elif SS['num_EMG_chans'] == 32:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/individual_KDFs32/*.kdf')
        
        print("read latest KDF for individual")

        kin = np.array(new_kin)
        feat = np.array(new_feat)
        print("Size of Kin individual:" + str(kin.shape))
        print("Size of Feat individual:" + str(feat.shape))
    except:
        print("No individual KDF")
        kin = [];
        feat = [];
    
    try:
        if SS['num_EMG_chans'] == 16:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_Pinch_KDFs/*.kdf')
            
        elif SS['num_EMG_chans'] == 32:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_Pinch_KDFs32/*.kdf')
        print("Size of Kin for combo pinch:" + str(new_kin.shape))
        print("Size of Feat for combo pinch:" + str(new_feat.shape))
        kin = np.concatenate([kin,new_kin])
        feat = np.concatenate([feat, new_feat])
        print("Size of Kin after concatenation:" + str(kin.shape))
        print("Size of feat after concatenation" + str(feat.shape))
    except:
        print("No combo pinch KDF")
        
    try:
        if SS['num_EMG_chans'] == 16:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_Rotation_KDFs/*.kdf')
            
        elif SS['num_EMG_chans'] == 32:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_Rotation_KDFs32/*.kdf')
        print("read latest KDF for combo")
        kin = np.concatenate([kin,new_kin])
        feat = np.concatenate([feat, new_feat])
        print("didn't fail trying to get combo rotation")
    except:
        print("No combo rotation KDF")
        
    try:
        if SS['num_EMG_chans'] == 16:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_FlexExt_KDFs/*.kdf')
            
        elif SS['num_EMG_chans'] == 32:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_FlexExt_KDFs32/*.kdf')

        kin = np.concatenate([kin,new_kin])
        feat = np.concatenate([feat, new_feat])
    except:
        print("No combo flex/Ext KDF")
        

        
    try:
        if SS['num_EMG_chans'] == 16:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_KeyGrip_KDFs/*.kdf')
            
        elif SS['num_EMG_chans'] == 32:
            new_kin, new_feat = fd.readKDFFileLatestPath( RootDir,  r'/combo_KeyGrip_KDFs32/*.kdf')

        kin = np.concatenate([kin,new_kin])
        feat = np.concatenate([feat, new_feat])
    except:
        print("No combo key grip KDF")
        
    print("Size of Kin:" + str(kin.shape))
    print("Size of Feat:" + str(feat.shape))
    return SS, kin, feat