import matplotlib.pyplot as plt

from tyssue.draw import sheet_view

def draw_half_sheet(sheet, ax):
    sheet_copy = sheet.copy()
    sheet_copy.edge_df = sheet_copy.edge_df[sheet.edge_df["sy"] > 0] 
    draw_specs = {
        'vert': {
            'visible': False
            },
        'edge': {
            'color': sheet_copy.edge_df["weight"],
            'colormap': "coolwarm",
            #'zorder': depth.values
            }
    }
    fig, ax = sheet_view(sheet_copy, ax=ax, coords = ['z', 'x'], **draw_specs)
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig, ax


def draw_half_N_sheet(sheet, ax, coords = ['z', 'x']):
    sheet_copy = sheet.copy()
    sheet_copy.edge_df = sheet_copy.edge_df[sheet.edge_df["sy"] > 0] 
    draw_specs = {
        'vert': {
            'visible': False
            },
        'edge': {
            'color': "#2b5d0a",
            'colormap': "coolwarm",
             "width": 0.3,
            #'zorder': depth.values
            }
    }
    fig, ax = sheet_view(sheet_copy, ax=ax, coords = ['z', 'x'], **draw_specs)
   
    return fig, ax