# 🎬 MediaFlow – YouTube Video & Audio Downloader

### 🚀 Simple Online Media Downloader Built with Python & Streamlit

**MediaFlow** is a user-friendly web application built with Python and Streamlit that allows users to download supported YouTube videos and audio in their preferred quality.

The application provides a clean interface with Light Mode and Dark Mode, media information previews, quality selection, download progress, and a result section where users can play or download the processed media.

---

# 🚀 Project Overview

MediaFlow provides a simple workflow for downloading supported media.

```text
Open MediaFlow
      ↓
Enter YouTube URL
      ↓
Fetch Video Information
      ↓
Choose Media Type
      ↓
Select Quality
      ↓
Start Download
      ↓
Preview Result
      ↓
Download File
```

---

# ✨ Features

- 🎬 Download supported YouTube videos
- 🎵 Extract and download audio
- 🎥 Multiple video quality options
- 🔊 Multiple audio bitrate options
- 🔗 YouTube URL input and validation
- 🖼️ Video information preview
- 📊 Download progress tracking
- ▶️ Preview downloaded video or audio
- 📥 Download the processed media file
- 🌙 Dark Mode
- ☀️ Light Mode
- 🎨 Clean and user-friendly interface
- 📱 Responsive layout
- ⚡ Simple browser-based experience
- 🐍 Python-based application
- 🧰 FFmpeg integration for media conversion

**Note:** Download availability and supported formats depend on the source, selected quality, and the application's current configuration.

---

# 🧠 How It Works

## 1️⃣ Open the Application

Open MediaFlow in your browser.

The application displays a simple interface for entering a supported YouTube URL.

---

## 2️⃣ Enter a YouTube URL

Paste the URL of the video you want to process.

Example:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

The application validates the URL before attempting to retrieve media information.

---

## 3️⃣ Fetch Media Information

MediaFlow uses `yt-dlp` to retrieve available information, such as:

- Video title
- Duration
- Available formats
- Available video resolutions, when supported

---

## 4️⃣ Choose Video or Audio

Users can select the required output type.

**Video Download**

```text
YouTube URL
     ↓
Select Video Quality
     ↓
Download Video
     ↓
Save Video File
```

**Audio Download**

```text
YouTube URL
     ↓
Select Audio Bitrate
     ↓
Extract Audio
     ↓
Convert to MP3
     ↓
Save Audio File
```

MP3 conversion requires FFmpeg.

---

## 5️⃣ Preview the Result

After processing completes, the application displays a result section.

Users can:

- ▶️ Play the downloaded video
- 🎧 Listen to the extracted audio
- 📥 Download the output file

---

# 🛠️ Technologies Used

## Programming Language

- Python

## Frontend & User Interface

- Streamlit
- HTML
- CSS
- JavaScript

## Media Processing

- yt-dlp
- FFmpeg

## Python Libraries

- Streamlit
- yt-dlp
- Python Standard Library

## Version Control

- Git
- GitHub

## Deployment

- Streamlit Community Cloud (optional)

---

# 📁 Project Structure

```text
mediaflow-downloader/
│
├── app.py
│
├── requirements.txt
│
├── packages.txt
│
└── README.md
```

### File Description

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application, user interface, media processing and download workflow |
| `requirements.txt` | Python dependencies required to run the application |
| `packages.txt` | System packages required for deployment, including FFmpeg |
| `README.md` | Project documentation and setup instructions |

This structure describes the main repository files. Additional files or folders may be included as the project develops.

---

# 💻 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/shekinapilla4809/mediaflow-downloader.git
```

---

## 2️⃣ Open the Project Folder

```bash
cd mediaflow-downloader
```

---

## 3️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

---

## 4️⃣ Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 5️⃣ Install FFmpeg

FFmpeg is required for audio extraction, MP3 conversion, and certain media-processing operations.

Verify the installation:

```bash
ffmpeg -version
```

If the command is not recognized, install FFmpeg and configure it in your system's PATH.

---

## 6️⃣ Run the Application

```bash
streamlit run app.py
```

The application will normally open in your default browser.

Local URL:

```text
http://localhost:8501
```

---

# 📦 Requirements

The project uses the following main dependencies.

### `requirements.txt`

```text
streamlit>=1.40,<2.0
yt-dlp
```

### `packages.txt`

```text
ffmpeg
```

Install the dependencies before running the application.

---

# 🎨 Theme Support

MediaFlow provides two interface themes.

### ☀️ Light Mode

A bright interface with readable text and controls.

### 🌙 Dark Mode

A dark interface designed for comfortable viewing.

Users can switch between themes using the theme toggle button in the application.

---

# 🎥 Video Download

The video workflow allows users to:

- Enter a supported YouTube URL
- Retrieve video information
- Select an available video quality
- Process the video
- Preview the result
- Download the output file

The available resolutions depend on the formats provided by the source and supported by the application.

---

# 🎵 Audio Download

The audio workflow allows users to:

- Enter a supported YouTube URL
- Select an available audio bitrate
- Extract audio using `yt-dlp`
- Convert audio to MP3 when supported
- Preview the audio
- Download the resulting file

Audio conversion depends on FFmpeg being installed and available.

---

# ☁️ Deployment

MediaFlow can be deployed using **Streamlit Community Cloud**, subject to the hosting platform's current limits and policies.

General deployment steps:

1. Push the project files to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the `mediaflow-downloader` repository.
5. Select `app.py` as the main application file.
6. Deploy the application.

Ensure the required Python dependencies and FFmpeg system package are configured correctly.

**Important:** Free hosting environments may have memory, execution-time, storage, and download-size limitations. Large media downloads may fail if they exceed the platform's available resources.

---

# 🎯 Problem Statement

Finding a simple way to process online video and audio can be difficult when users have to work with complicated command-line tools or multiple applications.

A lightweight interface can make media processing easier by bringing URL input, quality selection, progress tracking, preview, and file downloads together in one place.

---

# 💡 Proposed Solution

MediaFlow provides a straightforward interface built with Streamlit and Python.

By integrating `yt-dlp` with FFmpeg, the application supports configured video downloads and audio extraction through a simple browser-based workflow.

The interface focuses on usability, readable controls, theme selection, and easy access to processed results.

---

# 🌟 Key Benefits

- Easy-to-use interface
- Video and audio processing in one application
- Quality selection
- Audio bitrate selection
- Media preview before saving
- Light and Dark themes
- Python-based implementation
- Simple local setup
- GitHub-based project management
- Optional cloud deployment

---

# 🔮 Future Enhancements

Possible future improvements include:

- 📋 Download history
- 📦 Batch URL processing
- 🎧 Additional audio output formats
- 🎞️ More video format options
- 📊 Improved progress reporting
- 🗂️ Download history management
- 🌐 Additional source support where permitted
- 📱 Improved mobile interface
- ⚙️ Advanced media settings
- ☁️ Configurable cloud storage

These are potential enhancements and may not be available in the current version.

---

# ⚖️ Responsible Use

MediaFlow is intended for lawful media processing and personal use where permitted.

Users are responsible for complying with applicable laws, copyright requirements, YouTube's Terms of Service, and the permissions associated with the content they access.

Only download content that you own, have permission to download, or are otherwise legally permitted to access and save. Do not use the application to bypass access restrictions or download protected content without authorization.

---

# 👩‍💻 Developer

### Shekina Pilla

**B.Tech – Computer Science & Engineering (Data Science)**

### Areas of Interest

- Artificial Intelligence
- Python Development
- Full Stack Development
- Web Applications
- Data Science
- Cloud Applications

---

# 🙏 Acknowledgements

This project uses:

- Python
- Streamlit
- yt-dlp
- FFmpeg
- HTML, CSS and JavaScript

Thanks to the developers and maintainers of these open-source technologies.

---

# 📜 License

No specific license is declared here. If you intend to distribute or allow others to reuse this project, consider adding an appropriate `LICENSE` file and reviewing the licenses of its dependencies.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ star on GitHub.

Thank you for visiting **MediaFlow – YouTube Video & Audio Downloader**! 🎬🎵
