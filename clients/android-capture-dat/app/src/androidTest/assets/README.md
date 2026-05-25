# Instrumentation test assets

| File             | Purpose                                                     |
| ---------------- | ----------------------------------------------------------- |
| `test_video.mp4` | Mock streaming feed — **H.265/HEVC** recommended on Android |
| `test_image.png` | Mock still capture                                          |

Tests skip gracefully if files are missing (`Assume.assumeTrue`).

## H.265 transcode (Meta recommendation)

```bash
ffmpeg -i input.mp4 -c:v libx265 -tag:v hvc1 -vf "scale=540:960" test_video.mp4
cp test_video.mp4 app/src/androidTest/assets/
```

## Minimal PNG

Any small PNG works for `test_image.png` (e.g. 64×64).
