# TODO: Song template

from dataclasses import dataclass
from datetime import date
import re

SONG_REGEX = re.compile(r"(\d\d\d\d-\d\d-\d\d) - (.+) - (.+)\.mp3")


@dataclass
class Song:
  date: str
  artist: str
  title: str
  filename: str
  base_dir: str

def get_songs(ctx):
  songs = []

  for name in ctx.names:
    if name.startswith("songs/"):
      candidate = name[len("songs/"):]
      date_str, artist, title = SONG_REGEX.match(candidate).groups()
      base_dir = f"{date_str}/{artist}/{title}"
      songs.append(Song(date.fromisoformat(date_str), artist, title, name, base_dir))

  songs.sort(key=lambda s: s.date)
  return songs


def get_global_styles(ctx):
  minification = ctx.ext("minification")
  with open("./global.css") as f:
    return minification.minify_css(f.read())


def build(ctx):
  templating = ctx.ext("templating")

  templating.set_base_directory("./build_src/templates/")
  song_template = templating.from_file("./build_src/templates/song.html.j2")

  global_context = {
    "global_styles": get_global_styles(ctx)
  }

  songs = get_songs(ctx)
  for song in songs:
    song_audio_data = ctx.read_data(song.filename)
    ctx.write_data(song.base_dir + "/audio.mp3", song_audio_data)

    song_page = song_template.render(song=song, **global_context)
    ctx.write_text(song.base_dir + "/index.html", song_page)

  ctx.write_text(
    "index.html",
    templating.from_string(ctx.read_text("index.html.j2"))
      .render(songs=songs, **global_context)
  )
