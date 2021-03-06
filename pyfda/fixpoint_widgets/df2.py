# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Widget for specifying the parameters of a direct-form 2 (DF2) filter
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys
import logging
logger = logging.getLogger(__name__)

import numpy as np

import pyfda.filterbroker as fb
import pprint

from ..compat import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from .fixpoint_helpers import UI_W, UI_W_coeffs, UI_Q, UI_Q_coeffs
from .filter_iir import FilterIIR 
#==============================================================================

class DF2(QWidget):
    """
    Widget for entering word formats & quantization
    """
    def __init__(self, parent):
        super(DF2, self).__init__(parent)

        self.title = ("<b>Direct-Form 2 (DF2) Filters</b><br />"
                 "Simple topology, only suitable for low-order filters.")
        self.img_name = "df2.png"

        self._construct_UI()

    def _construct_UI(self):
        """
        Intitialize the UI
        """
#------------------------------------------------------------------------------

        lblHBtnsMsg = QLabel("<b>Fixpoint signal / coeff. formats as WI.WF:</b>", self)
        self.layHBtnsMsg = QHBoxLayout()
        self.layHBtnsMsg.addWidget(lblHBtnsMsg)

        self.wdg_w_input = UI_W(self, label='Input Format <i>Q<sub>X </sub></i>:')
        self.wdg_w_coeffs = UI_W_coeffs(self, label='Coefficient Format:', enabled=False,
                                        tip_WI='Number of integer bits - edit in the "b,a" tab',
                                        tip_WF='Number of fractional bits - edit in the "b,a" tab',
                                        WI = fb.fil[0]["q_coeff"]['WI'],
                                        WF = fb.fil[0]["q_coeff"]['WF'])
        self.wdg_q_coeffs = UI_Q_coeffs(self, enabled=False,
                                        cur_ov=fb.fil[0]["q_coeff"]['ovfl'], 
                                        cur_q=fb.fil[0]['q_coeff']['quant'])
        #self.wdg_w_accu = UI_W(self, label='Accumulator Format:', WF=30)
        #self.wdg_q_accu = UI_Q_Ovfl(self)
        self.wdg_w_output = UI_W(self, label='Output Format <i>Q<sub>Y </sub></i>:')
        self.wdg_q_output = UI_Q(self)
#------------------------------------------------------------------------------

        layVWdg = QVBoxLayout()
        layVWdg.setContentsMargins(0,0,0,0)

        layVWdg.addLayout(self.layHBtnsMsg)

        layVWdg.addWidget(self.wdg_w_input)
        layVWdg.addWidget(self.wdg_w_coeffs)
        layVWdg.addWidget(self.wdg_q_coeffs)

        #layVWdg.addWidget(self.wdg_w_accu)
        #layVWdg.addWidget(self.wdg_q_accu)

        layVWdg.addWidget(self.wdg_w_output)
        layVWdg.addWidget(self.wdg_q_output)

        layVWdg.addStretch()

        self.setLayout(layVWdg)
        
#------------------------------------------------------------------------------
    def update_UI(self):
        """
        Update all parts of the UI that need to be updated when specs have been
        changed outside this class (e.g. coefficient wordlength).
        This is called from one level above.
        """
        self.wdg_w_coeffs.load_ui()
        self.wdg_q_coeffs.load_ui()

#==============================================================================
    def build_hdl_dict(self):
        """
        Build the dictionary for passing infos to the filter implementation
        """
        hdl_dict = {'QC':self.wdg_w_coeffs.c_dict} # coefficients
        # parameters for input format
        hdl_dict.update({'QI':{'WI':self.wdg_w_input.WI,
                               'WF':self.wdg_w_input.WF
                               }
                        })
        # parameters for output format
        hdl_dict.update({'QO':{'WI':self.wdg_w_output.WI,
                               'WF':self.wdg_w_output.WF,
                               'OVFL': self.wdg_q_output.ovfl,
                               'QUANT': self.wdg_q_output.quant
                               }
                        })
  
        hdl_dict_sorted = [str(k) +' : '+ str(hdl_dict[k]) for k in sorted(hdl_dict.keys())]
        hdl_dict_str = pprint.pformat(hdl_dict_sorted)
        logger.info("exporting hdl_dict:\n{0:s}".format(hdl_dict_str))   

        return hdl_dict

#==============================================================================
    def setup_HDL(self, coeffs):
        """
        Instantiate the myHDL description and pass quantization parameters and
        coefficients.
        """
        # a dict like this could be passed to myHDL
        self.build_hdl_dict()

        self.W = (self.wdg_w_input.WI + self.wdg_w_input.WF, self.wdg_w_input.WF) # Matlab format: (W,WF)
        
        logger.info("W = {0}".format(self.W))
        logger.info('b = {0}'.format(coeffs[0][0:3]))
        logger.info('a = {0}'.format(coeffs[1][0:3]))

        
        self.flt = FilterIIR(b=np.array(coeffs[0][0:3]),
                a=np.array(coeffs[1][0:3]),
                #sos = sos, doesn't work yet
                word_format=(self.W[0], 0, self.W[1]))

#------------------------------------------------------------------------------

if __name__ == '__main__':

    from ..compat import QApplication
    app = QApplication(sys.argv)
    mainw = DF2(None)
    mainw.show()

    app.exec_()
    
    # test using "python -m pyfda.fixpoint_filters.df2"