
import html
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components
import yt_dlp


# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MediaFlow | Video & Audio Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MAX_DOWNLOAD_BYTES = 250 * 1024 * 1024

ALLOWED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtube-nocookie.com",
}

DEFAULTS = {
    "theme": "Dark",
    "media_info": None,
    "media_url": "",
    "result": None,
    "download_error": "",
    "download_complete": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# THEME TOGGLE
# =========================================================
def toggle_theme():
    st.session_state.theme = (
        "Light" if st.session_state.theme == "Dark" else "Dark"
    )


# Header row: brand on the left, theme button on the right.
brand_col, theme_col = st.columns([5, 1], vertical_alignment="center")

with brand_col:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="
                background:linear-gradient(135deg,#8B7CFF,#5142C7);
                color:white;width:44px;height:44px;
                border-radius:13px;display:flex;
                align-items:center;justify-content:center;
                font-size:23px;font-weight:800;">
                ▶
            </div>
            <div>
                <div style="font-size:23px;font-weight:850;">
                    MediaFlow
                </div>
                <div style="
                    font-size:11px;font-weight:750;
                    letter-spacing:2px;opacity:.75;">
                    VIDEO &amp; AUDIO STUDIO
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with theme_col:
    theme_label = (
        "☀️ Light Mode"
        if st.session_state.theme == "Dark"
        else "🌙 Dark Mode"
    )

    st.button(
        theme_label,
        key="theme_toggle_button",
        on_click=toggle_theme,
        use_container_width=True,
        help="Switch between light and dark appearance",
    )


# =========================================================
# THEME COLORS
# =========================================================
dark = st.session_state.theme == "Dark"

if dark:
    C = {
        "bg": "#0B1020",
        "panel": "#131B2E",
        "panel2": "#182238",
        "text": "#F1F5F9",
        "muted": "#B4C0D4",
        "border": "#35435E",
        "accent": "#8B7CFF",
        "input": "#111A2C",
        "button_text": "#FFFFFF",
        "hero_glow": "rgba(139,124,255,.15)",
    }
else:
    C = {
        "bg": "#F4F7FC",
        "panel": "#FFFFFF",
        "panel2": "#EAF0FA",
        "text": "#172033",
        "muted": "#4C5B73",
        "border": "#CCD7E8",
        "accent": "#5142C7",
        "input": "#FFFFFF",
        "button_text": "#FFFFFF",
        "hero_glow": "rgba(81,66,199,.08)",
    }


# =========================================================
# THEME-AWARE CSS
# =========================================================
st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: {"dark" if dark else "light"};
    }}

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background: {C["bg"]} !important;
        color: {C["text"]} !important;
    }}

    [data-testid="stHeader"] {{
        background: {C["bg"]} !important;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 1.3rem;
        padding-bottom: 4rem;
    }}

    /* Theme button stays easy to see and click */
    [data-testid="st-key-theme_toggle_button"] button {{
        background: {C["panel"]} !important;
        color: {C["text"]} !important;
        border: 2px solid {C["accent"]} !important;
        border-radius: 13px !important;
        min-height: 44px !important;
        padding: 8px 10px !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        white-space: nowrap !important;
        box-shadow: 0 3px 12px {C["hero_glow"]};
        transition: all .2s ease;
    }}

    [data-testid="st-key-theme_toggle_button"] button:hover {{
        background: {C["accent"]} !important;
        color: #FFFFFF !important;
        border-color: {C["accent"]} !important;
        transform: translateY(-1px);
    }}

    /* Text */
    h1, h2, h3, h4, p, li, label,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: {C["text"]};
    }}

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    .stCaption {{
        color: {C["muted"]} !important;
    }}

    /* Inputs */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea {{
        background: {C["input"]} !important;
        color: {C["text"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        caret-color: {C["accent"]};
    }}

    [data-testid="stTextInput"] input::placeholder {{
        color: {C["muted"]} !important;
        opacity: .8;
    }}

    [data-testid="stSelectbox"] > div > div,
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {{
        color: {C["text"]} !important;
    }}

    [data-testid="stSelectbox"] > div > div {{
        background: {C["input"]} !important;
        border-color: {C["border"]} !important;
    }}

    [data-testid="stRadio"] label p,
    [data-testid="stCheckbox"] label p {{
        color: {C["text"]} !important;
    }}

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {{
        background: {C["panel"]} !important;
        color: {C["text"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        min-height: 44px;
        font-weight: 700;
        transition: all .2s ease;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        border-color: {C["accent"]} !important;
        color: {C["accent"]} !important;
    }}

    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {{
        background: {C["accent"]} !important;
        color: #FFFFFF !important;
        border: 1px solid {C["accent"]} !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover {{
        filter: brightness(1.08);
        color: #FFFFFF !important;
    }}

    /* Hero */
    .hero {{
        background: linear-gradient(
            130deg, {C["panel"]}, {C["panel2"]}
        );
        border: 1px solid {C["border"]};
        border-radius: 24px;
        padding: 30px;
        margin: 22px 0 26px;
        box-shadow: 0 8px 30px {C["hero_glow"]};
    }}

    .eyebrow {{
        color: {C["accent"]} !important;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 2px;
    }}

    .hero-title {{
        color: {C["text"]} !important;
        font-size: clamp(29px, 4vw, 43px);
        line-height: 1.2;
        font-weight: 850;
        margin: 10px 0;
    }}

    .hero-sub {{
        color: {C["muted"]} !important;
        font-size: 16px;
        line-height: 1.8;
    }}

    .surface {{
        background: {C["panel"]};
        color: {C["text"]};
        border: 1px solid {C["border"]};
        border-radius: 18px;
        padding: 22px;
        margin: 10px 0 18px;
        overflow-wrap: anywhere;
    }}

    .pill {{
        display: inline-block;
        padding: 7px 12px;
        border: 1px solid {C["border"]};
        border-radius: 999px;
        color: {C["text"]};
        background: {C["panel"]};
        font-size: 12px;
        font-weight: 650;
        margin: 8px 5px 0 0;
    }}

    .notice {{
        color: {C["muted"]} !important;
        font-size: 13px;
        line-height: 1.8;
    }}

    [data-testid="stProgress"] > div > div > div {{
        background-color: {C["accent"]} !important;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    [data-testid="stMetric"] {{
        background: {C["panel"]};
        border: 1px solid {C["border"]};
        padding: 14px;
        border-radius: 14px;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {{
        color: {C["text"]} !important;
    }}

    hr {{
        border-color: {C["border"]} !important;
    }}

    #result-anchor {{
        scroll-margin-top: 25px;
    }}

    footer {{
        visibility: hidden;
    }}

    @media (max-width: 640px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        .hero {{
            padding: 20px;
        }}

        [data-testid="st-key-theme_toggle_button"] button {{
            font-size: 11px !important;
            padding: 6px !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================
def valid_youtube_url(url):
    try:
        parsed = urlparse(url.strip())

        if parsed.scheme not in ("http", "https"):
            return False

        host = (parsed.hostname or "").lower().rstrip(".")

        if host not in ALLOWED_HOSTS:
            return False

        if host == "youtu.be":
            return bool(parsed.path.strip("/"))

        if parsed.path == "/watch":
            return bool(re.search(r"(?:^|&)v=[^&]+", parsed.query))

        return bool(
            re.match(
                r"^/(shorts|embed|live)/[^/?]+",
                parsed.path,
            )
        )

    except (ValueError, AttributeError):
        return False


def human_size(size):
    if size is None:
        return "Unknown size"

    size = float(size)

    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}"
        size /= 1024

    return "Unknown size"


def human_duration(seconds):
    if seconds is None:
        return "Unknown"

    hours, rem = divmod(int(seconds), 3600)
    minutes, secs = divmod(rem, 60)

    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"

    return f"{minutes}:{secs:02d}"


def safe_filename(name, extension):
    name = re.sub(r'[\\/*?:"<>|]', "", str(name or "media"))
    name = re.sub(r"\s+", " ", name).strip(" .")
    return f"{(name[:100] or 'media')}.{extension}"


def extract_metadata(url):
    options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
        "socket_timeout": 20,
        "retries": 1,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title") or "Untitled media",
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "uploader": info.get("uploader") or "Unknown creator",
        "formats": info.get("formats") or [],
    }


def download_media(url, kind, quality, output_dir, progress_callback):
    """Download media the user is authorized to save."""

    def hook(data):
        if data.get("status") == "downloading":
            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
            )
            downloaded = data.get("downloaded_bytes", 0)
            percent = downloaded / total if total else None

            progress_callback(percent, "Downloading media...")

        elif data.get("status") == "finished":
            progress_callback(
                0.98,
                "Converting / processing media...",
            )

    output_template = str(
        Path(output_dir) / "%(title).100s.%(ext)s"
    )

    options = {
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 30,
        "retries": 2,
        "progress_hooks": [hook],
        "max_filesize": MAX_DOWNLOAD_BYTES,
    }

    if kind == "Video (MP4)":
        if quality == "Best available":
            fmt = (
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
                "/best[ext=mp4]/best"
            )
        else:
            height = int(quality.replace("p", ""))
            fmt = (
                f"bestvideo[height<={height}][ext=mp4]"
                "+bestaudio[ext=m4a]"
                f"/best[height<={height}][ext=mp4]"
                f"/best[height<={height}]"
            )

        options.update({
            "format": fmt,
            "merge_output_format": "mp4",
        })

    else:
        options.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(quality),
            }],
        })

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    files = [
        path
        for path in Path(output_dir).iterdir()
        if path.is_file() and path.stat().st_size > 0
    ]

    extension = ".mp4" if kind == "Video (MP4)" else ".mp3"

    matching = [
        path for path in files
        if path.suffix.lower() == extension
    ]

    if not matching:
        raise RuntimeError(
            "Output file was not found. Check FFmpeg, "
            "available formats, or try another quality."
        )

    output_file = max(
        matching,
        key=lambda path: path.stat().st_mtime,
    )

    if output_file.stat().st_size > MAX_DOWNLOAD_BYTES:
        raise RuntimeError(
            "The resulting file exceeds the 250 MB app limit."
        )

    return output_file


# =========================================================
# HERO SECTION
# =========================================================
st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">YOUR MEDIA WORKSPACE</div>
        <div class="hero-title">Your media, your way.</div>
        <div class="hero-sub">
            Preview media, select video resolution or MP3 bitrate,
            track progress, and access your completed file.
        </div>
        <div style="margin-top:12px;">
            <span class="pill">MP4 Video</span>
            <span class="pill">MP3 Audio</span>
            <span class="pill">Progress Tracking</span>
            <span class="pill">{"Dark" if dark else "Light"} Theme Active</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# URL INPUT
# =========================================================
st.markdown("### 01 · Add your YouTube link")

st.caption(
    "Only download content you own or are authorized to save."
)

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    key="youtube_url_input",
)

left, right = st.columns([3, 1])

with left:
    preview_clicked = st.button(
        "Preview media →",
        type="primary",
        use_container_width=True,
    )

with right:
    clear_clicked = st.button(
        "Clear",
        use_container_width=True,
    )

if clear_clicked:
    st.session_state.media_info = None
    st.session_state.media_url = ""
    st.session_state.result = None
    st.session_state.download_error = ""
    st.session_state.download_complete = False
    st.rerun()

if preview_clicked:
    if not valid_youtube_url(url):
        st.error("Please enter a valid YouTube video URL.")
    else:
        try:
            with st.spinner("Loading media information..."):
                info = extract_metadata(url.strip())

            st.session_state.media_info = info
            st.session_state.media_url = url.strip()
            st.session_state.result = None
            st.session_state.download_error = ""
            st.session_state.download_complete = False

            st.success("Media information loaded.")

        except Exception as exc:
            st.session_state.media_info = None

            st.error(
                "Unable to load this media. It may be private, "
                "restricted, unavailable, or temporarily unsupported."
            )
            st.caption(str(exc)[:400])


# =========================================================
# METADATA + DOWNLOAD OPTIONS
# =========================================================
info = st.session_state.media_info

if info:
    st.markdown("### 02 · Media preview")

    image_col, detail_col = st.columns([1, 2], gap="large")

    with image_col:
        if info.get("thumbnail"):
            st.image(
                info["thumbnail"],
                use_container_width=True,
            )
        else:
            st.info("Thumbnail unavailable.")

    with detail_col:
        st.subheader(info["title"])
        st.caption(f"Creator: {info['uploader']}")

        metric1, metric2 = st.columns(2)

        metric1.metric(
            "Duration",
            human_duration(info["duration"]),
        )

        metric2.metric(
            "Available formats",
            str(len(info["formats"])),
        )

    st.divider()
    st.markdown("### 03 · Choose your format")

    kind = st.radio(
        "Output format",
        ["Video (MP4)", "Audio (MP3)"],
        horizontal=True,
        key="output_kind",
    )

    quality = "Best available"

    if kind == "Video (MP4)":
        available_heights = sorted({
            int(f["height"])
            for f in info["formats"]
            if f.get("height")
            and f.get("vcodec") != "none"
            and int(f["height"]) <= 1080
        }, reverse=True)

        quality_options = ["Best available"] + [
            f"{height}p" for height in available_heights
        ]

        quality = st.selectbox(
            "Video resolution",
            quality_options,
            key="video_quality",
        )

        st.caption(
            "Maximum target resolution. Actual output depends "
            "on source formats and FFmpeg."
        )

    else:
        quality = st.selectbox(
            "Audio quality (MP3 bitrate)",
            options=["128", "192", "256", "320"],
            index=1,
            format_func=lambda value: f"{value} kbps",
            key="audio_quality",
        )

        st.caption(
            "Higher bitrate generally means a larger file. "
            "Upscaling bitrate cannot restore detail missing "
            "from the original audio."
        )

    consent = st.checkbox(
        "I own this content or have permission to download it "
        "and will comply with applicable copyright rules and "
        "platform terms.",
        key="download_permission",
    )

    start_download = st.button(
        "Start download",
        type="primary",
        disabled=not consent,
        use_container_width=True,
    )

    if start_download:
        st.session_state.result = None
        st.session_state.download_error = ""
        st.session_state.download_complete = False

        progress_widget = st.progress(
            0,
            text="Preparing download...",
        )

        status_widget = st.empty()

        def update_progress(percent, message):
            if percent is None:
                status_widget.info(message)
                return

            percent = max(0.0, min(1.0, percent))

            progress_widget.progress(
                int(percent * 100),
                text=message,
            )
            status_widget.info(message)

        work_dir = tempfile.mkdtemp(prefix="mediaflow_")

        try:
            with st.spinner("Processing your media..."):
                output_file = download_media(
                    st.session_state.media_url,
                    kind,
                    quality,
                    work_dir,
                    update_progress,
                )

                file_bytes = output_file.read_bytes()

            st.session_state.result = {
                "data": file_bytes,
                "filename": safe_filename(
                    info["title"],
                    "mp4" if kind == "Video (MP4)" else "mp3",
                ),
                "kind": kind,
                "size": len(file_bytes),
                "title": info["title"],
                "quality": (
                    f"{quality} kbps"
                    if kind == "Audio (MP3)"
                    else quality
                ),
            }

            st.session_state.download_complete = True

            progress_widget.progress(
                100,
                text="Download complete!",
            )

            status_widget.success("Your file is ready.")

        except Exception as exc:
            st.session_state.download_error = str(exc)[:800]

            st.error(
                "Download failed. Check the URL, available formats, "
                "FFmpeg installation, and server limits."
            )

            st.caption(st.session_state.download_error)

        finally:
            shutil.rmtree(work_dir, ignore_errors=True)


# =========================================================
# RESULT SECTION + AUTOMATIC SCROLL
# =========================================================
result = st.session_state.result

if result:
    st.markdown('<div id="result-anchor"></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 04 · Your finished media")

    safe_title = html.escape(result["title"][:180])
    safe_kind = html.escape(result["kind"])
    safe_quality = html.escape(result["quality"])

    st.markdown(
        f"""
        <div class="surface">
            <div style="
                color:{C['accent']};font-size:12px;
                font-weight:850;letter-spacing:1px;">
                DOWNLOAD COMPLETE
            </div>
            <div style="
                font-size:20px;font-weight:800;
                margin:8px 0;color:{C['text']};">
                {safe_title}
            </div>
            <div style="color:{C['muted']};font-size:13px;">
                {safe_kind} · {safe_quality} ·
                {human_size(result['size'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result["kind"] == "Video (MP4)":
        st.video(result["data"])
        mime_type = "video/mp4"
    else:
        st.audio(result["data"], format="audio/mpeg")
        mime_type = "audio/mpeg"

    st.download_button(
        label=f"⬇ Download {result['filename']}",
        data=result["data"],
        file_name=result["filename"],
        mime=mime_type,
        type="primary",
        use_container_width=True,
        key="final_download_button",
    )

    st.caption(
        "The result remains available in the current session "
        "while session and server resources remain available. "
        "This is not permanent cloud storage."
    )

    if st.session_state.download_complete:
        components.html(
            """
            <script>
            (function () {
                function scrollToResult() {
                    try {
                        const parentDoc = window.parent.document;
                        const anchor =
                            parentDoc.getElementById("result-anchor");

                        if (anchor) {
                            anchor.scrollIntoView({
                                behavior: "smooth",
                                block: "start"
                            });
                        }
                    } catch (error) {
                        // Parent-page access may be restricted.
                    }
                }

                setTimeout(scrollToResult, 250);
                setTimeout(scrollToResult, 800);
            })();
            </script>
            """,
            height=0,
        )

elif st.session_state.download_error:
    st.warning(st.session_state.download_error)


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    f"""
    <div style="text-align:center;padding:12px;">
        <div style="
            font-weight:850;color:{C['text']};font-size:18px;">
            MediaFlow
        </div>
        <div class="notice">
            Download only content you own or are authorized to save.
        </div>
        <div class="notice" style="margin-top:6px;">
            Made for your media workflow ·
            {"Dark" if dark else "Light"} appearance
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
