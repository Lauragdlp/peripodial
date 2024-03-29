import os
import random
import numpy as np
import pandas as pd

from polarity.dynamics import EllipsoidLameGeometry as geom
from polarity.toolbox import (define_fold_position,
                              define_apoptotic_pattern,
                              define_polarity)
from polarity.apoptosis import apoptosis_patterning
from polarity.delamination import delamination

from tyssue.dynamics import effectors
from tyssue.dynamics.factory import model_factory

from tyssue.solvers.quasistatic import QSSolver
from tyssue.core.history import HistoryHdf5
from tyssue.behaviors.event_manager import EventManager
from tyssue.behaviors.sheet.basic_events import reconnect


model = model_factory(
    [
        effectors.BarrierElasticity,
        effectors.RadialTension,
        effectors.PerimeterElasticity,
        effectors.FaceAreaElasticity,
        effectors.LumenVolumeElasticity,
    ], effectors.FaceAreaElasticity)

#Don't forget to add before sheet_copy = sheet.copy()
def update_weights(
    sheet, 
    threshold_angle=np.pi/3, 
    above_threshold=1,
    below_threshold=0.5
):
    """
    
    """

    threshold = np.sin(threshold_angle)**2

    # Define polarity
    z_orientation = (
        (sheet.edge_df['dx']**2 + sheet.edge_df['dy']**2)
        / (sheet.edge_df['length']**2)
    )

    """
    for idx in sheet.edge_df.index:
        if z_orientation.loc[idx] < threshold:
            sheet.edge_df.loc[idx, "weight"] = below_threshold
        else:    
            sheet.edge_df.loc[idx, "weight"] = above_threshold

    """
    #Apply polarity
    sheet.edge_df.loc[(z_orientation < threshold), 'weight'] = below_threshold
    sheet.edge_df.loc[(z_orientation >= threshold), 'weight'] = above_threshold

    
    
    #Normalize weights
    geom.normalize_weights(sheet)
    return z_orientation
    