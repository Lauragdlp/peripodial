import numpy as np
import pandas as pd

from tyssue.utils import data_at_opposite

from tyssue.geometry.sheet_geometry import (
    SheetGeometry,
    WeightedPerimeterEllipsoidLameGeometry)
from peripodial.polarity import update_weights


def face_orientation(df, rcoords=["rx", "ry", "rz"]):
    """Returns a vector with the scaling term s and the first line
    of the rotation matrix V from the singular value decomposition
    of df[rcoords]"""

    _, s, vh = np.linalg.svd(df[rcoords].to_numpy())##
    return np.concatenate((s, vh[0, :]))

def anysotropy (sheet, coords=None, column=None, save_orientation=False):
    
    if coords is None:
        coords = sheet.coords
    
    rcoords = ["r" + u for u in coords]
    svd = np.vstack(
        sheet.edge_df.groupby("face").apply(face_orientation, rcoords=rcoords)
    )
    ocoords = ["orientation" + u for u in coords]
    orientation = pd.DataFrame(svd[:, len(coords):], columns=ocoords)
    if save_orientation:
        sheet.face_df[ocoords] = orientation
        
    sheet.face_df["anisotropy"] = (
        svd[:, 0] - svd[:, 1]) / (svd[:, 0] + svd[:, 1])
    
    return sheet.face_df["anisotropy"]

def angle_distribution (sheet, coords=None, above_threshold=1):
    if coords is None:
        coords = sheet.coords

    z_orientation = update_weights(sheet, 
        threshold_angle=theta, 
        below_threshold=1,
        above_threshold=above_threshold)
    sheet.vert_df["angle_vert"] = np.arcsin(z_orientation)
    
    return sheet.vert_df["angle_vert"]