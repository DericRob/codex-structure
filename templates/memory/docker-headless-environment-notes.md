# Docker and Headless Environment Issues

## Known pitfalls

- `sounddevice` can fail at import time when PortAudio is unavailable
- `pyautogui` can fail with `KeyError: DISPLAY` or `OSError` in headless environments
- `mss.mss()` can fail at runtime when no display server is available
- Debian Bookworm uses `libgl1`, not `libgl1-mesa-glx`
- Tests should use `tmp_path` instead of writing beside test files on read-only mounts
- `load_dotenv()` can pollute test collection if unit tests rely on clean env state
- MCP stdio transport is safer with synchronous `stdout.buffer.write()` + `flush()`

## Practical rule

Guard GUI and audio imports, guard runtime instantiation of display-dependent objects, and keep test temp data isolated from the source tree.
