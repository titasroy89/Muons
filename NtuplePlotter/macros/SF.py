
luminosity = 19.78*1000 # check runC lumi!
gSF = luminosity
# trigger and electron ID SF are included in event weights

TTJets1l_num        = 24849110 #
TTJets2l_num        = 12086717 #
TTJetsHad_num       = 31178278


#TTgamma_num      =  1719954 #

# /TTGamma_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_RD1_START53_V7N-v1/AODSIM
newTTgamma_num   =  832989 # new MG ttgamma sample 

WJets_num      = 57709905 #

W4Jets_num     = 11742268 # 7026978 # PART of the statistics!
W3Jets_num     = 15408303

ZJets_num      = 30458871 #

#ZZ_num            = 9799908 #AODSIM inclusive?

# 2e2mu + 2e2tau + 2mu2tau + 4e + 4mu + 4tau
ZZ_2e2mu_num       = 1497445
ZZ_2e2tau_num      = 823911
ZZ_2mu2tau_num     = 823922
ZZ_4e_num          = 1499093
ZZ_4mu_num         = 1499064
ZZ_4tau_num        = 824466

#WW_num            = 10000431 #AODSIM
WW_2l2nu_num       = 1933120 # 1903235 #


#WZ_num            = 10000283 #AODSIM
#WZ_num            = 5233969 # 
WZ_3lnu_num       = 2017979 #
WZ_2l2q_num       = 3215990 #

Wgamma_num        = 4877150 #

#WWgamma_num       = 304285 #

Zgamma_num        = 6588161 #

#TTW_num           = 196046 #
#TTZ_num           = 210160 #

WHIZARD_num       = 1074860 #

#SingToptW_num     = 497658
SingToptW_num     =  497658 #

#SingTopbartW_num  = 493460
SingTopbartW_num  =  493460 #

#SingTopT_num      = 3758227
SingTopT_num      =  99876 # small sample

#SingTopbarT_num   = 1935072
SingTopbarT_num   =  1935072 #

#SingTopS_num      = 259961
SingTopS_num      =  259961 #

#SingTopbarS_num   = 139974
SingTopbarS_num   =  139974 #

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGC
Zgamma_xs         = 159.12 # 132.6 # PREP
Wgamma_xs         = 553.92 # 461.6 # PREP
WWgamma_xs        = 1.44 #0.528 # PREP

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV

#Top_xs            = 239 # new measurement #227 #CMS measurement
TTJets1l_xs       = 104.7 # 239*0.676*(1-0.676)*2
TTJets2l_xs       = 25.09 # 239*(1-0.676)*(1-0.676)
TTJetsHad_xs      = 109.2 # 239*0.676*0.676

TTgamma_xs        = 0.9081 * 2  # https://twiki.cern.ch/twiki/bin/view/CMS/WhizardMCTeeTeeGamma
newTTgamma_xs     = 0.033 * 9 + 0.148 * 12 + 0.8 # 2l(NLO) + l+jets(NLO) + all_had (approx)  
WJets_xs          = 36257.0 # 35640.0 # CMS measurement. was: 36257.0  # 
ZJets_xs          = 3350.0 # CMS measurement. was: 3533.0 # 3503.71 #

#http://cms.cern.ch/iCMS/prep/requestmanagement?dsn=W4JetsToLNu*&campid=Summer12
W3Jets_xs         = 519.0 # PREP
W4Jets_xs         = 214.0 # PREP


#WZ_xs             = 33.21 # inclusive
WZ_3lnu_xs        = 1.057 # 0.8674 # PREP
WZ_2l2q_xs        = 5.995 # 1.755  # PREP

#ZZ_xs             = 8.06 # inclusive #  4l 0.009?, 2l2l 0.018?
ZZ_2e2mu_xs       = 0.1767 # PREP
ZZ_2e2tau_xs      = 0.1767 # PREP
ZZ_2mu2tau_xs     = 0.1767 # PREP
ZZ_4e_xs          = 0.07691 # PREP
ZZ_4mu_xs         = 0.07691 # PREP
ZZ_4tau_xs        = 0.07691 # PREP

# NLO? 5.995 # 4.7 PREP this is 2l2nu, inclusive is 54.8
# 69.9 CMS measurement
# 69.9*(1-0.676)*(1-0.676)
WW_2l2nu_xs       = 7.3
TTW_xs            = 0.232 #
TTZ_xs            = 0.208 #

SingToptW_xs      = 11.1 #
SingTopbartW_xs   = 11.1 #
SingTopT_xs       = 56.4 #
SingTopbarT_xs    = 30.7 #
SingTopS_xs       = 3.79 #
SingTopbarS_xs    = 1.76 #

