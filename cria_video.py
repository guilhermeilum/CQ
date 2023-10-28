import imageio
import numpy as np

tempo = np.load(r"fps\tempo.npy")
frames = []
DT = tempo[-1]

for t in tempo[:-1]:
    frames.append(np.load(rf"fps\fps_{t}.npy"))

output_video_path = f"simulation.mp4"
imageio.mimsave(output_video_path, frames, fps=int(1 / DT))
