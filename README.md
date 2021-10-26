# Webcam Theremin 🎵
Python hand detection sends an OSC message to a SuperCollider synth - use hand motions to adjust the synth as it plays!

Python script (using OpenCV and MediaPipe to detect hand and landmarks) sends x and y coordinates of the index finger tip in an Open Sound Control message to SuperCollider. The parallel SuperCollider script uses these as frequency and multiplier for a synthesiser defined within it. 

Current example is a relatively basic sine oscillator, should work for different synths and for variables other than freq/mul with minimal adjustments.
Also detects the hand sign 🤘 or 🤟 (treated as the same) and will randomise the frequency, multiplier and amplitude while said hand sign is displayed.

Scripts just need to be run at the same time.
