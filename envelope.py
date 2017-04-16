"""
Envelope example:
Step by step implementation of the ceci filter
"""

from syllable import reader
import pylab as pl
import numpy as np

from scipy import signal
from syllable import filters

s = reader.read('test_data/canary.wav')
env = filters.envelope(s)
butter_fast = filters.butter(env, 250)
butter_slow = filters.butter(env, 40)

peakind_min_p = filters.relative_min(butter_slow)
candidates_env = butter_fast[peakind_min_p, :]
minima, idx = filters.threshold_min(candidates_env, 0.2*max(env[:, 1]))

plot_step = 100
pl.figure(figsize=(13, 9.5))
pl.grid(True)
pl.plot(s[::plot_step, 0], s[::plot_step, 1],
        color='c', label='Time Signal')

pl.plot(butter_fast[::plot_step, 0], butter_fast[::plot_step, 1],
        color='r', label='Peak approach Signal envelope', linewidth=2)

pl.xlabel('Time (s)')
pl.ylabel('Amplitude')
markerline3, _, __ = pl.stem(minima[:, 0], minima[:, 1], 'm')
pl.setp(markerline3, 'markerfacecolor', 'm', label='Envelope min')
pl.legend(fontsize='x-small')
pl.savefig('envelope_example.png')
