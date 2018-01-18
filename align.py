"""
Alignment example, with relative maximum.
"""

import pylab as pl
import pandas as pd
import numpy as np
from syllable import reader
from syllable import filters
from syllable import tools
from syllable import alignment

s = reader.read('test_data/canary.wav')
e = filters.envelope(s, 700)
minima, idx = filters.ceci(s, e, freq_fast=250, freq_slow=40, thr=0.2)
syl = tools.split(s, idx)
envel = tools.split(e, idx)

# Needed so far to convert np arrays to pandas.
for i, e in enumerate(envel):
  idx = e[:, 0]
  envel[i] = pd.Series(e[:, 1])
  envel[i].index = idx

#Get only first 20 syl
all_es = pd.concat(envel[:20], axis=1)


#Sweep in relative heights
relat = np.concatenate([np.linspace(0, 0.6, 6), np.linspace(0.6, 1.0, 41)])
dif = np.zeros_like(relat)

for i, r in enumerate(relat):
  aligned = alignment.maxrel(all_es, r)
  dif[i] = alignment.dispersion(aligned)


# Plot the sweep in relative heights
fig, ax = pl.subplots()
ax.plot(relat, dif, '.-')
ax.set_xlabel('Relative Height')
ax.set_ylabel('Error of the alignment')
ax.set_title('Effect of relative height')
fig.savefig('align_plots/sweep.png')
# Plot all signals for the optimum relative height
r = relat[np.argmin(dif)]
aligned = alignment.maxrel(all_es, r)

fig, ax = pl.subplots()
for c in all_es:
  aligned[c].dropna().plot(ax=ax, lw=0.2)
aligned.mean(axis=1).rolling(50).mean().plot(ax=ax)
ax.set_title('Syllable average')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude')
fig.savefig('align_plots/average.png')
