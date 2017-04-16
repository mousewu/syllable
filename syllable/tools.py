def split(sig, idx):
  """
  Split a sound signal for the given indices.

  Parameters
  ----------

  sig : numpy array
      An array of (nsamples, 2). First column is time, second one is
      envelope

  idx : numpy array
      Indices

  Returns
  -------

  syllables : list
      A list with the signal of each syllable
  """
  syl = []
  for j, i in enumerate(idx):
    if i == idx[0]:
      this_syl = sig[:i]
    elif i == idx[-1]:
      this_syl = sig[i:]
    else:
      this_syl = sig[i:idx[j+1]]
    this_syl[:, 0] -= this_syl[0, 0]
    syl.append(this_syl)
  return syl
