from scipy import signal
import numpy as np

def butter(sig, freq, order=4):
  """
  Calculate butterworth filter

  Parameters
  ----------

  freq : float
      Frequency of the filter

  sig : numpy array
      An array of (nsamples, 2). First column is time, second one is
      envelope

  order : optional
      Order of the filter. Default value is 4

  Returns
  -------

  filt : numpy array
      The filtered signal
  """
  filt = sig.copy()
  dt = sig[1, 0] - sig[0, 0]
  b, a = signal.butter(order, freq*dt, btype='lowpass')
  _filt = signal.filtfilt(b, a, sig[:, 1])
  filt[:, 1] = _filt
  return filt

def envelope(sig, freq=700.0):
  """
  Calculates a crude envelope finding the maximum in a window of
  frequency set by the object.

  Parameters
  ----------

  signal : numpy array
      An array of (nsamples, 2). First column is time, second one is
      value

  Returns
  -------

  envelope : numpy array
      An array of (nsamples, 2). First column is time, second one is
      envelope
  """
  window_size = int(1/(freq * (sig[1, 0] - sig[0, 0])))
  env = sig.copy()
  nsamples = sig.shape[0]
  for i, point in enumerate(sig):
    if i < (window_size + 1)/2 or i > (nsamples - (window_size + 1)/2):
      env[i, 1] = point[1]
      continue
    env[i, 1] = max(sig[i-window_size/2:i+window_size/2, 1])
  return env

def relative_min(sig):
  """
  Calculates the relative minima.

  Parameters
  ----------

  signal : numpy array
      An array of (nsamples). First column is time, second one is
      envelope.

  Returns
  -------

  minima : numpy array
      An array with the positions of minima.
  """
  minima = signal.argrelmin(sig[:, 1], axis=0)
  return minima[0]

def threshold_min(sig, thr):
  """
  Calculates the points lower than a given threshold.

  Parameters
  ----------

  sig : numpy array
      An array of (nsamples, 2). First column is time, second one is
      envelope.

  threshold : float
      Threshold value

  Returns
  -------

  signal : numpy array
      An array of (nsamples, 2). First column is time, second one is
      envelope.
  """
  filt = sig.copy()
  mask = sig[:, 1] < thr
  filt = filt[mask, :]
  return filt, np.arange(sig.shape[0])[mask]

def ceci(sig, env, freq_fast=250.0, freq_slow=40.0, thr=0.08):
  """
  Implement the ceci filter (je)

  Parameters
  ----------

  sig : numpy array
      An array of (nsamples, 2). First column is time, second one is
      envelope.

  env : numpy array
      The envelope of the signal

  freq_fast : float
      Frequency of the fast butter filter

  freq_slow : float
      Frequency of the slow butter filter

  freq_env : float
      Frequency of the envelope

  thr : float
      Relative value of the threshold

  Returns
  -------

  signal, idx : numpy array, numpy array
      sig is An array of (nsamples, 2). First column is time, second one is
      envelope.
      idx is the array of the positions
  """
  butter_fast = butter(env, freq_fast)
  butter_slow = butter(env, freq_slow)
  peakind_min_p = relative_min(butter_slow)
  candidates_env = butter_fast[peakind_min_p, :]
  minima, idx = threshold_min(candidates_env, thr*max(env[:, 1]))
  idx = peakind_min_p[idx]
  return minima, idx
