"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, real_freq=105.4, test_freq=1, source=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Source or Test block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.real_freq = real_freq
        self.test_freq = test_freq
        self.source = source
        self.portName = 'freq'
        self.message_port_register_out(pmt.intern(self.portName))

    def work(self, input_items, output_items):
        if (self.source < 5):
            #PMT_msg = pmt.to_float(self.real_freq)
            PMT_msg = pmt.cons(pmt.intern('freq'), pmt.from_float(self.real_freq))
            output_items[0][:] = self.real_freq
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
        else:
            #PMT_msg = pmt.to_float(self.test_freq)
            PMT_msg = pmt.cons(pmt.intern('freq'), pmt.from_float(self.test_freq))
            output_items[0][:] = self.test_freq
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
        #PMT_msg = pmt.from_float(self.test_freq)
        #self.message_port_pub(pmt.intern('freq'), pmt.cons(pmt.intern('freq'), pmt.from_double(self.test_freq)))
        #gr.log.error("Unable to print: %s" % repr(e)) 
        output_items[0][:] = input_items[0]
        #self.message_port_pub(pmt.intern(self.portName), PMT_msg)
        return len(output_items[0])
