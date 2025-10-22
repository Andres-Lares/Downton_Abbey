# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 01:54:36 2025

@author: alare
"""

# app.py
import streamlit as st
from pyvis.network import Network
import networkx as nx
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="Downton Companion — The Grand Finale", layout="wide")
st.title("Downton Companion — *The Grand Finale*")
st.markdown(
    "Interactive family & staff guide for guests. Click a name in the left panel to highlight and read a short, movie-accurate note."
)

# -----------------------
# Data (accurate to the movie)
# Sources: Wikipedia page for the film, People article & press (see citations at bottom)
# -----------------------

# Each entry: id, display name, role (Family / Staff / In-Law / Guest), relation summary, movie-note
CHARACTERS = [
    {
        "id": "violet",
        "name": "Violet Crawley\n(Dowager Countess)",
        "group": "Family",
        "relation": "Matriarch — Robert's mother; grandmother to Mary, Edith, (Sybil deceased).",
        "note": "Central emotional figure in the finale; her legacy and an inherited villa in France are key plot elements."
    },
    {
        "id": "robert",
        "name": "Robert Crawley\n(Earl of Grantham)",
        "group": "Family",
        "relation": "Head of the family; husband to Cora; father of Mary, Edith, and the late Sybil.",
        "note": "Estate steward; concerned about Downton's future and family dignity."
    },
    {
        "id": "cora",
        "name": "Cora Crawley\n(Countess)",
        "group": "Family",
        "relation": "Robert's wife; American by birth; mother to Mary & Edith.",
        "note": "Supportive partner; film scenes touch on her family connections and heritage."
    },
    {
        "id": "mary",
        "name": "Lady Mary\n(Mary Talbot)",
        "group": "Family",
        "relation": "Eldest daughter; widow of Matthew; mother to George; previously married to Henry Talbot (divorce revealed in the film).",
        "note": "Mary faces a social challenge in the film after her marital situation is revealed; still the estate's principal manager."
    },
    {
        "id": "edith",
        "name": "Lady Edith\n(Marchioness of Hexham)",
        "group": "Family",
        "relation": "Middle daughter; now Marchioness of Hexham; sister to Mary.",
        "note": "Independent and professionally active; her storyline shows continued personal growth."
    },
    {
        "id": "tom",
        "name": "Tom Branson",
        "group": "Family",
        "relation": "Former chauffeur who married Sybil (deceased); now part of the family and an estate manager figure.",
        "note": "Represents social change; returns with family developments in the later films."
    },
    {
        "id": "bates",
        "name": "John Bates",
        "group": "Staff",
        "relation": "Valet (upstairs) — husband to Anna Bates.",
        "note": "Steady, loyal; part of the servants' emotional core."
    },
    {
        "id": "anna",
        "name": "Anna Bates",
        "group": "Staff",
        "relation": "Lady Mary's maid; married to John Bates.",
        "note": "Warm, grounded, present in most family events."
    },
    {
        "id": "carson",
        "name": "Charles Carson",
        "group": "Staff",
        "relation": "Butler (retired/consulted) and a symbol of the old service tradition.",
        "note": "Respected figure who occasionally returns to help with major events."
    },
    {
        "id": "hughes",
        "name": "Elsie Hughes\n(Mrs Hughes)",
        "group": "Staff",
        "relation": "Housekeeper, married to Mr Carson.",
        "note": "Practically minded, often the staff's emotional anchor."
    },
    {
        "id": "barrow",
        "name": "Thomas Barrow",
        "group": "Staff",
        "relation": "Senior servant; complex arc across series and films.",
        "note": "By the final film, he seeks a dignified and personally fulfilling future."
    },
    {
        "id": "patmore",
        "name": "Mrs Patmore",
        "group": "Staff",
        "relation": "Head cook, mentor to kitchen staff.",
        "note": "Brings warmth and comic relief in the downstairs storylines."
    },
    {
        "id": "daisy",
        "name": "Daisy",
        "group": "Staff",
        "relation": "Kitchen assistant; younger staff representative.",
        "note": "Represents the newer generation of staff; personal growth arcs continue."
    },
    {
        "id": "molesley",
        "name": "Mr Molesley",
        "group": "Staff",
        "relation": "Former footman, schoolteacher, occasional aspiring writer.",
        "note": "Has some surprising new opportunities connected to film work in the house."
    },
    {
        "id": "edithspouse",
        "name": "Bertie Pelham",
        "group": "In-Law",
        "relation": "Edith's husband (Marquess of Hexham).",
        "note": "Supportive presence in Edith's life."
    },
    # Additional cameo/guest characters can be added later if you want more detail
]

# Quick lookup
CHAR_MAP = {c["id"]: c for c in CHARACTERS}

# -----------------------
# Helpers: build graph (pyvis) and embed
# -----------------------

def make_network(highlight=None):
    """
    Build a PyVis interactive graph. highlight = id of node to emphasize.
    Returns path to temporary HTML file.
    """
    G = nx.Graph()
    # add nodes
    for c in CHARACTERS:
        G.add_node(c["id"], label=c["name"], group=c["group"])
    # add family edges (simple known connections)
    edges = [
        ("violet", "robert"),
        ("robert", "cora"),
        ("robert", "mary"),
        ("robert", "edith"),
        ("robert", "tom"),
        ("mary", "edith"),
        ("mary", "bates"),  # upstairs connection (Mary <-> Bates via staff)
        ("bates", "anna"),
        ("carson", "hughes"),
        ("patmore", "daisy"),
        ("molesley", "patmore"),
        ("edith", "edithspouse"),
        ("tom", "daisy"),
        # add more logical links if desired
    ]
    for a, b in edges:
        G.add_edge(a, b)

    net = Network(height="650px", width="100%", bgcolor="#0b0b0b", font_color="white", notebook=False)

    # configure physics for nicer layout
    net.barnes_hut()

    for node, data in G.nodes(data=True):
        label = data.get("label", node)
        group = data.get("group", "Other")
        title = CHAR_MAP[node]["note"]
        color = "#c9b37e" if group == "Family" else "#7f8c8d"
        size = 30 if node == highlight else 18
        net.add_node(node, label=label, title=title, color=color, size=size)

    for source, target in G.edges():
        net.add_edge(source, target, color="#cccccc")

    # If highlight, center that node
    if highlight:
        net.force_atlas_2based()

    tmpdir = tempfile.gettempdir()
    out_path = os.path.join(tmpdir, "downton_graph.html")
    net.show(out_path)
    return out_path

# -----------------------
# UI layout
# -----------------------

left, right = st.columns([2, 3])

with left:
    st.subheader("Characters")
    st.markdown("Filter or click a name to show details and highlight on the graph.")
    group_filter = st.selectbox("Show", options=["All", "Family", "Staff", "In-Law"], index=0)
    char_list = [c for c in CHARACTERS if group_filter == "All" or c["group"] == group_filter]

    # selection
    selected = st.selectbox("Select a character", options=[f'{c["name"]}' for c in char_list])
    # map back to id
    sel_id = None
    for c in char_list:
        if c["name"] == selected:
            sel_id = c["id"]
            break

    # Quick facts
    if sel_id:
        c = CHAR_MAP[sel_id]
        st.markdown(f"**{c['name']}**")
        st.markdown(f"*Role*: {c['group']}")
        st.markdown(f"*Relation*: {c['relation']}")
        st.markdown(f"*Movie note*: {c['note']}")

    st.markdown("---")
    st.markdown("**Quick controls**")
    st.caption("Tip: use the network on the right — zoom & pan are enabled.")
    if st.button("Center all"):
        sel_id = None

with right:
    st.subheader("Interactive Relationship Map")
    # Build & embed pyvis HTML
    html_path = make_network(highlight=sel_id)
    html = open(html_path, "r", encoding="utf-8").read()
    st.components.v1.html(html, height=700, scrolling=True)

st.markdown("---")
st.caption(
    "Source notes: data adapted from publicly available reporting and the official film entries to ensure accuracy for the final film (see sources below)."
)

# -----------------------
# Sources / Citations
# -----------------------
st.markdown(
    """
**Sources & verification (movie-specific facts):**  
- *Downton Abbey: The Grand Finale* — official film entry and cast info (Wikipedia). :contentReference[oaicite:0]{index=0}  
- People magazine coverage on trailer and cast developments. :contentReference[oaicite:1]{index=1}  
- Coverage about Matthew Goode (Henry Talbot) absence in the final film. :contentReference[oaicite:2]{index=2}

(If you need exact scene-level spoilers or extended cast detail, I can expand the dataset.)
"""
)