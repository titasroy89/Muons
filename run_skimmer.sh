#!/bin/bash

job=$1
#job=5

cd /uscms_data/d3/troy2012/CMSSW_5_3_14_patch2/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
cd /uscms_data/d3/troy2012/ANALYSIS_2/ 

outputDir="/eos/uscms/store/user/troy2012/TTGamma/skim_19_5/"
inputfiles=("skim_ttjets_0l.root /eos/uscms/store/user/troy2012/GG_MC_12/TTJets_Hadronic/TTJets_hadronic.root" \
"skim_W3jets.root /uscmst1b_scratch/lpc1/old_scratch/lpceg/yurii/iraklis/Makouski/CMSSW_5_3_12/src/ggAnalysis/ggNtuplizer/test/W3JetsToLNu_TuneZ2Star_8TeV-madgraph.root" \
"skim_W4jets.root /uscmst1b_scratch/lpc1/old_scratch/lpceg/yurii/iraklis/Makouski/CMSSW_5_3_12/src/ggAnalysis/ggNtuplizer/test/W4JetsToLNu_TuneZ2Star_8TeV-madgraph.root" \
"skim_data_mu_a.root /eos/uscms/store/user/iraklis/ggNtuples/job_muon_2012a_Jan22rereco.root" \
"skim_data_mu_b.root /eos/uscms/store/user/troy2012/TTGamma/job_muon_2012b_Jan22rereco.root" \
"skim_data_mu_c.root /eos/uscms/store/user/iraklis/ggNtuples/job_muon_2012c_Jan22rereco.root" \
"skim_data_mu_d.root /eos/uscms/store/user/troy2012/TTGamma/job_muon_2012d_Jan22rereco.root" \
"skim_ttg.root /uscmst1b_scratch/lpc1/cmsroc/yumiceva/TTGamma/CMSSW_5_3_12/src/ggAnalysis/ggNtuplizer/test/crab_projects/crab_ggNtuple_TTGamma_madgraph_test5/results/*.root" \
"skim_DYJetsToLL.root /eos/uscms/store/user/makouski/job_summer12_DYJetsToLL.root" \
"skim_ttjets_2l.root /eos/uscms/store/user/makouski/job_summer12_ttjets_2l.root" \
"skim_ttjets_1l.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_ttjets_1l.root" \
"skim_t_s.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_t_s.root" \
"skim_t_t.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_t_t.root" \
"skim_t_tW.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_t_tW.root" \
"skim_tbar_s.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_tbar_s.root" \
"skim_tbar_t.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_tbar_t.root" \
"skim_tbar_tW.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_tbar_tW.root" \
"skim_Zg.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_Zg.root" \
"skim_Wg.root /eos/uscms/store/user/iraklis/ggNtuples/job_summer12_Wg.root")

echo "NtuplePlotter/makeSkim ${outputDir}${inputfiles[job]}"
NtuplePlotter/makeSkim ${outputDir}${inputfiles[job]}
