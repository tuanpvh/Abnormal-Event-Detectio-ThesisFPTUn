import os

import matplotlib.pyplot as plt
import numpy as np
import torch
from moviepy.editor import VideoFileClip

from load_model import anomaly_model
import matplotlib.pyplot as plt
plt.switch_backend('Agg')

def predict(video_name):
  video_path = "static/uploads"
  output = torch.Tensor(np.load("shanghaitech_swin_feature/{}.npy".format(video_name))).unsqueeze(0)
  print(output.shape)

  clip = VideoFileClip(os.path.join(video_path, "{}.mp4".format(video_name)))
  duration = clip.duration
  print(duration)
  with torch.no_grad():
    anomaly_model.eval()
    scores = anomaly_model(output)
    scores = scores.numpy()
    
    scs = []

    for s in scores:
      for c in s:
        scs.append(c)
    print(scores.shape)
    x_ax = np.arange(len(scs))
    x_ax = x_ax*((duration*1000)/len(scs))
    print(x_ax)
    plt.xlabel("Time (ms)")
    plt.ylabel("Anomaly Score")

    start_frame = 0
    end_frame = 0
    for i in range(len(scs)):
      if scs[i] > 0.5:
        start_frame = i
        break
    
    for sc in reversed(scs):
      if sc > 0.5:
        end_frame = scs.index(sc)
        break
    
    start_frame = start_frame*((duration*1000)/len(scs))
    end_frame = end_frame*((duration*1000)/len(scs))
    plt.axvspan(start_frame, end_frame, facecolor='pink', alpha=0.5)

    plt.plot(x_ax,scs)
    plt.savefig('{}/{}.png'.format(video_path, video_name))
    plt.close()

    
  
  return int(start_frame), int(end_frame)