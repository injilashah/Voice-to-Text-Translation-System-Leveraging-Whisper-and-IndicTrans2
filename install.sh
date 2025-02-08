#!/bin/bash

echo "Updating package list..."
sudo apt update

echo "Installing required system dependencies..."
sudo apt install -y git wget ffmpeg  # Added ffmpeg

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
pip install transformers torch numpy gitpython  
pip install whisper  # Explicitly installing Whisper
pip install bitsandbytes accelerate 
pip install gradio
pip install yt_dlp
echo "Cloning IndicTrans2 repository..."
if [ ! -d "IndicTrans2" ]; then
    git clone https://github.com/AI4Bharat/IndicTrans2
else
    echo "IndicTrans2 already exists, skipping clone."
fi

echo "Navigating to IndicTrans2 directory..."
cd IndicTrans2/huggingface_interface || exit

echo "Running IndicTrans2 install script..."
bash install.sh

echo "Setup complete! You can now use Whisper, IndicTrans2, and Gradio."
