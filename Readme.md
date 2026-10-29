
# 🌈 Ultimate Neon Fractal Animation

A Python project that creates a beautiful neon fractal animation with glowing curves, rainbow colors, and a progressive drawing effect.

## ✨ Features

- Neon blue, purple, pink, and rainbow colors
- Glowing fractal-style curves
- Progressive animation reveal
- Smooth 30 FPS video output
- Landscape resolution: 1024 × 768
- MP4 video export
- WhatsApp-compatible video conversion instructions

## 📋 Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- OpenCV
- NumPy
- FFmpeg (optional, for WhatsApp-compatible video conversion)

## 🚀 Step 1: Install Python Libraries

Open PowerShell or Command Prompt in the project folder and run:

```bash
python -m pip install numpy opencv-python
```

## ▶️ Step 2: Run the Project

Keep `ultimate_neon_fractal.py` inside your project folder.

Run:

```bash
python ultimate_neon_fractal.py
```

Wait until the animation finishes rendering.

The output video should be created in the same folder:

`ultimate_neon_fractal.mp4`

## 🎬 Step 3: Video Settings

The default settings are:

- Resolution: 1024 × 768
- Frame rate: 30 FPS
- Duration: 12 seconds
- Output: `ultimate_neon_fractal.mp4`

You can change these settings near the top of the Python file.

## 📱 Step 4: Make the Video WhatsApp-Compatible

Some devices may not support the original video codec. FFmpeg can convert it to H.264 MP4.

First, install FFmpeg and ensure it is available in your system PATH.

Check the installation:

```bash
ffmpeg -version
```

Then run this command in your project folder:

```bash
ffmpeg -i "ultimate_neon_fractal.mp4" -c:v libx264 -pix_fmt yuv420p -profile:v high -movflags +faststart -an "whatsapp_video.mp4"
```

After conversion, send `whatsapp_video.mp4` through WhatsApp.

Official FFmpeg download page:

https://ffmpeg.org/download.html

## 🛠️ Troubleshooting

### 1. ModuleNotFoundError

Install the required libraries:

```bash
python -m pip install numpy opencv-python
```

### 2. Python command not working

Try:

```bash
py ultimate_neon_fractal.py
```

### 3. Video not created

- Check that the script runs without errors.
- Ensure the project folder is writable.
- Wait until rendering completes.
- Check the terminal for error messages.

### 4. WhatsApp says the file is not supported

Convert the video using the FFmpeg command in Step 4.

## 📁 Project Structure

```text
NeonButterflyProject/
│
├── ultimate_neon_fractal.py
├── README.md
├── ultimate_neon_fractal.mp4
└── whatsapp_video.mp4
```

The two MP4 files will appear after you generate and convert the video.

## 📝 Notes

- The animation is generated locally on your computer.
- Rendering time depends on your computer's performance.
- FFmpeg is only needed if you want to convert the video.
- The script produces a silent video unless audio is added separately.

## 💙 Credits

Created with Python, NumPy, and OpenCV.
