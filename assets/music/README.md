# HD-era soundtrack (playlist)

The final ("Today") era streams music from the tracks listed in **`assets/music/playlist.json`**:

```json
{ "tracks": [ { "file": "my-track.mp3", "title": "My Track" } ] }
```

- Tracks play in random order, never the same track twice in a row (when there's more than one).
- Only one track is downloaded up front (when the SVGA era starts, a lap early). Once the current track is
  half played, the next random track is loaded into a second player so it starts instantly when the current one ends.
- A "♪ NOW PLAYING" message shows when each track starts.
- To add a track: drop the MP3 in this folder and add an entry to `playlist.json`.
- Use music you have the rights to distribute, and add a credit to `assets/CREDITS.md` if needed.
- If no track can be loaded, the HD era falls back to the game's synthesised score.
