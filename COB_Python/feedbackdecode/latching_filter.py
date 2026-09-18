# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 08:47:43 2020

@author: Eric
"""
import numpy as np

def latching_filter(SS, LF_C=1, velIdxs=None):

    # Keep decoder states consistently as column vectors: (n_DOF, 1)
    SS['xhat'] = np.asarray(SS['xhat']).reshape(-1, 1)
    SS['xhat_prev'] = np.asarray(SS['xhat_prev']).reshape(-1, 1)

    change = SS['xhat'] - SS['xhat_prev']

    change = LF_C * np.square(change)
    change[change > 1] = 1

    SS['xhat'] = SS['xhat_prev'] + change * (
        SS['xhat'] - SS['xhat_prev']
    )

    SS['xhat'][SS['xhat'] > 1] = 1
    SS['xhat'][SS['xhat'] < -1] = -1

    SS['xhat_prev'] = SS['xhat'].copy()

    return SS