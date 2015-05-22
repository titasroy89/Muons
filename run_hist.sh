#!/bin/csh

set hist="hist_PU_up"
set dir="/eos/uscms/store/user/troy2012/TTGamma/skim_19_5/"

NtuplePlotter/makeTemplates Data_a $hist ${dir}skim_data_mu_a.root
NtuplePlotter/makeTemplates Data_b $hist ${dir}skim_data_mu_b.root
NtuplePlotter/makeTemplates Data_c $hist ${dir}skim_data_mu_c.root
NtuplePlotter/makeTemplates Data_d $hist ${dir}skim_data_mu_d.root
NtuplePlotter/makeTemplates W4Jets $hist ${dir}skim_W4jets.root
NtuplePlotter/makeTemplates W3Jets $hist ${dir}skim_W3jets.root
NtuplePlotter/makeTemplates TTJets2l $hist ${dir}skim_ttjets_2l.root
NtuplePlotter/makeTemplates TTJets1l $hist ${dir}skim_ttjets_1l.root
NtuplePlotter/makeTemplates TTJetsHad $hist ${dir}skim_ttjets_0l.root
NtuplePlotter/makeTemplates TTGamma $hist ${dir}skim_ttg.root
NtuplePlotter/makeTemplates ZJets $hist ${dir}skim_DYJetsToLL.root
NtuplePlotter/makeTemplates Zgamma $hist ${dir}skim_Zg.root
NtuplePlotter/makeTemplates Wgamma $hist ${dir}skim_Wg.root
NtuplePlotter/makeTemplates SingleT_t $hist ${dir}skim_t_t.root
NtuplePlotter/makeTemplates SingleT_s $hist ${dir}skim_t_s.root
NtuplePlotter/makeTemplates SingleT_tw $hist ${dir}skim_t_tW.root
NtuplePlotter/makeTemplates SingleTbar_t $hist ${dir}skim_tbar_t.root
NtuplePlotter/makeTemplates SingleTbar_s $hist ${dir}skim_tbar_s.root
NtuplePlotter/makeTemplates SingleTbar_tw $hist ${dir}skim_tbar_tW.root
