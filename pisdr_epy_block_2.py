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
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, real_freq = 1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Frequency Control',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.inPortName = "in"
        self.freq = real_freq
        self.message_port_register_in(pmt.intern(self.inPortName))
        self.message_port_register_out(pmt.intern("freq"))
        self.set_msg_handler(pmt.intern(self.inPortName), self.handle_msg)
        
    def handle_msg(self, msg):
    	value = pmt.to_python(msg)[1]
    	self.freq += value
    	print (self.freq)
    	freq_msg = pmt.cons(pmt.intern('freq'), pmt.from_double(self.freq))
    	self.message_port_pub(pmt.intern("freq"),freq_msg)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0][:]
        return len(output_items[0])
