import streamlit as st
import os

from pathlib import Path
from datetime import date, datetime, timedelta
import streamlit.components.v1 as components
import random


#st.write("CWD:", os.getcwd())
MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)
images_dir = Path("media/images")
videos_dir = Path("media/videos")
images_dir.mkdir(parents=True, exist_ok=True)
videos_dir.mkdir(parents=True, exist_ok=True)


if "page" not in st.session_state:
    st.session_state.page = "home"

with st.sidebar:
    st.header("Controls")

    uploaded_files = st.file_uploader(
    "Upload Sage Media",
    type=["jpg","png","jpeg", "jpg", "heif", "heic","mp4","mov","avi"],  # restrict file types
    accept_multiple_files=True
)
    
    if st.button("View Full Gallery"):
        st.session_state.page = "gallery"
    if st.button("Home"):
        st.session_state.page = "home"
    

for uploaded_file in uploaded_files:
    if uploaded_file.type.startswith("image/"):
        save_path = images_dir / uploaded_file.name
    elif uploaded_file.type.startswith("video/"):
        save_path = videos_dir / uploaded_file.name
    else:
        st.warning(f"Unsupported file type: {uploaded_file.name}")
        continue

    if save_path.exists():
        st.warning(f"{uploaded_file.name} already exists, skipping.")
        continue

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Saved {uploaded_file.name}!")
    
        
st.set_page_config(layout="wide")


images = list(Path("media/images").glob("*"))
videos = list(Path("media/videos").glob("*"))

if st.session_state.page == "home":

    st.markdown(
    "<h1 style='text-align: center; font-size: 60px;'>🐈‍⬛ Daily Sage</h1>",
    unsafe_allow_html=True
)



    from datetime import datetime
    import pytz
    import streamlit as st

    if "timezone" not in st.session_state:
        st.session_state.timezone = "America/New_York"
        
    tz = st.selectbox(
        "Time zone",
        options=pytz.common_timezones,
        index=pytz.common_timezones.index(st.session_state.timezone),
        key="tz_select"
    )

    if tz != st.session_state.timezone:
        st.session_state.timezone = tz
        st.rerun()
        
    tz = pytz.timezone(st.session_state.timezone)
    user_now = datetime.now(tz)

    today_str = user_now.strftime("%B %d, %Y")



    #today_str = date.today().strftime("%B %d, %Y")

    st.markdown(
        f"<p style='text-align: center; font-size: 24px;'>{today_str}</p>",
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <style>
        .stColumn {
            background-color: #9caf88;
            padding: 10px;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    today = date.today()
    day_number = (today - date(1970,1,1)).days

    # Get the “daily” photo/video using modulo
    img_path = images[day_number % len(images)] if images else None
    vid_path = videos[day_number % len(videos)] if videos else None

    photo_col, video_col= st.columns([5, 5])

    with photo_col:
            st.markdown(
            "<h1 style='text-align: center; font-size: 30px; color: black;'>Your Daily Photo</h1>",
            unsafe_allow_html=True
        )
            if img_path:
                st.image(img_path, use_container_width=True)
            else:
                st.info("No image available")


    with video_col:
            st.markdown(
            "<h1 style='text-align: center; font-size: 30px; color: black;'>Your Daily Video</h1>",
            unsafe_allow_html=True
        )
            
            if vid_path:
                st.video(vid_path)
            else:
                st.info("No video available")


    #Sage Sounds

    st.markdown(
        "<h1 style='text-align: center; font-size: 40px;'>🎵Sage Sounds</h1>",
        unsafe_allow_html=True
    )

    audio_dir = Path("media/audio")
    audio_files = list(audio_dir.glob("*"))

    if st.button(
        f"Click to hear Sage",
        key="sage_sound_btn",
        help="Click to play a random sage sound",
        use_container_width=True,
    ):
        if audio_files:
            chosen_audio = random.choice(audio_files)
            st.audio(str(chosen_audio), autoplay=True)
        else:
            st.info("No audio files found")
    
elif st.session_state.page == "gallery":
    def display_media_grid(media_list, items_per_row=4, media_type="image"):
        for i in range(0, len(media_list), items_per_row):
            row_items = media_list[i:i+items_per_row]
            cols = st.columns(len(row_items))  # create a column for each item in this row
            for col, item in zip(cols, row_items):
                with col:
                    if media_type == "image":
                        st.image(item, use_container_width=True)
                    elif media_type == "video":
                        st.video(item)
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{media_type}_{item.name}",
                        use_container_width=True,
                    ):
                        item.unlink(missing_ok=True)
                        st.success(f"Deleted {item.name}")
                        st.rerun()
                        
    st.title("📸 Full Gallery")
    
    tabs = st.tabs(["Photos", "Videos"])

    with tabs[0]:
        if images:
            display_media_grid(images, items_per_row=4, media_type="image")
        else:
            st.info("No images available")

    with tabs[1]:
        if videos:
            display_media_grid(videos, items_per_row=4, media_type="video")
        else:
            st.info("No videos available")