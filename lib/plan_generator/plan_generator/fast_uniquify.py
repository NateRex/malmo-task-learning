def fast_uniquify(seq, idfun=None):
    """
    # https://www.peterbe.com/plog/uniqifiers-benchmark
    # May 9 2018, 1:21
    """
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result
