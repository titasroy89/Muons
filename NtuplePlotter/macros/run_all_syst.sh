#!/bin/bash
python makePlots.py Btag_up 
python makePlots.py Btag_down
python makePlots.py EleEff_up
python makePlots.py EleEff_down
python makePlots.py EleFakeSF_up
python makePlots.py EleFakeSF_down
python makePlots.py JEC_up
python makePlots.py JEC_down
python makePlots.py JER_up
python makePlots.py JER_down
python makePlots.py PU_up
python makePlots.py PU_down
python makePlots.py QCD_up
python makePlots.py QCD_down
python makePlots.py ZJetsSF_up
python makePlots.py ZJetsSF_down
python makePlots.py elesmear_up
python makePlots.py elesmear_down
python makePlots.py pho_up
python makePlots.py pho_down
python makePlots.py toppt_up
python makePlots.py toppt_down
python makePlots.py > ratio_nominal.txt

