# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 01:54:36 2025

@author: alare
"""

# app.py
import streamlit as st
from pyvis.network import Network
import networkx as nx
import tempfile
import os

# -----------------------
# STREAMLIT SETUP
# -----------------------
st.set_page_config(page_title="Downton Abbey — Family Tree", layout="wide")
st.title("🏰 Downton Abbey: The Grand Finale — Family & Household Tree")

st.markdown(
    """
An interactive **relationship map** for *Downton Abbey: The Grand Finale* (2025).  
Use your mouse to zoom, pan, and explore connections between the Crawley family and the Downton household.
"""
)

# -----------------------
# CHARACTER DATA
# -----------------------

CHARACTERS = [
    # Core Family
    ("violet", "Violet Crawley (Dowager Countess)", "Family"),
    ("robert", "Robert Crawley (Earl of Grantham)", "Family"),
    ("cora", "Cora Crawley (Countess of Grantham)", "Family"),
    ("mary", "Lady Mary Talbot", "Family"),
    ("edith", "Lady Edith Pelham", "Family"),
    ("sybil", "Lady Sybil Branson (†)", "Family"),
    ("tom", "Tom Branson", "Family"),
    ("george", "Master George Crawley", "Family"),
    ("bertie", "Bertie Pelham (Marquess of Hexham)", "In-Law"),

    # Staff / Household
    ("carson", "Charles Carson", "Staff"),
    ("hughes", "Elsie Hughes (Mrs. Carson)", "Staff"),
    ("bates", "John Bates", "Staff"),
    ("anna", "Anna Bates", "Staff"),
    ("barrow", "Thomas Barrow", "Staff"),
    ("patmore", "Mrs. Patmore", "Staff"),
    ("daisy", "Daisy", "Staff"),
    ("molesley", "Mr. Molesley", "Staff"),
]

# Relationships: (source, target, type)
RELATIONSHIPS = [
    # Family ties
    ("violet", "robert", "parent"),
    ("robert", "mary", "parent"),
    ("robert", "edith", "parent"),
    ("robert", "sybil", "parent"),
    ("robert", "cora", "spouse"),
    ("mary", "george", "parent"),
    ("edith", "bertie", "spouse"),
    ("sybil", "tom", "spouse"),
    # Staff / household
    ("carson", "hughes", "spouse"),
    ("bates", "anna", "spouse"),
    ("patmore", "daisy", "mentor"),
    ("molesley", "patmore", "colleague"),
    ("barrow", "carson", "work"),
    ("barrow", "bates", "colleague"),
    ("tom", "carson", "work"),
    ("mary", "carson", "work"),
    ("edith", "patmore", "work"),
]

# -----------------------
# GRAPH CONSTRUCTION
# -----------------------

def build_family_network():
    """Create and return a PyVis interactive graph as a temporary HTML file."""
    G = nx.Graph()

    # Add nodes
    for node_id, label, group in CHARACTERS:
        color = {
            "Family": "#c9b37e",
            "In-Law": "#9bbcd1",
            "Staff": "#8a8a8a",
        }.get(group, "#cccccc")

        size = 30 if group == "Family" else 20
        G.add_node(node_id, label=label, color=color, size=size)

    # Add edges
    for src, tgt, rel in RELATIONSHIPS:
        style = {
            "parent": "#d4b483",
            "spouse": "#b0a3e5",
            "mentor": "#87b897",
            "work": "#cccccc",
            "colleague": "#cccccc",
        }.get(rel, "#aaaaaa")
        G.add_edge(src, tgt, color=style, width=2)

    net = Network(
        height="700px", width="100%",
        bgcolor="#0b0b0b", font_color="white", directed=False
    )

    # Use a stable layout
    net.barnes_hut(gravity=-20000, central_gravity=0.3, spring_length=180, damping=0.9)

    # Add nodes and edges into the pyvis Network
    for node, data in G.nodes(data=True):
        # pyvis expects keys: id, label, title, color, size
        net.add_node(node, label=data.get("label"), title=data.get("label"),
                     color=data.get("color"), size=data.get("size"))
    for u, v, data in G.edges(data=True):
        net.add_edge(u, v, color=data.get("color"), width=data.get("width", 2))

    # Write the HTML to a file (safe in headless / cloud environments)
    tmp = tempfile.gettempdir()
    out_path = os.path.join(tmp, "downton_tree.html")
    net.write_html(out_path)   # <<< use write_html instead of show()
    return out_path

# -----------------------
# APP DISPLAY
# -----------------------
html_path = build_family_network()
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=750, scrolling=False)

st.markdown("---")
st.caption(
    "Accurate to *Downton Abbey: The Grand Finale (2025)* — Relationships reflect family, marriages, and main household connections."
)

