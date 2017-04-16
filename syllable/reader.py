from scipy.io import wavfile
import numpy as np

def read(filename):
  """
  Take a wavefile and return its mono signal (average of both
  channels) in an array with time and value.
  
  Parameters
  ----------

  filename : str
      Wavefile name
  
  Returns
  -------

  song : numpy array
      An array of (nsamples, 2). First column is time, second one is
      value
  """
  w = wavfile.read(filename)
  fsample = float(w[0])
  audio = w[1]
  nsamples = audio.shape[0]
  song = np.zeros((nsamples, 2))
  song[:, 0] = np.arange(0, nsamples/fsample, 1/fsample)
  song[:, 1] = (audio[:, 0] + audio[:, 1])/2
  return song
