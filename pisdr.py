#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SDR
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time



from gnuradio import qtgui

class pisdr(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SDR", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SDR")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pisdr")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.variable_qtgui_range_0 = variable_qtgui_range_0 = 105.5
        self.squelch = squelch = -20
        self.samp_rate = samp_rate = 2.4e6
        self.variable_qtgui_range_1 = variable_qtgui_range_1 = squelch
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = variable_qtgui_range_0 / 1e6
        self.source_chooser = source_chooser = 0
        self.freq = freq = variable_qtgui_range_0
        self.bandwidth = bandwidth = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self._variable_qtgui_range_1_range = Range(-100, 0, 1, squelch, 200)
        self._variable_qtgui_range_1_win = RangeWidget(self._variable_qtgui_range_1_range, self.set_variable_qtgui_range_1, "Squelch", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_1_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._source_chooser_options = [0, 1, 2, 3, 4, 5]
        # Create the labels list
        self._source_chooser_labels = ['WBFM', 'NBFM', 'AM', 'AM-USB', 'CW', 'Test']
        # Create the combo box
        self._source_chooser_tool_bar = Qt.QToolBar(self)
        self._source_chooser_tool_bar.addWidget(Qt.QLabel("Source" + ": "))
        self._source_chooser_combo_box = Qt.QComboBox()
        self._source_chooser_tool_bar.addWidget(self._source_chooser_combo_box)
        for _label in self._source_chooser_labels: self._source_chooser_combo_box.addItem(_label)
        self._source_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._source_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._source_chooser_options.index(i)))
        self._source_chooser_callback(self.source_chooser)
        self._source_chooser_combo_box.currentIndexChanged.connect(
            lambda i: self.set_source_chooser(self._source_chooser_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._source_chooser_tool_bar)
        self._bandwidth_range = Range(1, 2.5e6, 10, samp_rate, 200)
        self._bandwidth_win = RangeWidget(self._bandwidth_range, self.set_bandwidth, "Bandwidth", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bandwidth_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_range_0_range = Range(10, 800, 0.01, 105.5, 200)
        self._variable_qtgui_range_0_win = RangeWidget(self._variable_qtgui_range_0_range, self.set_variable_qtgui_range_0, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_range_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if lambda x: f'{x:5f}':
            self._variable_qtgui_label_0_formatter = lambda x: f'{x:5f}'
        else:
            self._variable_qtgui_label_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Frequency (MHz): "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq * 1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(40, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.rational_resampler_xxx_1_0_1 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1_0_0_0_2 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=200,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1_0_0_0_0 = filter.rational_resampler_ccc(
                interpolation=70,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1_0_0_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=10,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1_0_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            512, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq * 1e6, #fc
            bandwidth, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0_1_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate/4,
                samp_rate/8,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate/4,
                samp_rate/8,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate/4,
                samp_rate/8,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate/4,
                samp_rate/8,
                window.WIN_HAMMING,
                6.76))
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,source_chooser,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,source_chooser)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0_0_1_0 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0_0_1 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0_0_1_0 = audio.sink(48000, '', True)
        self.audio_sink_0_0_1 = audio.sink(48000, '', True)
        self.audio_sink_0_0_0 = audio.sink(48000, '', True)
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate/5,
        	audio_decimation=10,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq * 1e6, 1, 0, 0)
        self.analog_pwr_squelch_xx_0_1 = analog.pwr_squelch_cc(variable_qtgui_range_1, 1, 0, True)
        self.analog_pwr_squelch_xx_0_0 = analog.pwr_squelch_cc(variable_qtgui_range_1, 1, 0, True)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(variable_qtgui_range_1, 1, 0, True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=480000,
        	tau=75e-6,
        	max_dev=5e3,
          )
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate/10,
        	audio_decim=1,
        	audio_pass=10000,
        	audio_stop=11000,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.rational_resampler_xxx_1_0_0_0_2, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0_0_1, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0_1, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.audio_sink_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_1, 0), (self.audio_sink_0_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_1_0, 0), (self.audio_sink_0_0_1_0, 0))
        self.connect((self.blocks_selector_0, 5), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0, 3), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.rational_resampler_xxx_1_0_0, 0))
        self.connect((self.blocks_selector_0, 2), (self.rational_resampler_xxx_1_0_0_0, 0))
        self.connect((self.blocks_selector_0, 4), (self.rational_resampler_xxx_1_0_1, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.rational_resampler_xxx_1_0_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_pwr_squelch_xx_0_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.analog_pwr_squelch_xx_0_1, 0))
        self.connect((self.low_pass_filter_0_1_1, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.rational_resampler_xxx_1_0_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.rational_resampler_xxx_1_0_0_0, 0), (self.low_pass_filter_0_1_1, 0))
        self.connect((self.rational_resampler_xxx_1_0_0_0_0, 0), (self.blocks_selector_0_0, 5))
        self.connect((self.rational_resampler_xxx_1_0_0_0_2, 0), (self.blocks_multiply_const_vxx_0_0_1_0, 0))
        self.connect((self.rational_resampler_xxx_1_0_1, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0_0, 3))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0_0, 2))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0_0, 4))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pisdr")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_range_0(self):
        return self.variable_qtgui_range_0

    def set_variable_qtgui_range_0(self, variable_qtgui_range_0):
        self.variable_qtgui_range_0 = variable_qtgui_range_0
        self.set_freq(self.variable_qtgui_range_0)
        self.set_variable_qtgui_label_0(self.variable_qtgui_range_0 / 1e6)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.set_variable_qtgui_range_1(self.squelch)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bandwidth(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/4, self.samp_rate/8, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/4, self.samp_rate/8, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/4, self.samp_rate/8, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1_1.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/4, self.samp_rate/8, window.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_variable_qtgui_range_1(self):
        return self.variable_qtgui_range_1

    def set_variable_qtgui_range_1(self, variable_qtgui_range_1):
        self.variable_qtgui_range_1 = variable_qtgui_range_1
        self.analog_pwr_squelch_xx_0.set_threshold(self.variable_qtgui_range_1)
        self.analog_pwr_squelch_xx_0_0.set_threshold(self.variable_qtgui_range_1)
        self.analog_pwr_squelch_xx_0_1.set_threshold(self.variable_qtgui_range_1)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_source_chooser(self):
        return self.source_chooser

    def set_source_chooser(self, source_chooser):
        self.source_chooser = source_chooser
        self._source_chooser_callback(self.source_chooser)
        self.blocks_selector_0.set_output_index(self.source_chooser)
        self.blocks_selector_0_0.set_input_index(self.source_chooser)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0.set_frequency(self.freq * 1e6)
        self.qtgui_sink_x_0.set_frequency_range(self.freq * 1e6, self.bandwidth)
        self.rtlsdr_source_0.set_center_freq(self.freq * 1e6, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.qtgui_sink_x_0.set_frequency_range(self.freq * 1e6, self.bandwidth)




def main(top_block_cls=pisdr, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
