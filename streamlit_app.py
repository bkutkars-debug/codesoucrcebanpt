import os
import sys
import runpy

# CodeRescue AI - Root Streamlit Launcher for 1-Click Streamlit Cloud Deployment
current_dir = os.path.dirname(os.path.abspath(__file__))
sub_dir = os.path.join(current_dir, "coderescue-ai")
if sub_dir not in sys.path:
    sys.path.insert(0, sub_dir)

app_path = os.path.join(sub_dir, "streamlit_app.py")
runpy.run_path(app_path, run_name="__main__")
