---
name: ffmpeg-cheatsheet
description: 'Use when the user needs ffmpeg commands: converting video and audio formats, trimming and cutting, resizing and compressing, extracting audio, adding subtitles, making GIFs and thumbnails, merging files, and batch conversion.'
---

# FFmpeg Cheatsheet — commands you'll actually use

One page. 28 commands. Each entry tells you **what it does** and gives you a **copy-paste command that really works**.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

---

## 📦 Install & check

### Install FFmpeg
Get the `ffmpeg` binary on your system first — everything below needs it.
```bash
brew install ffmpeg          # macOS
sudo apt install ffmpeg     # Debian/Ubuntu
winget install ffmpeg       # Windows (winget)
```
🏷️ `#install` `#setup`

### Check version and available encoders
Confirm the install worked and see which codecs your build supports.
```bash
ffmpeg -version                  # show version
ffmpeg -encoders | grep libx264  # is H.264 encoding available?
ffmpeg -encoders | grep libvpx   # is VP9 encoding available?
```
🏷️ `#install` `#debug`

---

## 🔄 Basic transcoding

### Anything → MP4 (H.264 + AAC)
The universal recipe: plays everywhere — browsers, phones, editors.
```bash
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```
🏷️ `#transcode` `#mp4` `#h264`

### MP4 → WebM (VP9 + Opus)
Smaller files for the web, great for `<video>` tags and HTML5 players.
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 2M -c:a libopus output.webm
```
🏷️ `#transcode` `#webm` `#web`

### MKV → MP4 without re-encoding (remux)
Just change the container — finishes in seconds, zero quality loss.
```bash
ffmpeg -i input.mkv -c copy output.mp4
# -c copy = copy streams as-is, no re-encoding
```
🏷️ `#transcode` `#remux` `#fast`

---

## 🗜️ Compression & quality

### Compress a video (CRF — the easy way)
One number controls quality: CRF 18–28, lower = better quality and bigger file. 23 is the default sweet spot.
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
# try -crf 28 for much smaller files, -crf 18 when quality matters most
```
🏷️ `#compress` `#quality` `#h264`

### Trade speed for size with presets
Same quality, smaller file — if you can wait. Or go fast when you're in a hurry.
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow output.mp4
# presets: ultrafast superfast veryfast faster fast medium slow slower veryslow
```
🏷️ `#compress` `#preset` `#h264`

### Two-pass encoding for a target file size
When the file must be exactly X MB (e.g. upload limits), two-pass hits the bitrate precisely.
```bash
ffmpeg -y -i input.mp4 -c:v libx264 -b:v 1M -pass 1 -an -f null /dev/null && \
ffmpeg -i input.mp4 -c:v libx264 -b:v 1M -pass 2 -c:a aac -b:a 128k output.mp4
# -an = no audio on pass 1; /dev/null discards the first-pass output
```
🏷️ `#compress` `#bitrate` `#advanced`

---

## 🎵 Extract audio

### Extract audio → MP3
Pull the soundtrack out of any video file.
```bash
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
# -vn = no video; -q:a 2 = high VBR quality (0 best … 9 worst)
```
🏷️ `#audio` `#extract` `#mp3`

### Extract audio → M4A (AAC)
Better quality per megabyte than MP3; plays natively on Apple devices.
```bash
ffmpeg -i input.mp4 -vn -c:a aac -b:a 192k audio.m4a
```
🏷️ `#audio` `#extract` `#aac`

### Extract audio without re-encoding
Fastest option — but only works if the codec already fits the container.
```bash
ffmpeg -i input.mp4 -vn -c:a copy audio.aac
```
🏷️ `#audio` `#extract` `#fast`

---

## 🖼️ Video → GIF

### Step 1: generate an optimized palette
A custom palette is what makes GIFs look good instead of banded and ugly.
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,palettegen" palette.png
```
🏷️ `#gif` `#palette`

### Step 2: render the GIF with that palette
Use the palette from step 1 for clean colors and small file size.
```bash
ffmpeg -i input.mp4 -i palette.png -filter_complex "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
# fps=10 keeps the GIF small; raise it (e.g. 15) for smoother motion
```
🏷️ `#gif` `#convert`

---

## ✂️ Cut & join

### Fast cut (seek before `-i`)
Cuts a 30-second clip starting at 1:30. Fast because it seeks before decoding.
```bash
ffmpeg -ss 00:01:30 -i input.mp4 -t 00:00:30 -c copy clip.mp4
# -ss before -i = fast seek; -t = duration of the clip
```
🏷️ `#cut` `#clip` `#fast`

### Frame-accurate cut (re-encode)
Put `-ss` after `-i` when the cut point must land on the exact frame.
```bash
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:00:30 -c:v libx264 -c:a aac clip.mp4
# slower (decodes from the start) but frame-accurate
```
🏷️ `#cut` `#clip` `#accurate`

### Join videos losslessly (concat)
Stitch clips together with no re-encoding — all inputs must share codec and parameters.
```bash
# list.txt contains one line per file:
#   file 'a.mp4'
#   file 'b.mp4'
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4
```
🏷️ `#join` `#concat` `#fast`

---

## 📐 Scale & crop

### Scale to 720p
Resize to exactly 1280×720.
```bash
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4
```
🏷️ `#scale` `#resize`

### Scale by width, keep aspect ratio
Set the width; `-2` auto-computes the height and rounds to an even number (H.264 requires even dimensions).
```bash
ffmpeg -i input.mp4 -vf "scale=640:-2" output.mp4
```
🏷️ `#scale` `#resize`

### Crop a region
Cut a 640×480 box starting at position (100, 50). Format: `crop=W:H:X:Y`.
```bash
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4
```
🏷️ `#crop` `#edit`

---

## 💧 Watermark & subtitles

### Overlay a watermark (top-right)
Burn a PNG logo into the corner of the video.
```bash
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=W-w-10:10" -c:a copy output.mp4
# W-w-10:10 = 10px margin from the top-right corner
```
🏷️ `#watermark` `#overlay` `#branding`

### Burn subtitles into the video
Hardcode an `.srt` file so the text shows on every player.
```bash
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" -c:a copy output.mp4
# needs a build with libass; quote the path if it contains spaces or special chars
```
🏷️ `#subtitles` `#burn-in`

### Simple text overlay
Add plain text without any extra files.
```bash
ffmpeg -i input.mp4 -vf "drawtext=text='Hello':fontsize=48:fontcolor=white:x=10:y=10" -c:a copy output.mp4
```
🏷️ `#text` `#overlay`

---

## 🎞️ Frames & info

### Extract a poster frame
Grab one still image at the 5-second mark — perfect for video thumbnails.
```bash
ffmpeg -ss 00:00:05 -i input.mp4 -vframes 1 poster.jpg
# -ss before -i = fast seek to that timestamp
```
🏷️ `#thumbnail` `#frame`

### Dump video frames as images
Export one JPEG per second — handy for analysis or building datasets.
```bash
ffmpeg -i input.mp4 -vf fps=1 frame_%03d.jpg
# produces frame_001.jpg, frame_002.jpg … ; use fps=1/60 for one frame per minute
```
🏷️ `#frames` `#extract`

### Replace a video's audio track
Swap in new audio without re-encoding the video stream.
```bash
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4
# -map picks streams explicitly; -shortest ends output at the shorter input
```
🏷️ `#audio` `#mux`

---

## 📡 Live streaming

### Push to an RTMP server
Stream a file (or loop it) to YouTube Live, Twitch, or any RTMP endpoint.
```bash
ffmpeg -re -i input.mp4 -c:v libx264 -preset veryfast -b:v 2500k -c:a aac -b:a 128k -f flv rtmp://live.example.com/app/STREAM_KEY
# -re reads input at native frame rate; replace the URL and key with yours
```
🏷️ `#streaming` `#rtmp` `#live`

---

## 🔁 Batch processing

### Batch-convert every MP4 to WebM
Loop over a folder — one command handles the whole batch.
```bash
for f in *.mp4; do ffmpeg -i "$f" -c:v libvpx-vp9 -b:v 2M -c:a libopus "${f%.mp4}.webm"; done
```
🏷️ `#batch` `#loop` `#webm`

### Batch-extract audio from every video
Same loop pattern, different job: MP3s for the whole folder.
```bash
for f in *.mp4; do ffmpeg -i "$f" -vn -c:a libmp3lame -q:a 2 "${f%.mp4}.mp3"; done
```
🏷️ `#batch` `#loop` `#audio`

---

## 📚 Learn more

- Official documentation: https://ffmpeg.org/documentation.html
- `ffmpeg -h` and `ffmpeg -h full` — every option, right in your terminal

## Contributing

Found a wrong command, a better recipe, or a bad translation? Pull requests are welcome — please keep entries to the format above (what it does / command / tags) and **verify every command runs before submitting**.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
