import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from enum import Enum
from helpers import *

# TODO maybe move to helpers? 

class PlotSols:
    def __init__(self):
        self.force_refresh=False

    def plot_node_sols(self, node:NodeProperties, fig=go.Figure()):
        
        for face in node.faces.face_list:
            fig = self.plot_face_sols(face, node.index, fig)
        return fig


    def plot_face_sols(self, face:Face, ix:int=0, fig=go.Figure(), ):
        
        if not face.viz_data or self.force_refresh:
            face.get_face_sols()
            face.create_viz_data()
            # print("refresh")

        color = COLORWAY[ix]
        label = f"{ix}.{face.name}"

        if face.viz_data and not face.orig_sols:
            if face.viz_type=="shape": # TODO make enum 
                if "d1" in face.viz_data.keys():
                    fig.add_trace(go.Scatter(face.viz_data["d2"],
                    mode='lines', line_color=color, name=f"{label}_match"
                    ))
                    fig.add_trace(go.Scatter(face.viz_data["d1"],
                    mode='lines', name=label, line_color=color, fillpattern=dict(shape="x", fillmode="replace")
                    ))
        
            elif face.viz_type == "lines":
                fig.add_trace(go.Scatter(face.viz_data, mode='lines', name=label, line=dict(color=color, width=4),)), 

        fig.update_layout(xaxis_title='x',
                        yaxis_title='y',)

        fig.update_xaxes(range=[-20, 80])
        fig.update_yaxes(range=[-20, 80])

        return fig    







        # face.viz_data = d
        # face.viz_type = type
        

# def create_constrained_node_data():


        


# fig = go.Figure()
# fig.add_trace(go.Scatter(res, mode='markers',))
# fig.update_layout(xaxis_title='x',
#                   yaxis_title='y',)
    

# fig = go.Figure()
# fig.add_shape(
#     res,type="rect",
#     line=dict(color="RoyalBlue"),
#     fillcolor="RoyalBlue",
#     opacity=0.5
# )
# fig.update_layout(xaxis_title='x',
#                   yaxis_title='y',)

# fig.update_xaxes(range=[0, 50], showgrid=False)
# fig.update_yaxes(range=[0, 50])