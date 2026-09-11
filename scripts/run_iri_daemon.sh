#!/bin/bash
# Iri Autonomous Voice Loop Daemon Launcher
# AE01M - The Transcending Form

# Set working directory
cd /home/artid1994/Projects/THE_TRANSCENDING_FORM

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment and run Iri voice loop
exec ./.venv/bin/python 04_Cerebellum/voice_interactive_loop.py >> logs/iri_daemon.log 2>&1
