PVM v5.3 ComfyUI skin - typeface
=================================
ComfyUI's interface font is Inter. Put these two files here:

  fonts/Inter-Regular.ttf
  fonts/Inter-Medium.ttf

Download (free, SIL Open Font License): https://rsms.me/inter/
 -> unzip -> "Inter Desktop" or "extras/ttf" -> copy the two files above.

If the files are missing PVM falls back to a system "Inter"/Segoe UI/Arial,
and finally to pygame's default font, so nothing breaks - it just won't
match ComfyUI's typography until the files are in place.

Tuning: INTER_SIZE_SCALE (top of __init__.py, default 0.9) adjusts Inter's
rendered size relative to v5.2's metrics if buttons feel too wide/narrow.
