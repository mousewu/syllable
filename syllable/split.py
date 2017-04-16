import pylab as pl
import scipy
import reader as rd
import filters
import tools

s = rd.read('canary.wav')
minima, idx = filters.ceci(s, freq_fast=250, freq_slow=40,
                           freq_env=700, thr=0.2)
syl = tools.split(s, idx)
for i, s in enumerate(syl):
  print i
  fig, axarr = pl.subplots(2, 1, figsize=(5, 8))
  axarr[0].plot(s[:, 0], s[:, 1])
  axarr[1].specgram(s[:, 1], NFFT=int(0.005*44800),
                    window=scipy.signal.tukey(int(44800*0.005)),
                    Fs=44800, noverlap=int(44800*0.004), cmap='jet')
  pl.savefig("syl_{0}.png".format(i))
  #pl.close()
