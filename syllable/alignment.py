"""Alignment routines"""

from scipy import signal
from filters import envelope
import pandas as pd
import numpy as np

def maxrel(signals, rel_height=0.8):
  """
  Simple alignment routine that tries to align signal matching times
  with equal height relative to the maximum.
  
  Parameters
  ----------

  signals: pandas DataFrame
      DataFrame with signals 

  rel_height : float
      Relative height to anchor time series. Default value is 0.8

  Returns
  -------

  aligned_signals: pandas DataFrame
      DataFrame with aligned signals
  """
  all_es = []
  for i in signals:
    es = signals[i].dropna()
    anchor = es[es >= es.max()*rel_height]
    # First time that is greater than rel*max
    anchor = anchor.index[0]
    es.index -= anchor
    all_es.append(es)
  aligned_signals = pd.concat(all_es, axis=1)
  aligned_signals.index -= aligned_signals.index[0]
  return aligned_signals

def dispersion(signals):
  """
  Checks how dispersed is each signal from the average, reporting the 
  result in only one float number, so to minimize the error and assess
  how well was the alignment.
  
  Parameters
  ----------

  signals: pandas DataFrame
      DataFrame with signals 

  Returns
  -------

  error: float
      Total error/dispersion
  """
  diff = signals.copy()
  for i in signals:         
    diff[i] = signals[i] - signals.mean(axis=1)
  return diff.std().sum()
