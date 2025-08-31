import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="GlucoShe", 
    page_icon="⚕️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS with modern design
st.markdown("""
<style>
/* CSS Variables for consistent theming */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #10b981;
    --danger: #ef4444;
    --warning: #f59e0b;
    --dark: #1f2937;
    --light: #f9fafb;
    --gray: #9ca3af;
    --card-bg: rgba(255, 255, 255, 0.1);
    --glass-bg: rgba(255, 255, 255, 0.15);
    --glass-border: rgba(255, 255, 255, 0.2);
    --text-primary: rgba(255, 255, 255, 0.95);
    --text-secondary: rgba(255, 255, 255, 0.7);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
    overflow-x: hidden;
}

.main {
    padding: 1rem;
}

/* Header styling */
.header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    padding: 2rem 1.5rem;
    border-radius: 24px;
    margin-bottom: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    position: relative;
    overflow: hidden;
    text-align: center;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    animation: fadeIn 0.8s ease-out;
}

.header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    animation: pulse 18s infinite linear;
}

@keyframes pulse {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.header h1 {
    font-size: 2.8rem;
    margin-bottom: 0.8rem;
    font-weight: 800;
    position: relative;
    z-index: 2;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header p {
    font-size: 1.2rem;
    opacity: 0.9;
    position: relative;
    z-index: 2;
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto;
}

/* Card styling - Glassmorphism effect */
.card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--glass-border);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    overflow: hidden;
    position: relative;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.5s ease;
}

.card:hover::before {
    transform: scaleX(1);
}

.card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.card h2 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    font-size: 1.7rem;
    font-weight: 700;
    position: relative;
    display: inline-block;
}

.card h2::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 40px;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    border-radius: 3px;
    transition: width 0.3s ease;
}

.card:hover h2::after {
    width: 100px;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 16px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
    text-align: center;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3);
    width: 100%;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: all 0.6s ease;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(79, 70, 229, 0.5);
}

/* Input field styling */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    color: var(--text-primary);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    font-size: 1rem;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-2px);
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

/* Slider styling */
.stSlider > div > div {
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid var(--glass-border);
    padding: 1rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stSlider > div > div:hover {
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-2px);
}

/* Result styling */
.result {
    padding: 2rem;
    border-radius: 20px;
    margin: 2rem 0;
    text-align: center;
    font-size: 1.3rem;
    font-weight: 600;
    animation: fadeInUp 0.6s ease;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    transform-origin: center;
}

@keyframes fadeInUp {
    from { 
        opacity: 0; 
        transform: translateY(20px) scale(0.95);
    }
    to { 
        opacity: 1; 
        transform: translateY(0) scale(1);
    }
}

.success {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10b981;
    box-shadow: 0 12px 30px rgba(16, 185, 129, 0.2);
}

.warning {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #f59e0b;
    box-shadow: 0 12px 30px rgba(245, 158, 11, 0.2);
}

.danger {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #ef4444;
    box-shadow: 0 12px 30px rgba(239, 68, 68, 0.2);
}

/* Chart container */
.chart-container {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--glass-border);
    transition: all 0.4s ease;
}

.chart-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

/* Tips styling */
.tips-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.tip-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid var(--glass-border);
    position: relative;
    overflow: hidden;
}

.tip-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(to bottom, var(--primary), var(--secondary));
    transition: width 0.3s ease;
}

.tip-card:hover::before {
    width: 8px;
}

.tip-card:hover {
    transform: translateY(-8px) rotate(1deg);
    box-shadow: 0 20px 50px rgba(0,0,0,0.2);
}

.tip-card h3 {
    color: var(--text-primary);
    margin-bottom: 1rem;
    font-size: 1.4rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.tip-card p {
    color: var(--text-secondary);
    line-height: 1.7;
    font-size: 1.05rem;
}

/* Risk indicator */
.risk-meter {
    width: 100%;
    height: 30px;
    background: rgba(243, 244, 246, 0.15);
    border-radius: 16px;
    overflow: hidden;
    margin: 2rem 0;
    position: relative;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);
}

.risk-level {
    height: 100%;
    border-radius: 16px;
    transition: width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}

.risk-level::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Metric cards */
.metric-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    text-align: center;
    border: 1px solid var(--glass-border);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.5s ease;
}

.metric-card:hover::before {
    transform: scaleX(1);
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0.8rem 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.metric-label {
    color: var(--text-secondary);
    font-size: 1rem;
    font-weight: 500;
}

/* Form elements styling */
.stSlider {
    margin-bottom: 1.5rem;
}

.stSlider div[data-testid="stSlider"] > div {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    transition: all 0.3s ease;
}

.stSlider div[data-testid="stSlider"] > div:hover {
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-2px);
}

.stSlider div[data-testid="stSlider"] > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
}

/* History section styling */
.history-item {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 1px solid var(--glass-border);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.history-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(to bottom, var(--primary), var(--secondary));
    transition: width 0.3s ease;
}

.history-item:hover::before {
    width: 8px;
}

.history-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

.history-date {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-bottom: 0.8rem;
}

.history-risk {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.8rem;
    background: transparent;
    border-bottom: 1px solid var(--glass-border);
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px 16px 0 0;
    padding: 1rem 1.5rem;
    font-weight: 600;
    color: var(--text-secondary);
    border: 1px solid var(--glass-border);
    border-bottom: none;
    transition: all 0.3s ease;
    margin-bottom: -1px;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.15);
    color: var(--text-primary);
    transform: translateY(-2px);
}

.stTabs [aria-selected="true"] {
    background: rgba(255, 255, 255, 0.2);
    color: var(--text-primary);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transform: translateY(-2px);
}

/* Progress bar styling */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
    border-radius: 10px;
}

/* Checkbox styling */
.stCheckbox [data-baseweb="checkbox"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid var(--glass-border);
    border-radius: 6px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

.stCheckbox [data-baseweb="checkbox"]:hover {
    background: rgba(255, 255, 255, 0.12);
}

.stCheckbox [aria-checked="true"] [data-baseweb="checkbox"] {
    background: var(--primary);
    border-color: var(--primary);
}

/* Expander styling */
.stExpander {
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

.stExpander summary {
    padding: 1.2rem 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
}

.stExpander div {
    padding: 1rem 1.5rem;
}

/* Responsive adjustments for mobile */
@media (max-width: 768px) {
    .main {
        padding: 0.8rem;
    }
    
    .header {
        padding: 1.5rem 1rem;
        margin-bottom: 1.5rem;
        border-radius: 20px;
    }
    
    .header h1 {
        font-size: 2.2rem;
    }
    
    .header p {
        font-size: 1rem;
    }
    
    .card {
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 20px;
    }
    
    .card h2 {
        font-size: 1.5rem;
    }
    
    .result {
        padding: 1.5rem;
        font-size: 1.1rem;
        border-radius: 18px;
    }
    
    .chart-container {
        padding: 1.5rem;
        border-radius: 20px;
    }
    
    .stButton > button {
        padding: 0.9rem 1.5rem;
        font-size: 1rem;
        border-radius: 14px;
    }
    
    .metric-card {
        padding: 1.2rem;
        border-radius: 18px;
    }
    
    .metric-value {
        font-size: 1.8rem;
    }
    
    .tip-card {
        padding: 1.5rem;
        border-radius: 18px;
    }
    
    .tip-card h3 {
        font-size: 1.2rem;
    }
    
    .history-item {
        padding: 1.2rem;
        border-radius: 18px;
    }
    
    .history-risk {
        font-size: 1.1rem;
    }
    
    /* Input fields on mobile */
    .stTextInput > div > div > input {
        padding: 0.9rem 1rem;
        font-size: 0.95rem;
    }
    
    .tips-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
}

/* Extra small devices */
@media (max-width: 480px) {
    .header h1 {
        font-size: 1.9rem;
    }
    
    .header p {
        font-size: 0.9rem;
    }
    
    .card {
        padding: 1.2rem;
    }
    
    .card h2 {
        font-size: 1.3rem;
    }
    
    .metric-value {
        font-size: 1.6rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
    }
}

/* Tabs styling for mobile */
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        flex: 1;
        min-width: 100px;
        border-radius: 12px 12px 0 0;
    }
}

/* Plotly chart responsiveness */
.js-plotly-plot .plotly, .plotly-container {
    width: 100% !important;
    border-radius: 16px;
}

/* Streamlit column adjustments for mobile */
@media (max-width: 768px) {
    .stColumn {
        min-width: 100% !important;
    }
    
    /* Force single column layout on mobile */
    [data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
    }
}

/* Loading animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading {
    display: inline-block;
    width: 24px;
    height: 24px;
    border: 3px solid rgba(99, 102, 241, 0.3);
    border-radius: 50%;
    border-top-color: var(--primary);
    animation: spin 1s ease-in-out infinite;
}

/* Improve form elements for mobile */
@media (max-width: 768px) {
    .stSlider {
        margin-bottom: 1.2rem;
    }
    
    .stSlider [data-testid="stTickBar"] {
        font-size: 0.8rem;
    }
    
    .stMetric {
        padding: 1rem;
    }
    
    .stMetric > div {
        padding: 0.6rem;
    }
}

/* Ensure text doesn't overflow on small screens */
.metric-value, .metric-label, .tip-card h3, .tip-card p, .history-date, .history-risk {
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    border: 2px solid transparent;
    background-clip: padding-box;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Input container styling */
.input-container {
    margin-bottom: 1.5rem;
}

.input-container label {
    display: block;
    margin-bottom: 0.6rem;
    color: var(--text-primary);
    font-weight: 500;
}

.input-row {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 1.2rem;
}

.input-field {
    flex: 1;
}

.input-toggle {
    display: flex;
    align-items: center;
    margin-top: 0.8rem;
    color: var(--text-secondary);
    font-size: 0.95rem;
    cursor: pointer;
    transition: color 0.3s ease;
}

.input-toggle:hover {
    color: var(--text-primary);
}

.input-toggle input {
    margin-right: 0.6rem;
}

/* Floating animation for elements */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.float-animation {
    animation: float 6s ease-in-out infinite;
}

/* Fade in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.8s ease forwards;
}

/* Staggered animation for cards */
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
.card:nth-child(5) { animation-delay: 0.5s; }

/* Gradient text */
.gradient-text {
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Focus states for accessibility */
button:focus, input:focus, select:focus, textarea:focus {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}

/* Selection color */
::selection {
    background: rgba(99, 102, 241, 0.3);
}

::-moz-selection {
    background: rgba(99, 102, 241, 0.3);
}

/* Pulse animation for important elements */
@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
    70% { box-shadow: 0 0 0 15px rgba(99, 102, 241, 0); }
    100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
}

.pulse-glow {
    animation: pulse-glow 2s infinite;
}

/* Hover lift effect */
.hover-lift {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for history and input mode
if 'history' not in st.session_state:
    st.session_state.history = []

if 'keyboard_input' not in st.session_state:
    st.session_state.keyboard_input = False

# Function to save prediction to history
def save_to_history(input_data, risk_score, risk_category):
    history_item = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'inputs': input_data,
        'risk_score': risk_score,
        'risk_category': risk_category
    }
    
    # Add to beginning of history (newest first)
    st.session_state.history.insert(0, history_item)
    
    # Keep only the last 10 entries
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

# Function to validate and convert input values
def validate_input(value, min_val, max_val, default, input_type=float):
    try:
        num_value = input_type(value)
        if min_val <= num_value <= max_val:
            return num_value
        else:
            return default
    except (ValueError, TypeError):
        return default

# App layout
st.markdown('<div class="header"><h1>🩺 GlucoShe💉🩸</h1><p>Where Women’s Wellness Meets AI Precision</p></div>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prediction", "Dashboard", "Health Tips", "History", "About"])

with tab1:
    # Use a single column on mobile, two columns on larger screens
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card"><h2>Health Assessment</h2></div>', unsafe_allow_html=True)
        
        # Toggle between slider and keyboard input
        st.markdown('<div class="input-toggle">', unsafe_allow_html=True)
        keyboard_input = st.checkbox("Use keyboard input instead of sliders", value=st.session_state.keyboard_input)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if keyboard_input:
            st.session_state.keyboard_input = True
            
            # Input form with text inputs
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                Pregnancies = st.text_input("Pregnancies", value="0", help="Number of times pregnant (0-20)")
                Glucose = st.text_input("Glucose Level", value="100", help="Plasma glucose concentration (0-200 mg/dL)")
                BloodPressure = st.text_input("Blood Pressure", value="70", help="Diastolic blood pressure (0-130 mm Hg)")
                SkinThickness = st.text_input("Skin Thickness", value="20", help="Triceps skin fold thickness (0-100 mm)")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with form_col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                Insulin = st.text_input("Insulin", value="80", help="2-Hour serum insulin (0-850 mu U/ml)")
                BMI = st.text_input("BMI", value="25.0", help="Body mass index (0.0-70.0)")
                DiabetesPedigreeFunction = st.text_input("Diabetes Pedigree", value="0.5", help="Diabetes pedigree function (0.0-2.5)")
                Age = st.text_input("Age", value="30", help="Age in years (0-100)")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Validate and convert inputs
            Pregnancies = validate_input(Pregnancies, 0, 20, 0, int)
            Glucose = validate_input(Glucose, 0, 200, 100, int)
            BloodPressure = validate_input(BloodPressure, 0, 130, 70, int)
            SkinThickness = validate_input(SkinThickness, 0, 100, 20, int)
            Insulin = validate_input(Insulin, 0, 850, 80, int)
            BMI = validate_input(BMI, 0.0, 70.0, 25.0, float)
            DiabetesPedigreeFunction = validate_input(DiabetesPedigreeFunction, 0.0, 2.5, 0.5, float)
            Age = validate_input(Age, 0, 100, 30, int)
            
        else:
            st.session_state.keyboard_input = False
            
            # Input form with sliders
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                Pregnancies = st.slider("Pregnancies", 0, 20, 0, help="Number of times pregnant")
                Glucose = st.slider("Glucose Level", 0, 200, 100, help="Plasma glucose concentration (mg/dL)")
                BloodPressure = st.slider("Blood Pressure", 0, 130, 70, help="Diastolic blood pressure (mm Hg)")
                SkinThickness = st.slider("Skin Thickness", 0, 100, 20, help="Triceps skin fold thickness (mm)")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with form_col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                Insulin = st.slider("Insulin", 0, 850, 80, help="2-Hour serum insulin (mu U/ml)")
                BMI = st.slider("BMI", 0.0, 70.0, 25.0, help="Body mass index (weight in kg/(height in m)^2)")
                DiabetesPedigreeFunction = st.slider("Diabetes Pedigree", 0.0, 2.5, 0.5, help="Diabetes pedigree function")
                Age = st.slider("Age", 0, 100, 30, help="Age in years")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction button
        if st.button("Predict Diabetes Risk", type="primary", use_container_width=True):
            # Simulate prediction process
            with st.spinner("Analyzing health data..."):
                time.sleep(1.5)
                
                # Mock prediction logic for demo
                risk_score = (
                    (Glucose - 70) / 130 * 0.3 +
                    (BMI - 18) / 52 * 0.25 +
                    (Age - 20) / 80 * 0.15 +
                    (Pregnancies if Pregnancies > 0 else 0) * 0.1 +
                    (BloodPressure - 60) / 70 * 0.1 +
                    (DiabetesPedigreeFunction - 0.2) / 2.3 * 0.1
                )
                
                risk_score = max(0, min(1, risk_score))
                
                if risk_score < 0.3:
                    risk_category = "Low Risk"
                    st.markdown(f'<div class="result success">✅ Low Risk: Your diabetes risk is {(risk_score*100):.1f}%</div>', unsafe_allow_html=True)
                elif risk_score < 0.7:
                    risk_category = "Moderate Risk"
                    st.markdown(f'<div class="result warning">⚠ Moderate Risk: Your diabetes risk is {(risk_score*100):.1f}%</div>', unsafe_allow_html=True)
                else:
                    risk_category = "High Risk"
                    st.markdown(f'<div class="result danger">🔴 High Risk: Your diabetes risk is {(risk_score*100):.1f}%</div>', unsafe_allow_html=True)
                
                # Save to history
                input_data = {
                    'Pregnancies': Pregnancies,
                    'Glucose': Glucose,
                    'BloodPressure': BloodPressure,
                    'SkinThickness': SkinThickness,
                    'Insulin': Insulin,
                    'BMI': BMI,
                    'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
                    'Age': Age
                }
                
                save_to_history(input_data, risk_score, risk_category)
                
                # Show risk meter
                st.markdown(f'<div class="risk-meter"><div class="risk-level" style="width: {risk_score*100}%; background: {"#10b981" if risk_score < 0.3 else "#f59e0b" if risk_score < 0.7 else "#ef4444"};"></div></div>', unsafe_allow_html=True)
                
                # Risk factors breakdown
                st.subheader("Risk Factors Breakdown")
                
                risk_factors = {
                    "Glucose Level": max(0, (Glucose - 70) / 130),
                    "BMI": max(0, (BMI - 18) / 52),
                    "Age": max(0, (Age - 20) / 80),
                    "Pregnancies": Pregnancies * 0.05,
                    "Blood Pressure": max(0, (BloodPressure - 60) / 70),
                    "Genetic Factor": DiabetesPedigreeFunction / 2.5
                }
                
                # Create a DataFrame for the chart
                risk_df = pd.DataFrame({
                    'Factor': list(risk_factors.keys()),
                    'Contribution': list(risk_factors.values())
                })
                
                # Create a bar chart
                fig = px.bar(risk_df, x='Factor', y='Contribution', 
                             title='Contributions to Diabetes Risk',
                             color='Contribution',
                             color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'])
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # Right column - Health Summary
    with col2:
        st.markdown('<div class="card"><h2>Health Summary</h2></div>', unsafe_allow_html=True)
        
        # Display metrics in a responsive grid
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Glucose", f"{Glucose} mg/dL", help="Normal range: 70-100 mg/dL")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Blood Pressure", f"{BloodPressure} mmHg", help="Normal range: 60-80 mmHg")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with metrics_col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("BMI", f"{BMI}", help="Normal range: 18.5-24.9")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Age", f"{Age} years")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Health status indicators
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Health Status")
        
        # Glucose indicator
        glucose_status = "Normal" if 70 <= Glucose <= 100 else "Pre-diabetic" if 101 <= Glucose <= 125 else "Diabetic"
        glucose_color = "#10b981" if glucose_status == "Normal" else "#f59e0b" if glucose_status == "Pre-diabetic" else "#ef4444"
        st.markdown(f'Glucose: <span style="color:{glucose_color}; font-weight:bold">{glucose_status}</span>', unsafe_allow_html=True)
        st.progress(min(1.0, max(0, (Glucose - 50) / 150)))
        
        # BMI indicator
        bmi_status = "Underweight" if BMI < 18.5 else "Normal" if BMI < 25 else "Overweight" if BMI < 30 else "Obese"
        bmi_color = "#f59e0b" if bmi_status == "Underweight" else "#10b981" if bmi_status == "Normal" else "#f59e0b" if bmi_status == "Overweight" else "#ef4444"
        st.markdown(f'BMI: <span style="color:{bmi_color}; font-weight:bold">{bmi_status}</span>', unsafe_allow_html=True)
        st.progress(min(1.0, max(0, (BMI - 15) / 40)))
        
        # Blood Pressure indicator
        bp_status = "Low" if BloodPressure < 60 else "Normal" if BloodPressure < 80 else "Elevated" if BloodPressure < 90 else "High"
        bp_color = "#f59e0b" if bp_status == "Low" else "#10b981" if bp_status == "Normal" else "#f59e0b" if bp_status == "Elevated" else "#ef4444"
        st.markdown(f'Blood Pressure: <span style="color:{bp_color}; font-weight:bold">{bp_status}</span>', unsafe_allow_html=True)
        st.progress(min(1.0, max(0, (BloodPressure - 50) / 100)))
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card"><h2>Health Dashboard</h2></div>', unsafe_allow_html=True)
    
    # Responsive columns for dashboard
    dash_col1, dash_col2 = st.columns([2, 1])
    
    with dash_col1:
        # Historical trends chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Historical Health Trends")
        
        # Generate sample historical data
        dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M')
        glucose_values = np.random.normal(Glucose, 15, 12)
        bmi_values = np.random.normal(BMI, 2, 12)
        
        trend_df = pd.DataFrame({
            'Date': dates,
            'Glucose': glucose_values,
            'BMI': bmi_values
        })
        
        fig = px.line(trend_df, x='Date', y=['Glucose', 'BMI'], 
                      title='Health Metrics Over Time',
                      labels={'value': 'Measurement', 'variable': 'Metric'})
        
        fig.update_layout(height=400)  # Fixed height for better mobile viewing
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Risk comparison chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Risk Comparison")
        
        # Sample data for comparison
        risk_score_val = risk_score*100 if 'risk_score' in locals() else 25
        comparison_data = {
            'Category': ['Your Risk', 'Average Risk (Same Age)', 'Low Risk Benchmark'],
            'Value': [risk_score_val, 
                     (Age/100)*0.6 if 'Age' in locals() else 30, 
                     10]
        }
        
        comp_df = pd.DataFrame(comparison_data)
        
        fig = px.bar(comp_df, x='Category', y='Value', 
                     title='Diabetes Risk Comparison (%)',
                     color='Category',
                     color_discrete_sequence=['#6366f1', '#8b5cf6', '#10b981'])
        
        fig.update_layout(height=400)  # Fixed height for better mobile viewing
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column for dashboard
    with dash_col2:
        # Health score
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Overall Health Score")
        
        if 'risk_score' in locals():
            health_score = 100 - (risk_score * 100)
        else:
            health_score = 75
            
        st.markdown(f'<div style="text-align: center; font-size: 2.5rem; font-weight: bold; color: {("#10b981" if health_score > 80 else "#f59e0b" if health_score > 60 else "#ef4444")};">{health_score:.0f}/100</div>', unsafe_allow_html=True)
        
        st.metric("Score Trend", "+2.5%", "vs last month")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommendations
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Personalized Recommendations")
        
        recommendations = []
        
        if Glucose > 100:
            recommendations.append("Consider reducing sugar intake")
        if BMI > 25:
            recommendations.append("Aim for 150 mins of exercise weekly")
        if BloodPressure > 80:
            recommendations.append("Reduce sodium in your diet")
        if Age > 45:
            recommendations.append("Schedule annual diabetes screening")
        if not recommendations:
            recommendations.append("Maintain your healthy lifestyle!")
        
        for i, rec in enumerate(recommendations):
            st.markdown(f"{i+1}. {rec}")
            
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card"><h2>Diabetes Prevention Tips</h2></div>', unsafe_allow_html=True)
    
    # Lifestyle tips in a responsive grid
    tips = [
        {
            "title": "Healthy Eating",
            "content": "Focus on whole foods, fruits, vegetables, lean proteins and whole grains. Limit processed foods and sugary beverages.",
            "icon": "🥗"
        },
        {
            "title": "Regular Exercise",
            "content": "Aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week.",
            "icon": "🏃‍♀️"
        },
        {
            "title": "Weight Management",
            "content": "Maintaining a healthy weight can significantly reduce your risk of developing diabetes.",
            "icon": "⚖️"
        },
        {
            "title": "Stress Management",
            "content": "Chronic stress can affect blood sugar levels. Practice relaxation techniques like meditation or yoga.",
            "icon": "🧘‍♀️"
        },
        {
            "title": "Quality Sleep",
            "content": "Aim for 7-9 hours of quality sleep per night. Poor sleep can affect insulin sensitivity.",
            "icon": "😴"
        },
        {
            "title": "Regular Check-ups",
            "content": "Schedule regular health screenings to monitor your blood sugar levels and overall health.",
            "icon": "🩺"
        }
    ]
    
    # Display tips in a responsive grid
    cols = st.columns(2)  # 2 columns on desktop, will stack on mobile
    
    for i, tip in enumerate(tips):
        # This will automatically stack on mobile
        with cols[i % 2]:
            st.markdown(f'<div class="tip-card"><h3>{tip["icon"]} {tip["title"]}</h3><p>{tip["content"]}</p></div>', unsafe_allow_html=True)
    
    # Additional resources
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Additional Resources")
    
    resources = [
        ["INTERNATIONAL DIABETES FEDERATION", "https://idf.org/what-we-do/diabetes-awareness-activities/"],
        ["AMERICAN DIABETES ASSOCIATION", "https://www.diabetes.org"],
        ["WORLD DIABETES FOUNDATION", "https://www.worlddiabetesfoundation.org/what-we-do/projects/wdf07-0295/"],
        ["NUTRITION AND DIET RESOURCES", "https://www.eatright.org"],
        ["NIH", "https://pmc.ncbi.nlm.nih.gov/articles/PMC3395295/"]
    ]
    
    for resource in resources:
        st.markdown(f"- [{resource[0]}]({resource[1]})")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="card"><h2>Prediction History</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.info("No prediction history yet. Make your first prediction on the Prediction tab!")
    else:
        for i, item in enumerate(st.session_state.history):
            risk_color = "#10b981" if item['risk_category'] == "Low Risk" else "#f59e0b" if item['risk_category'] == "Moderate Risk" else "#ef4444"
            
            st.markdown(f'''
            <div class="history-item">
                <div class="history-date">{item['timestamp']}</div>
                <div class="history-risk" style="color: {risk_color};">{item['risk_category']}: {(item['risk_score']*100):.1f}%</div>
                <div>Glucose: {item['inputs']['Glucose']} mg/dL | BMI: {item['inputs']['BMI']} | Age: {item['inputs']['Age']}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Show details on expansion
            with st.expander(f"View Details {i}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Pregnancies: {item['inputs']['Pregnancies']}")
                    st.write(f"Glucose: {item['inputs']['Glucose']} mg/dL")
                    st.write(f"Blood Pressure: {item['inputs']['BloodPressure']} mmHg")
                    st.write(f"Skin Thickness: {item['inputs']['SkinThickness']} mm")
                with col2:
                    st.write(f"Insulin: {item['inputs']['Insulin']} mu U/ml")
                    st.write(f"BMI: {item['inputs']['BMI']}")
                    st.write(f"Diabetes Pedigree: {item['inputs']['DiabetesPedigreeFunction']}")
                    st.write(f"Age: {item['inputs']['Age']} years")
        
        # Clear history button
        if st.button("Clear History", type="secondary"):
            st.session_state.history = []
            st.rerun()

with tab5:
    st.markdown('<div class="card"><h2>About GlucoShe</h2></div>', unsafe_allow_html=True)
    
    st.write("""
    GlucoShe is an advanced health assessment tool designed to evaluate your risk of developing diabetes 
    based on key health indicators. Our system uses machine learning algorithms trained on extensive health data 
    to provide personalized risk assessments and recommendations.
    """)
    
    st.info("""
    *Disclaimer*: This tool is for informational purposes only and is not a substitute for professional medical advice, 
    diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any 
    questions you may have regarding a medical condition.
    """)
    
    st.markdown("### How It Works")
    st.write("""
    1. *Input Health Data*: Enter your basic health metrics including glucose levels, BMI, and age.
    2. *Risk Assessment*: Our algorithm analyzes your data against known risk factors for diabetes.
    3. *Personalized Insights*: Receive your risk score and personalized recommendations for reducing your risk.
    4. *Track Progress*: Use the dashboard to monitor your health metrics over time.
    """)
    
    st.markdown("### Why Monitor Diabetes Risk?")
    st.write("""
    - Early detection of prediabetes can prevent or delay the onset of type 2 diabetes
    - Lifestyle changes are more effective when implemented early
    - Regular monitoring helps maintain awareness of health status
    - Knowledge empowers you to make informed health decisions
    """)

# Footer
st.markdown("---")
st.markdown("""
    <style>
    .footer-glow {
        text-align: center;
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 20px;
        margin-bottom: 10px;
        text-shadow: 0 0 2px #ffffff,
                     0 0 4px #ffffff,
                     0 0 6px #a29bfe,
                     0 0 8px #6c5ce7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: 0.6px;
    }
    </style>

    <div class="footer-glow">
        <p>GlucoShe — Harnessing Technology for Preventive Care</p>
        <p>Developed by Dibyendu Karmahapatra • Strictly for awareness & learning</p>
    </div>
""", unsafe_allow_html=True)


