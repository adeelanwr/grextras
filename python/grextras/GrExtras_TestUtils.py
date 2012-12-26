# Copyright (C) by Josh Blum. See LICENSE.txt for licensing information.

import gras
import time

class VectorSource(gras.Block):
    def __init__(self, out_sig, vec, autodone=True):
        gras.Block.__init__(self, name='VectorSource', out_sig=[out_sig])
        self._vec = vec
        self._autodone = autodone

    def work(self, ins, outs):
        num = min(len(outs[0]), len(self._vec))
        outs[0][:num] = self._vec[:num]
        self.produce(0, num)
        self._vec = self._vec[num:]
        if not self._vec:
            if self._autodone: self.mark_done()
            #TODO auto done is a hack so we dont mark done for some of the tests
            #so we sleep here when not marking done so we dont suck cpu
            #Is there a better way to avoid this for a source block?
            #Also having a more configurable done policy could help the issue.
            else: time.sleep(0.1)

class VectorSink(gras.Block):
    def __init__(self, in_sig):
        gras.Block.__init__(self, name='VectorSink', in_sig=[in_sig])
        self._vec = list()

    def data(self):
        return tuple(self._vec)

    def work(self, ins, outs):
        self._vec.extend(ins[0].copy())
        self.consume(0, len(ins[0]))

class Head(gras.Block):
    def __init__(self, sig, num_items):
        gras.Block.__init__(self, name='Head', in_sig=[sig], out_sig=[sig])
        self._num_items = num_items

    def work(self, ins, outs):
        n = min(len(ins[0]), len(outs[0]), self._num_items)
        outs[0][:n] = ins[0][:n]
        self.consume(0, n)
        self.produce(0, n)
        self._num_items -= n
        if not self._num_items:
            self.mark_done()

__all__ = ["VectorSource", "VectorSink", "Head"]
