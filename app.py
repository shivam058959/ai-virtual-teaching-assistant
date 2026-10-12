import os



import io



import json



import re



import sqlite3



import hashlib



import hmac



import secrets







import streamlit as st



import numpy as np



import faiss







from dotenv import load_dotenv



from pypdf import PdfReader



from google import genai



from google.genai import types







from xml.sax.saxutils import escape



from reportlab.lib import colors



from reportlab.lib.enums import TA_CENTER



from reportlab.lib.pagesizes import A4



from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle



from reportlab.lib.units import mm



from reportlab.platypus import (



          SimpleDocTemplate,



          Paragraph,



          Spacer,



          HRFlowable,



)







# =====================================================



# CONFIGURATION



# =====================================================







st.set_page_config(



          page_title="AI Virtual Teaching Assistant",



          page_icon="🎓",



          layout="wide"



)



# =====================================================

# MODERN UI THEME

# =====================================================

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: radial-gradient(circle at 75% 0%, rgba(124,107,255,.10), transparent 28%), #f7f8fc; }

.block-container { max-width: 1180px; padding-top: 1.8rem; padding-bottom: 3rem; }

[data-testid="stSidebar"] { background: linear-gradient(180deg,#171a35 0%,#22264a 100%); border-right:1px solid rgba(255,255,255,.08); }

[data-testid="stSidebar"] * { color:#f5f6ff; }

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#c8cbe5; }

[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.14); }

[data-testid="stSidebar"] [data-testid="stRadio"] label { background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.07); border-radius:12px; padding:.55rem .7rem; margin-bottom:.35rem; transition:all .18s ease; }

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,255,255,.12); border-color:#a78bfa; }

[data-testid="stSidebar"] [data-testid="stFileUploader"] section { background:rgba(255,255,255,.07); border:1px dashed rgba(255,255,255,.28); border-radius:12px; }

[data-testid="stSidebar"] [data-testid="stButton"] button { border-radius:11px; border:1px solid rgba(255,255,255,.15); background:rgba(255,255,255,.09); color:white; font-weight:600; }

[data-testid="stSidebar"] [data-testid="stButton"] button:hover { background:rgba(255,255,255,.16); border-color:#a78bfa; }

h1,h2,h3 { letter-spacing:-.035em; color:#1b2340 !important; } h1 { font-weight:800!important; } h2,h3 { font-weight:700!important; } [data-testid='stTextInput'] label, [data-testid='stForm'] label, [data-testid='stWidgetLabel'], [data-testid='stWidgetLabel'] p, [data-testid='stHeading'] h1, [data-testid='stHeading'] h2, [data-testid='stHeading'] h3, [data-testid='stMarkdownContainer'] p { color:#27304a !important; }

[data-testid="stMetric"] { background:white; border:1px solid #e9eaf4; border-radius:16px; padding:1rem; box-shadow:0 5px 18px rgba(31,41,80,.045); }

.stButton button,.stDownloadButton button { border-radius:12px; font-weight:650; padding:.55rem 1rem; transition:transform .15s ease,box-shadow .15s ease; }

.stButton button[kind="primary"],.stDownloadButton button { background:linear-gradient(110deg,#6254e8,#8b5cf6); border:none; color:white; box-shadow:0 5px 14px rgba(98,84,232,.20); }

.stButton button:hover,.stDownloadButton button:hover { transform:translateY(-1px); box-shadow:0 8px 20px rgba(98,84,232,.20); }

.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stNumberInput input { border-radius:11px!important; }

[data-testid="stChatInput"] { border:1px solid #e0def8; border-radius:18px; box-shadow:0 10px 32px rgba(42,40,100,.10); background:white; }

[data-testid="stChatInput"] textarea { font-size:1rem; }

[data-testid="stChatMessage"] { border:1px solid #ececf5; border-radius:16px; padding:.85rem 1rem; background:white; box-shadow:0 4px 16px rgba(31,41,80,.035); }

[data-testid="stAlert"] { border-radius:13px; }

.ui-brand { display:flex; align-items:center; gap:14px; margin:0 0 1.25rem; }

.ui-brand-icon { display:flex; align-items:center; justify-content:center; width:52px; height:52px; border-radius:16px; color:white; font-size:25px; background:linear-gradient(135deg,#6254e8,#9b6bfa); box-shadow:0 8px 22px rgba(98,84,232,.25); }

.ui-brand-title { font-size:clamp(1.6rem,3vw,2.25rem); font-weight:800; color:#1b2340; letter-spacing:-.055em; line-height:1.15; }

.ui-brand-sub { color:#77809a; font-size:.92rem; margin-top:5px; }

.ui-chat-hero { text-align:center; padding:clamp(2rem,7vh,5rem) 1rem 1rem; }

.ui-chat-pill { display:inline-block; padding:7px 12px; margin-bottom:16px; color:#6254e8; background:#eeecff; border:1px solid #e0dcff; border-radius:999px; font-size:.8rem; font-weight:700; }

.ui-chat-title { color:#1b2340; font-size:clamp(2rem,4vw,3.1rem); font-weight:800; letter-spacing:-.06em; line-height:1.12; }

.ui-chat-sub { color:#77809a; font-size:1rem; margin:12px auto 1.5rem; max-width:560px; }

@media(max-width:700px){.block-container{padding-top:1rem}.ui-brand{gap:10px}.ui-brand-icon{width:44px;height:44px}}



/* Accessible contrast for sidebar and main content */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
    color: #f5f6ff !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #c8cbe5 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] label * {
    color: #f5f6ff !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button,
[data-testid="stSidebar"] [data-testid="stButton"] button * {
    color: #ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.13) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(124,107,255,.28) !important;
    border-color: #a78bfa !important;
}
.stApp h1, .stApp h2, .stApp h3,
[data-testid="stMarkdownContainer"] p,
[data-testid="stTextInput"] label,
[data-testid="stForm"] label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stTabs"] button {
    color: #1b2340 !important;
}
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(110deg, #6254e8, #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #d9d9ed !important;
}
[data-testid="stChatInput"] textarea {
    color: #1b2340 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #69738d !important;
}
[data-testid="stBottom"] {
    background: #f7f8fc !important;
}

/* Final visual polish: spacing, balanced background, readable text */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background:
        radial-gradient(circle at 78% 8%, rgba(124,107,255,.13), transparent 30%),
        linear-gradient(135deg, #f4f5ff 0%, #f8faff 52%, #eef1ff 100%) !important;
    color: #1b2340 !important;
}
.block-container {
    max-width: 1180px !important;
    padding-top: 4.5rem !important;
    padding-bottom: 5rem !important;
}
[data-testid="stHeader"] {
    background: rgba(244,245,255,.96) !important;
}
.ui-brand {
    margin-top: .75rem !important;
    margin-bottom: 1.75rem !important;
    padding-top: .25rem !important;
}
.ui-brand-title {
    color: #172044 !important;
    text-shadow: none !important;
}
.ui-brand-sub {
    color: #596581 !important;
}
.ui-chat-hero {
    padding-top: clamp(1.5rem, 5vh, 3.5rem) !important;
    padding-bottom: 2rem !important;
}
.ui-chat-title {
    color: #172044 !important;
}
.ui-chat-sub {
    color: #596581 !important;
}
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: #f0f2ff !important;
}
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #d8dcf2 !important;
    box-shadow: 0 10px 28px rgba(40,48,100,.10) !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea::placeholder {
    color: #293453 !important;
}
[data-testid="stChatInput"] button {
    color: #ffffff !important;
    background: #6254e8 !important;
}
@media (max-width: 700px) {
    .block-container { padding-top: 3.5rem !important; }
    .ui-brand { margin-top: .5rem !important; }
}


/* Final contrast fix for AI answers, lists, user questions, and chat composer */
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] span,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] em,
[data-testid="stMain"] [data-testid="stChatMessage"],
[data-testid="stMain"] [data-testid="stChatMessage"] * {
    color: #202b49 !important;
}
[data-testid="stMain"] [data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e1e5f2 !important;
}
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #d3d9ed !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea::placeholder {
    color: #263453 !important;
    -webkit-text-fill-color: #263453 !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #64708b !important;
    -webkit-text-fill-color: #64708b !important;
}

/* Chat input typed-text colour: white */

/* Make text typed into the chat box white; keep placeholder muted */
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #b8c2dc !important;
    -webkit-text-fill-color: #b8c2dc !important;
    opacity: 1 !important;
}

/* Chat input typed-text colour: black */

/* Make typed chat input black for contrast against the dark composer */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 1 !important;
}

/* Fix generated answer/subtopic text contrast; leave chat input untouched */

/* Fix generated answer/subtopic text contrast; leave chat input untouched */
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] span,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] em,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] td,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] th {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h5,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h6 {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Full dark theme: black backgrounds and white text across the app */

/* Full dark theme: black backgrounds and white text across the app */
:root {
    color-scheme: dark;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"],
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stChatMessage"],
[data-testid="stMain"] [data-testid="stExpander"],
[data-testid="stMain"] [data-testid="stDataFrame"],
[data-testid="stMain"] table {
    background-color: #000000 !important;
    color: #ffffff !important;
}
.stApp,
.stApp p,
.stApp li,
.stApp span,
.stApp label,
.stApp strong,
.stApp em,
.stApp td,
.stApp th,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6,
[data-testid="stMarkdownContainer"] *,
[data-testid="stChatMessage"] *,
[data-testid="stMetric"] *,
[data-testid="stCaptionContainer"] *,
[data-testid="stWidgetLabel"] *,
[data-testid="stAlert"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid #333333 !important;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: #151515 !important;
    color: #ffffff !important;
    border: 1px solid #3a3a3a !important;
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stChatInput"] textarea,
[data-baseweb="select"] > div,
[data-testid="stDateInput"] input {
    background: #111111 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
    border-color: #444444 !important;
}
[data-testid="stChatInput"] {
    background: #111111 !important;
    border: 1px solid #555555 !important;
}
[data-testid="stChatInput"] textarea::placeholder,
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #bdbdbd !important;
    -webkit-text-fill-color: #bdbdbd !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button,
.stButton button[kind="primary"],
.stDownloadButton button,
[data-testid="stFormSubmitButton"] button {
    background: #333333 !important;
    color: #ffffff !important;
    border: 1px solid #555555 !important;
}
[data-testid="stMetric"],
[data-testid="stAlert"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background: #111111 !important;
    color: #ffffff !important;
    border-color: #333333 !important;
}
hr {
    border-color: #333333 !important;
}

/* Polished midnight-purple theme: consistent surfaces and readable chat cards */

/* Polished midnight-purple theme: consistent surfaces and readable chat cards */
:root {
    color-scheme: dark;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #0b1020 !important;
    color: #f3f5ff !important;
}
[data-testid="stHeader"] {
    background: rgba(11,16,32,.96) !important;
}
[data-testid="stMain"] [data-testid="stVerticalBlock"],
[data-testid="stMain"] [data-testid="stHorizontalBlock"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"] {
    background: transparent !important;
}
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] span,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] em,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] td,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] th,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h5,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h6 {
    color: #f3f5ff !important;
    -webkit-text-fill-color: #f3f5ff !important;
}
.ui-brand-title,
.ui-chat-title {
    color: #f8f9ff !important;
    -webkit-text-fill-color: #f8f9ff !important;
}
.ui-brand-sub,
.ui-chat-sub {
    color: #b7c0dc !important;
    -webkit-text-fill-color: #b7c0dc !important;
}
.ui-chat-pill {
    color: #dcd6ff !important;
    background: #201b42 !important;
    border-color: #403478 !important;
}
/* Chat messages use a single consistent dark card; prevent white inner strips */
[data-testid="stMain"] [data-testid="stChatMessage"] {
    background: #151c31 !important;
    border: 1px solid #2c3654 !important;
    border-radius: 16px !important;
    padding: 1rem 1.1rem !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.18) !important;
    color: #f3f5ff !important;
}
[data-testid="stMain"] [data-testid="stChatMessage"] > div,
[data-testid="stMain"] [data-testid="stChatMessage"] [data-testid="stVerticalBlock"],
[data-testid="stMain"] [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    background: transparent !important;
}
[data-testid="stMain"] [data-testid="stChatMessage"] p,
[data-testid="stMain"] [data-testid="stChatMessage"] li,
[data-testid="stMain"] [data-testid="stChatMessage"] span,
[data-testid="stMain"] [data-testid="stChatMessage"] strong,
[data-testid="stMain"] [data-testid="stChatMessage"] h1,
[data-testid="stMain"] [data-testid="stChatMessage"] h2,
[data-testid="stMain"] [data-testid="stChatMessage"] h3,
[data-testid="stMain"] [data-testid="stChatMessage"] h4 {
    color: #f3f5ff !important;
    -webkit-text-fill-color: #f3f5ff !important;
    background: transparent !important;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background: #10162a !important;
    border-right: 1px solid #27304b !important;
}
[data-testid="stSidebar"] * {
    color: #edf0ff !important;
    -webkit-text-fill-color: #edf0ff !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: #1a223a !important;
    border: 1px solid #303b5c !important;
    border-radius: 12px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover,
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #29234f !important;
    border-color: #7667e8 !important;
}
/* Composer: keep input readable and visually separate from message cards */
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: #0b1020 !important;
}
[data-testid="stChatInput"] {
    background: #171d30 !important;
    border: 1px solid #35405f !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.2) !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #aab4d0 !important;
    -webkit-text-fill-color: #aab4d0 !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button {
    background: #6557e8 !important;
    color: #ffffff !important;
    border: 0 !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-baseweb="select"] > div,
[data-testid="stDateInput"] input {
    background: #171d30 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-color: #35405f !important;
}
[data-testid="stMetric"],
[data-testid="stAlert"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background: #151c31 !important;
    color: #f3f5ff !important;
    border-color: #2c3654 !important;
}
[data-testid="stMetric"] *,
[data-testid="stAlert"] *,
[data-testid="stExpander"] * {
    color: #f3f5ff !important;
    -webkit-text-fill-color: #f3f5ff !important;
}
.stButton button[kind="primary"],
.stDownloadButton button,
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(110deg, #6254e8, #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
}
hr {
    border-color: #2c3654 !important;
}

/* Remove the white chat-message outer borders and keep the dark card design */

/* Remove the white chat-message outer borders and keep the dark card design */
[data-testid="stMain"] [data-testid="stChatMessage"] {
    background: #151c31 !important;
    border: 0 !important;
    outline: 0 !important;
    border-radius: 16px !important;
    box-shadow: none !important;
    overflow: hidden !important;
}
[data-testid="stMain"] [data-testid="stChatMessage"] > div,
[data-testid="stMain"] [data-testid="stChatMessage"] > div > div,
[data-testid="stMain"] [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stChatMessage"] [data-testid="stVerticalBlock"] {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}
[data-testid="stMain"] [data-testid="stChatMessage"] [data-testid="stAvatar"] {
    background: transparent !important;
}

/* Definitively remove Streamlit chat message white panels/borders */

/* Definitively remove Streamlit chat message white panels/borders */
[data-testid="stChatMessage"],
[data-testid="stChatMessage"] > div,
[data-testid="stChatMessage"] > div > div,
[data-testid="stChatMessage"] [data-testid="stVerticalBlock"],
[data-testid="stChatMessage"] [data-testid="stHorizontalBlock"],
[data-testid="stChatMessage"] [data-testid="stMarkdown"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] > div {
    background: #151c31 !important;
    background-color: #151c31 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 1rem 1.1rem !important;
    margin-bottom: .85rem !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    color: #f3f5ff !important;
    -webkit-text-fill-color: #f3f5ff !important;
    background: transparent !important;
}

/* Force both user and assistant chat cards to dark surfaces with black borders */

/* Force both user and assistant chat cards to dark surfaces with black borders */
[data-testid="stChatMessage"],
[data-testid="stMain"] [data-testid="stChatMessage"],
[data-testid="stChatMessage"] > div,
[data-testid="stChatMessage"] > div > div,
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stVerticalBlock"],
[data-testid="stChatMessage"] [data-testid="stHorizontalBlock"] {
    background: #000000 !important;
    background-color: #000000 !important;
    border: 1px solid #000000 !important;
    outline: none !important;
    box-shadow: none !important;
}
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    padding: 1rem 1.1rem !important;
    margin-bottom: .8rem !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: transparent !important;
}
/* Also remove the white rim around the chat composer itself */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] textarea {
    background: #111111 !important;
    border-color: #000000 !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

</style>

""", unsafe_allow_html=True)











load_dotenv()







API_KEY = os.getenv("GEMINI_API_KEY")







if not API_KEY:



          st.error("GEMINI_API_KEY nahi mili. Apni .env file check karo.")



          st.stop()







client = genai.Client(api_key=API_KEY)



DB_PATH = "teaching_assistant.db"



MODEL = "gemini-3.5-flash-lite"







# =====================================================



# DATABASE



# =====================================================







def get_connection():



          return sqlite3.connect(DB_PATH)











def create_database():



          con = get_connection()



          cur = con.cursor()







          cur.execute("""



                    CREATE TABLE IF NOT EXISTS users (



                              id INTEGER PRIMARY KEY AUTOINCREMENT,



                              name TEXT NOT NULL,



                              username TEXT NOT NULL UNIQUE COLLATE NOCASE,



                              password_hash TEXT NOT NULL,



                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP



                    )



          """)







          cur.execute("""



                    CREATE TABLE IF NOT EXISTS quiz_attempts (



                              id INTEGER PRIMARY KEY AUTOINCREMENT,



                              student_id INTEGER,



                              score INTEGER,



                              total_questions INTEGER,



                              percentage REAL,



                              difficulty TEXT,



                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP



                    )



          """)







          columns = [



                    row[1]



                    for row in cur.execute(



                              "PRAGMA table_info(quiz_attempts)"



                    ).fetchall()



          ]







          if "user_id" not in columns:



                    cur.execute(



                              "ALTER TABLE quiz_attempts ADD COLUMN user_id INTEGER"



                    )







          con.commit()



          con.close()











create_database()







# =====================================================



# PASSWORD SECURITY



# =====================================================







def hash_password(password):



          salt = secrets.token_bytes(16)







          digest = hashlib.pbkdf2_hmac(



                    "sha256",



                    password.encode("utf-8"),



                    salt,



                    300000



          )







          return salt.hex() + ":" + digest.hex()











def verify_password(password, stored_hash):



          try:



                    salt_hex, digest_hex = stored_hash.split(":", 1)



                    salt = bytes.fromhex(salt_hex)



                    expected = bytes.fromhex(digest_hex)







                    actual = hashlib.pbkdf2_hmac(



                              "sha256",



                              password.encode("utf-8"),



                              salt,



                              300000



                    )







                    return hmac.compare_digest(actual, expected)







          except (ValueError, TypeError):



                    return False











def create_account(name, username, password):



          con = get_connection()







          try:



                    con.execute(



                              """



                              INSERT INTO users (name, username, password_hash)



                              VALUES (?, ?, ?)



                              """,



                              (name.strip(), username.strip(), hash_password(password))



                    )







                    con.commit()



                    return True, "Account created! Ab login karo."







          except sqlite3.IntegrityError:



                    return False, "Ye username pehle se registered hai."







          finally:



                    con.close()











def authenticate_user(username, password):



          con = get_connection()







          user = con.execute(



                    """



                    SELECT id, name, username, password_hash



                    FROM users



                    WHERE username = ? COLLATE NOCASE



                    """,



                    (username.strip(),)



          ).fetchone()







          con.close()







          if user and verify_password(password, user[3]):



                    return {



                              "id": user[0],



                              "name": user[1],



                              "username": user[2]



                    }







          return None











# =====================================================



# QUIZ DATABASE FUNCTIONS



# =====================================================







def save_quiz_attempt(user_id, score, total, percentage, difficulty):



          con = get_connection()







          con.execute(



                    """



                    INSERT INTO quiz_attempts



                    (user_id, score, total_questions, percentage, difficulty)



                    VALUES (?, ?, ?, ?, ?)



                    """,



                    (user_id, score, total, percentage, difficulty)



          )







          con.commit()



          con.close()











def get_quiz_history(user_id):



          con = get_connection()







          rows = con.execute(



                    """



                    SELECT score, total_questions, percentage,



                                       difficulty, created_at



                    FROM quiz_attempts



                    WHERE user_id = ?



                    ORDER BY id ASC



                    """,



                    (user_id,)



          ).fetchall()







          con.close()







          return [



                    {



                              "score": row[0],



                              "total": row[1],



                              "percentage": row[2],



                              "difficulty": row[3],



                              "created_at": row[4]



                    }



                    for row in rows



          ]











# =====================================================



# SESSION STATE



# =====================================================







defaults = {



          "authenticated_user": None,



          "messages": [],



          "chunks": [],



          "full_text": "",



          "index": None,



          "file_names": [],



          "quiz": [],



          "quiz_submitted": False,



          "quiz_score": 0,



          "quiz_saved": False,



          "summary": "",



          "question_paper": "",



          "paper_generated": False



}







for key, value in defaults.items():



          if key not in st.session_state:



                    st.session_state[key] = value











# =====================================================



# LOGIN AND SIGNUP



# =====================================================







if st.session_state.authenticated_user is None:







          st.title("🎓 AI Virtual Teaching Assistant")



          st.write("Login karo ya apna naya account banao.")







          login_tab, signup_tab = st.tabs(



                    ["🔐 Login", "📝 Sign Up"]



          )







          with login_tab:







                    with st.form("login_form"):



                              username = st.text_input("Username")



                              password = st.text_input(



                                        "Password",



                                        type="password"



                              )







                              login_button = st.form_submit_button(



                                        "Login",



                                        use_container_width=True



                              )







                    if login_button:







                              if not username.strip() or not password:



                                        st.error("Username aur password dono enter karo.")







                              else:



                                        user = authenticate_user(username, password)







                                        if user:



                                                  st.session_state.authenticated_user = user







                                                  st.session_state.messages = []



                                                  st.session_state.chunks = []



                                                  st.session_state.full_text = ""



                                                  st.session_state.index = None



                                                  st.session_state.file_names = []



                                                  st.session_state.quiz = []



                                                  st.session_state.quiz_submitted = False



                                                  st.session_state.quiz_saved = False



                                                  st.session_state.summary = ""



                                                  st.session_state.question_paper = ""



                                                  st.session_state.paper_generated = False







                                                  st.rerun()







                                        else:



                                                  st.error("Invalid username ya password.")







          with signup_tab:







                    with st.form("signup_form"):



                              name = st.text_input("Full Name")



                              new_username = st.text_input("Create Username")







                              new_password = st.text_input(



                                        "Create Password",



                                        type="password"



                              )







                              confirm_password = st.text_input(



                                        "Confirm Password",



                                        type="password"



                              )







                              signup_button = st.form_submit_button(



                                        "Create Account",



                                        use_container_width=True



                              )







                    if signup_button:







                              if not name.strip() or not new_username.strip():



                                        st.error("Saari details fill karo.")







                              elif len(new_username.strip()) < 3:



                                        st.error("Username minimum 3 characters ka hona chahiye.")







                              elif len(new_password) < 8:



                                        st.error("Password minimum 8 characters ka hona chahiye.")







                              elif new_password != confirm_password:



                                        st.error("Dono passwords match nahi kar rahe.")







                              else:



                                        success, message = create_account(



                                                  name,



                                                  new_username,



                                                  new_password



                                        )







                                        if success:



                                                  st.success(message)



                                        else:



                                                  st.error(message)










          st.stop()











# =====================================================



# LOGGED-IN USER



# =====================================================







current_user = st.session_state.authenticated_user



user_id = current_user["id"]







st.markdown(

          """<div class="ui-brand"><div class="ui-brand-icon">🎓</div><div><div class="ui-brand-title">AI Teaching Assistant</div><div class="ui-brand-sub">Your personal AI-powered learning space</div></div></div>""",

          unsafe_allow_html=True,

)







st.sidebar.title("👤 Student")



st.sidebar.write(f"**{current_user['name']}**")



st.sidebar.caption(f"@{current_user['username']}")







if st.sidebar.button("🚪 Logout", use_container_width=True):







          for key, value in defaults.items():



                    st.session_state[key] = value







          st.rerun()











# =====================================================



# SIDEBAR NAVIGATION



# =====================================================



page = st.sidebar.radio(

          "🧭 NAVIGATION",

          [

                    "💬 AI Chat",

                    "📚 Study Material",

                    "📖 AI Summary",

                    "📝 Quiz Center",

                    "📊 Performance",

                    "📄 Question Paper",

          ],

          key="main_navigation",

)



if page == "📚 Study Material":

          st.header("📚 Study Material")

          st.write("Upload your PDFs from the sidebar. The assistant will use them to answer your questions.")

          if st.session_state.file_names:

                    st.subheader("Uploaded PDFs")

                    for uploaded_name in st.session_state.file_names:

                              st.write(f"• {uploaded_name}")

          else:

                    st.info("Abhi koi PDF upload nahi hai. Sidebar se PDF upload karo.")



# =====================================================



# PDF UPLOAD



# =====================================================







st.sidebar.divider()



st.sidebar.subheader("📚 Study Material")







uploaded_files = st.sidebar.file_uploader(



          "Upload study PDFs",



          type=["pdf"],



          accept_multiple_files=True



)











# =====================================================



# PDF PROCESSING FUNCTIONS



# =====================================================







def extract_pdf_text(uploaded_file):



          reader = PdfReader(uploaded_file)



          text = ""







          for page in reader.pages:



                    page_text = page.extract_text()







                    if page_text:



                              text += page_text + "\n"







          return text











def create_chunks(text, chunk_size=500, overlap=100):



          words = text.split()



          chunks = []



          start = 0







          while start < len(words):



                    chunk = " ".join(words[start:start + chunk_size])







                    if chunk.strip():



                              chunks.append(chunk)







                    start += chunk_size - overlap







          return chunks











def create_embeddings(chunks):



          response = client.models.embed_content(



                    model="gemini-embedding-001",



                    contents=chunks,



                    config=types.EmbedContentConfig(



                              task_type="RETRIEVAL_DOCUMENT",



                              output_dimensionality=768



                    )



          )







          return np.array(



                    [item.values for item in response.embeddings],



                    dtype="float32"



          )











# =====================================================



# PROCESS UPLOADED PDFS



# =====================================================







if uploaded_files:







          current_names = [file.name for file in uploaded_files]







          if current_names != st.session_state.file_names:







                    all_chunks = []



                    all_text = ""







                    progress = st.progress(0)







                    for number, file in enumerate(uploaded_files):







                              try:



                                        with st.spinner(f"Reading {file.name}..."):



                                                  pdf_text = extract_pdf_text(file)







                                        if pdf_text.strip():



                                                  all_text += (



                                                            f"\n\n===== {file.name} =====\n\n"



                                                            + pdf_text



                                                  )







                                                  for chunk in create_chunks(pdf_text):



                                                            all_chunks.append(



                                                                      f"SOURCE FILE: {file.name}\n"



                                                                      f"CONTENT:\n{chunk}"



                                                            )







                              except Exception as error:



                                        st.warning(f"{file.name} read nahi hua: {error}")







                              progress.progress((number + 1) / len(uploaded_files))







                    progress.empty()







                    if not all_chunks:



                              st.error(



                                        "Readable text nahi mila. PDF scanned/image-based ho sakta hai."



                              )



                              st.stop()







                    try:



                              with st.spinner("Creating search index..."):







                                        embeddings = create_embeddings(all_chunks)



                                        faiss.normalize_L2(embeddings)







                                        index = faiss.IndexFlatIP(embeddings.shape[1])



                                        index.add(embeddings)







                              st.session_state.chunks = all_chunks



                              st.session_state.full_text = all_text



                              st.session_state.index = index



                              st.session_state.file_names = current_names







                              st.success(f"{len(current_names)} PDF(s) successfully loaded.")







                    except Exception as error:



                              st.error("PDF embedding error.")



                              st.code(str(error))











if st.session_state.file_names:







          st.sidebar.subheader("📄 Uploaded Files")







          for file_name in st.session_state.file_names:



                    st.sidebar.write(f"• {file_name}")











if page == "📊 Performance":

          # =====================================================



          # PERFORMANCE DASHBOARD



          # =====================================================







          quiz_history = get_quiz_history(user_id)







          st.sidebar.divider()



          st.sidebar.subheader("📊 Performance")







          if quiz_history:







                    total_questions = sum(



                              item["total"] for item in quiz_history



                    )







                    total_correct = sum(



                              item["score"] for item in quiz_history



                    )







                    accuracy = (



                              total_correct / total_questions * 100



                              if total_questions else 0



                    )







                    best_score = max(



                              item["percentage"] for item in quiz_history



                    )







                    st.sidebar.metric("Quiz Attempts", len(quiz_history))



                    st.sidebar.metric("Accuracy", f"{accuracy:.1f}%")



                    st.sidebar.metric("Best Score", f"{best_score:.0f}%")







          else:



                    st.sidebar.info("Abhi koi quiz attempt nahi hai.")











          with st.expander("📊 Student Performance Dashboard"):







                    if not quiz_history:



                              st.info("Pehle ek quiz complete karo.")







                    else:



                              total_questions = sum(



                                        item["total"] for item in quiz_history



                              )







                              total_correct = sum(



                                        item["score"] for item in quiz_history



                              )







                              total_wrong = total_questions - total_correct







                              col1, col2, col3, col4 = st.columns(4)







                              col1.metric("Attempts", len(quiz_history))



                              col2.metric("Correct", total_correct)



                              col3.metric("Wrong", total_wrong)



                              col4.metric(



                                        "Accuracy",



                                        f"{total_correct / total_questions * 100:.1f}%"



                              )







                              st.subheader("📈 Quiz Progress")







                              st.line_chart([



                                        item["percentage"] for item in quiz_history



                              ])







                              st.subheader("📋 Quiz History")







                              for number, item in enumerate(quiz_history, 1):



                                        st.write(



                                                  f"{number}. Score: {item['score']}/{item['total']} | "



                                                  f"{item['percentage']:.1f}% | "



                                                  f"{item['difficulty']} | {item['created_at']}"



                                        )















if page == "📖 AI Summary":

          # =====================================================



          # AI SUMMARY



          # =====================================================







          st.sidebar.divider()



          st.sidebar.subheader("📖 AI Summary")







          if st.sidebar.button("✨ Generate Summary"):







                    if not st.session_state.full_text:



                              st.sidebar.error("Pehle PDF upload karo.")







                    else:



                              prompt = f"""



          Create an exam-oriented summary from the following study material.







          Include:



          1. Summary



          2. Important Topics



          3. Important Points



          4. Important Exam Questions



          5. Exam Preparation Tips







          Use only the provided material.







          STUDY MATERIAL:



          {st.session_state.full_text}



          """







                              try:



                                        with st.spinner("Generating summary..."):







                                                  response = client.models.generate_content(



                                                            model=MODEL,



                                                            contents=prompt



                                                  )







                                                  st.session_state.summary = response.text







                              except Exception as error:



                                        st.error("Summary generate nahi hui.")



                                        st.code(str(error))











          if st.session_state.summary:



                    st.header("📖 AI Study Summary")



                    st.markdown(st.session_state.summary)















if page == "📝 Quiz Center":

          # =====================================================



          # AI QUIZ GENERATOR



          # =====================================================







          st.sidebar.divider()



          st.sidebar.subheader("📝 Quiz Generator")







          question_count = st.sidebar.slider(



                    "Number of Questions",



                    min_value=3,



                    max_value=10,



                    value=5



          )







          difficulty = st.sidebar.selectbox(



                    "Quiz Difficulty",



                    ["Easy", "Medium", "Hard"]



          )







          if st.sidebar.button("🚀 Generate Quiz"):







                    if not st.session_state.chunks:



                              st.sidebar.error("Pehle PDF upload karo.")







                    else:



                              context = "\n\n".join(st.session_state.chunks)







                              prompt = f"""



          Generate {question_count} multiple-choice questions



          from the provided study material.







          Difficulty: {difficulty}







          Return ONLY valid JSON in this format:



          [



               {{



                    "question": "Question text",



                    "options": ["Option A", "Option B", "Option C", "Option D"],



                    "answer": 0,



                    "explanation": "Explanation"



               }}



          ]







          The answer must be the zero-based index of the correct option.



          Do not add markdown or text outside the JSON.







          STUDY MATERIAL:



          {context}



          """







                              try:



                                        with st.spinner("Generating quiz..."):







                                                  response = client.models.generate_content(



                                                            model=MODEL,



                                                            contents=prompt



                                                  )







                                                  raw = response.text.strip()



                                                  raw = re.sub(r"```json", "", raw)



                                                  raw = re.sub(r"```", "", raw)







                                                  questions = json.loads(raw.strip())







                                                  if not isinstance(questions, list) or not questions:



                                                            raise ValueError("Invalid quiz format.")







                                                  st.session_state.quiz = questions



                                                  st.session_state.quiz_submitted = False



                                                  st.session_state.quiz_saved = False







                                                  for key in list(st.session_state.keys()):



                                                            if key.startswith("quiz_answer_"):



                                                                      del st.session_state[key]







                              except Exception as error:



                                        st.sidebar.error("Quiz generate nahi hua.")



                                        st.sidebar.code(str(error))











          # =====================================================



          # DISPLAY AND SUBMIT QUIZ



          # =====================================================







          if st.session_state.quiz:







                    st.header("📝 AI Generated Quiz")







                    for number, question in enumerate(st.session_state.quiz):







                              st.subheader(



                                        f"Q{number + 1}. {question['question']}"



                              )







                              st.radio(



                                        "Select your answer:",



                                        question["options"],



                                        index=None,



                                        key=f"quiz_answer_{number}"



                              )







                              st.divider()







                    if st.button("🎯 Submit Quiz"):







                              score = 0







                              for number, question in enumerate(st.session_state.quiz):







                                        selected = st.session_state.get(



                                                  f"quiz_answer_{number}"



                                        )







                                        if selected is not None:



                                                  selected_index = question["options"].index(selected)







                                                  if selected_index == question["answer"]:



                                                            score += 1







                              total = len(st.session_state.quiz)



                              percentage = score / total * 100 if total else 0







                              st.session_state.quiz_score = score



                              st.session_state.quiz_submitted = True







                              if not st.session_state.quiz_saved:







                                        save_quiz_attempt(



                                                  user_id,



                                                  score,



                                                  total,



                                                  percentage,



                                                  difficulty



                                        )







                                        st.session_state.quiz_saved = True







                              st.rerun()







                    if st.session_state.quiz_submitted:







                              score = st.session_state.quiz_score



                              total = len(st.session_state.quiz)



                              percentage = score / total * 100 if total else 0







                              st.subheader("📊 Your Result")







                              col1, col2, col3 = st.columns(3)







                              col1.metric("Correct Answers", score)



                              col2.metric("Total Questions", total)



                              col3.metric("Accuracy", f"{percentage:.1f}%")







                              st.progress(percentage / 100)







                              for number, question in enumerate(st.session_state.quiz):







                                        st.markdown(



                                                  f"**Q{number + 1}. {question['question']}**"



                                        )







                                        correct = question["options"][question["answer"]]







                                        st.write(f"Correct answer: {correct}")







                                        st.write(



                                                  question.get("explanation", "No explanation available.")



                                        )







                                        st.divider()















if page == "📄 Question Paper":

          # =====================================================



          # QUESTION PAPER GENERATOR



          # =====================================================







          st.sidebar.divider()



          st.sidebar.subheader("📄 Question Paper Generator")







          paper_subject = st.sidebar.text_input(



                    "Subject",



                    value="DBMS"



          )







          paper_marks = st.sidebar.selectbox(



                    "Maximum Marks",



                    [30, 50, 60, 70, 100]



          )







          paper_duration = st.sidebar.selectbox(



                    "Exam Duration",



                    ["1 Hour", "2 Hours", "3 Hours"]



          )







          paper_difficulty = st.sidebar.selectbox(



                    "Paper Difficulty",



                    ["Easy", "Medium", "Hard"],



                    key="paper_difficulty"



          )







          if st.sidebar.button("📄 Generate Question Paper"):







                    if not st.session_state.full_text:



                              st.sidebar.error("Pehle PDF upload karo.")







                    else:



                              prompt = f"""



          You are a college professor.







          Create a university-style question paper using the study material.







          Subject: {paper_subject}



          Maximum Marks: {paper_marks}



          Duration: {paper_duration}



          Difficulty: {paper_difficulty}







          Use:



          SECTION A: Short/objective questions



          SECTION B: Medium descriptive questions



          SECTION C: Long-answer questions







          Rules:



          1. Target total marks must be exactly {paper_marks}.



          2. Mention marks for every question.



          3. Include general instructions.



          4. Avoid duplicate questions.



          5. Do not provide answers.



          6. Use only the supplied study material.



          7. Return the paper only.







          STUDY MATERIAL:



          {st.session_state.full_text}



          """







                              try:



                                        with st.spinner("Generating question paper..."):







                                                  response = client.models.generate_content(



                                                            model=MODEL,



                                                            contents=prompt



                                                  )







                                                  st.session_state.question_paper = response.text



                                                  st.session_state.paper_generated = True







                              except Exception as error:



                                        st.sidebar.error("Question paper generate nahi hua.")



                                        st.sidebar.code(str(error))











          # =====================================================



          # QUESTION PAPER PDF



          # =====================================================







          def build_question_paper_pdf(



                    paper_text,



                    subject,



                    marks,



                    duration,



                    difficulty



          ):







                    buffer = io.BytesIO()







                    doc = SimpleDocTemplate(



                              buffer,



                              pagesize=A4,



                              rightMargin=20 * mm,



                              leftMargin=20 * mm,



                              topMargin=18 * mm,



                              bottomMargin=18 * mm,



                              title=f"{subject} Question Paper",



                              author="AI Virtual Teaching Assistant"



                    )







                    styles = getSampleStyleSheet()







                    title_style = ParagraphStyle(



                              "PaperTitle",



                              parent=styles["Title"],



                              fontName="Helvetica-Bold",



                              fontSize=16,



                              leading=20,



                              alignment=TA_CENTER,



                              textColor=colors.HexColor("#17365D"),



                              spaceAfter=5 * mm



                    )







                    meta_style = ParagraphStyle(



                              "PaperMeta",



                              parent=styles["Normal"],



                              fontSize=10,



                              leading=14,



                              alignment=TA_CENTER,



                              spaceAfter=2 * mm



                    )







                    section_style = ParagraphStyle(



                              "PaperSection",



                              parent=styles["Heading2"],



                              fontName="Helvetica-Bold",



                              fontSize=12,



                              leading=15,



                              textColor=colors.HexColor("#17365D"),



                              spaceBefore=4 * mm,



                              spaceAfter=2 * mm,



                              keepWithNext=True



                    )







                    body_style = ParagraphStyle(



                              "PaperBody",



                              parent=styles["BodyText"],



                              fontName="Helvetica",



                              fontSize=10,



                              leading=14,



                              spaceAfter=2 * mm



                    )







                    story = [



                              Paragraph("AI VIRTUAL TEACHING ASSISTANT", title_style),



                              Paragraph(escape(str(subject)), meta_style),



                              Paragraph(



                                        f"Maximum Marks: {escape(str(marks))}"



                                        f" | Duration: {escape(str(duration))}",



                                        meta_style



                              ),



                              Paragraph(



                                        f"Difficulty: {escape(str(difficulty))}",



                                        meta_style



                              ),



                              Spacer(1, 3 * mm),



                              HRFlowable(



                                        width="100%",



                                        thickness=1,



                                        color=colors.HexColor("#17365D")



                              ),



                              Spacer(1, 4 * mm)



                    ]







                    for raw_line in paper_text.splitlines():







                              line = raw_line.strip()







                              if not line:



                                        story.append(Spacer(1, 1.5 * mm))



                                        continue







                              clean_line = line.strip("# ")



                              clean_line = clean_line.replace("**", "")



                              clean_line = clean_line.replace("__", "")







                              upper_line = clean_line.upper()







                              if (



                                        upper_line.startswith("SECTION ")



                                        or upper_line in ["GENERAL INSTRUCTIONS", "INSTRUCTIONS"]



                              ):



                                        story.append(



                                                  Paragraph(escape(clean_line), section_style)



                                        )







                              else:



                                        story.append(



                                                  Paragraph(escape(clean_line), body_style)



                                        )







                    def add_page_number(canvas, document):



                              canvas.saveState()



                              canvas.setFont("Helvetica", 8)



                              canvas.setFillColor(colors.grey)







                              canvas.drawCentredString(



                                        A4[0] / 2,



                                        10 * mm,



                                        f"Page {document.page}"



                              )







                              canvas.restoreState()







                    doc.build(



                              story,



                              onFirstPage=add_page_number,



                              onLaterPages=add_page_number



                    )







                    buffer.seek(0)



                    return buffer.getvalue()











          if st.session_state.paper_generated:







                    st.header("📄 Generated Question Paper")







                    st.markdown(st.session_state.question_paper)







                    try:



                              pdf_bytes = build_question_paper_pdf(



                                        st.session_state.question_paper,



                                        paper_subject,



                                        paper_marks,



                                        paper_duration,



                                        paper_difficulty



                              )







                              safe_subject = re.sub(



                                        r"[^A-Za-z0-9_-]+",



                                        "_",



                                        paper_subject.strip()



                              ).strip("_") or "Question_Paper"







                              st.download_button(



                                        "📥 Download Question Paper PDF",



                                        data=pdf_bytes,



                                        file_name=f"{safe_subject}_Question_Paper.pdf",



                                        mime="application/pdf"



                              )







                    except Exception as error:



                              st.error("PDF create nahi ho paya.")



                              st.code(str(error))















if page == "💬 AI Chat":

          # =====================================================



          # AI CHATBOT WITH RAG



          # =====================================================







          if not st.session_state.messages:

                    st.markdown(

                              """<div class="ui-chat-hero"><div class="ui-chat-pill">✦ YOUR AI STUDY PARTNER</div><div class="ui-chat-title">What do you want to<br>learn today?</div><div class="ui-chat-sub">Ask a question, understand a difficult concept, or get help with your uploaded study PDFs.</div></div>""",

                              unsafe_allow_html=True,

                    )

          else:

                    st.markdown("### 💬 Your AI Study Assistant")



          for message in st.session_state.messages:







                    with st.chat_message(message["role"]):



                              st.markdown(message["content"])











          question = st.chat_input(



                    "Ask me anything..."



          )







          if question:







                    st.session_state.messages.append({



                              "role": "user",



                              "content": question



                    })







                    with st.chat_message("user"):



                              st.markdown(question)







                    context = ""







                    if (



                              st.session_state.index is not None



                              and st.session_state.chunks



                    ):







                              try:



                                        with st.spinner("Searching study material..."):







                                                  question_embedding = client.models.embed_content(



                                                            model="gemini-embedding-001",



                                                            contents=question,



                                                            config=types.EmbedContentConfig(



                                                                      task_type="RETRIEVAL_QUERY",



                                                                      output_dimensionality=768



                                                            )



                                                  )







                                                  query_vector = np.array(



                                                            [question_embedding.embeddings[0].values],



                                                            dtype="float32"



                                                  )







                                                  faiss.normalize_L2(query_vector)







                                                  k = min(5, len(st.session_state.chunks))







                                                  _, indices = st.session_state.index.search(



                                                            query_vector,



                                                            k



                                                  )







                                                  relevant_chunks = [



                                                            st.session_state.chunks[i]



                                                            for i in indices[0]



                                                            if i >= 0



                                                  ]







                                                  context = "\n\n---\n\n".join(relevant_chunks)







                              except Exception as error:



                                        st.warning("Study material search failed.")



                                        st.code(str(error))







                    prompt = f"""



          You are an intelligent AI Virtual Teaching Assistant.







          Help a college CSE student with:



          DBMS, Operating Systems, Computer Organization,



          Software Engineering, Mathematics, Java, Python,



          DSA, GATE and academic questions.







          Use uploaded study material when relevant.



          If the question is outside the material, answer using general knowledge.



          Give exam-friendly explanations and working code when appropriate.







          STUDY MATERIAL:



          {context}







          STUDENT QUESTION:



          {question}



          """







                    with st.chat_message("assistant"):







                              with st.spinner("Gemini is thinking..."):







                                        try:



                                                  response = client.models.generate_content(



                                                            model=MODEL,



                                                            contents=prompt



                                                  )







                                                  answer = response.text or "No response received."



                                                  st.markdown(answer)







                                        except Exception as error:



                                                  answer = "Gemini API error."



                                                  st.error(answer)



                                                  st.code(str(error))







                    st.session_state.messages.append({



                              "role": "assistant",



                              "content": answer



                    })