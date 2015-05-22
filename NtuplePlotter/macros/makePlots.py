from distribution_mod import distribution
import ROOT
import sys

import templateFits
import qcd_fit
import calc_the_answer
import vgamma_fit

ROOT.gROOT.SetBatch()

isSyst = False
systematic = ''
if len(sys.argv) > 1:
	print sys.argv
	systematic = sys.argv[1]
	if systematic != 'zeroB':
		isSyst = True
		sys.stdout = open('ratio_'+systematic+'.txt','w')

# initialize variables, assign values later
WJetsSF = 1.0
TopSF = 1.0
QCDSF = 0.0
ZJetsSF = 1.0 #1.20 
ZJetsSFErr = 0.06
if systematic == 'ZJetsSF_up':
	ZJetsSF += ZJetsSFErr
if systematic == 'ZJetsSF_down':
	ZJetsSF -= ZJetsSFErr
if systematic == 'zeroB':
	ZJetsSF = 1.0

VgammaSF = 1.0 

#import array
#binarray = array.array('d')
#binarray.fromlist([0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,300])

# load cross-sections and N gen as global variables
execfile('SF.py')

# function definitions ####################################################

def saveTemplatesToFile(templateList, varlist, outFileName):
	outfile = ROOT.TFile(outFileName,'RECREATE')
	for template in templateList:
		for var in varlist:
			template.histList[var].SetDirectory(outfile.GetDirectory(''))
			template.histList[var].Write()
			template.histList[var].SetDirectory(0)
	outfile.Close()

def plotTemplates(dataTemplate, MCTemplateList, SignalTemplateZoomList, varlist, outDirName):
	canvas = ROOT.TCanvas('c1','c1',640,800)
	
	latex = ROOT.TLatex()
	latex.SetNDC()
	latex.SetTextAlign(12)
	latex.SetTextSize(0.037)
	latex.SetLineWidth(2)
	
	for var in varlist:
		legend = ROOT.TLegend(0.7, 1 - 0.05*(1 + len(MCTemplateList) + len(SignalTemplateZoomList)), 0.99, 1.00)
		legend.SetBorderSize(0)
		legend.SetFillColor(10)
		
		if dataTemplate is not None:
			legend.AddEntry(dataTemplate.histList[var], dataTemplate.name, 'pl')
		
		# MC templates listed in the order they appear in legend
		for mc in MCTemplateList:
			mcHist = mc.histList[var]
			legend.AddEntry(mcHist, mc.name, 'f')
		
		stack = ROOT.THStack('stack_'+var,var)
		# reverse order for stack to be consistent with legend
		MCTemplateList.reverse()
		for mc in MCTemplateList:
			mcHist = mc.histList[var]
			#if var == 'M3pho':
			#	mcHist.Rebin(2)
			stack.Add(mcHist)
		MCTemplateList.reverse()

		if dataTemplate is not None:
			#if var == 'M3pho':
			#	dataTemplate.histList[var].Rebin(2)
			if dataTemplate.histList[var].GetMaximum() > stack.GetMaximum():
				stack.SetMaximum(dataTemplate.histList[var].GetMaximum())

		if 'cut_flow' in var: # or 'MET' in var:
			canvas.SetLogy(1)
			stack.SetMinimum(100)
		else:
			canvas.SetLogy(0)
		
		stack.Draw('HIST')
		if 'mu1RelIso' in var:
			canvas.SetLogy()
		
		if 'barrel' in outDirName and 'photon1SigmaIEtaIEta' in var:
			stack.GetXaxis().SetRangeUser(0.0,0.025)
		
		if dataTemplate is not None:
			stack.GetXaxis().SetTitle(dataTemplate.histList[var].GetXaxis().GetTitle())
			stack.GetYaxis().SetTitle(dataTemplate.histList[var].GetYaxis().GetTitle())
		stack.SetTitle('')

		if dataTemplate is not None:
			dataTemplate.histList[var].Draw('ESAME')
					
		for signal,zoom in SignalTemplateZoomList:
			sigHist = signal.histList[var].Clone()
			#sigHist.SetFillStyle(3244)
			sigHist.Scale(zoom)
			sigHist.Draw('HISTSAME')
			if zoom != 1:
				legend.AddEntry(sigHist, signal.name + ' x ' + str(zoom), 'f')
			else:
				legend.AddEntry(sigHist, signal.name, 'f')
		if 'cut_flow' not in var:
			legend.Draw()
		
		latex.DrawLatex(0.1,0.94,'CMS Preliminary #sqrt{s} = 8 TeV')
		if not isSyst:
			canvas.SaveAs(outDirName+'/'+var+'.png')
		
def loadDataTemplate(varlist, inputDir, prefix):
	templPrefix = inputDir+prefix
	DataTempl = distribution('Data', [
		(templPrefix+'Data_a.root', 1),
		(templPrefix+'Data_b.root', 1),
		(templPrefix+'Data_c.root', 1),
		(templPrefix+'Data_d.root', 1),
		], varlist)
	return DataTempl

def loadQCDTemplate(varlist, inputDir, prefix):
	templPrefix = inputDir+prefix
	QCD_sf = QCDSF
	QCDTempl = distribution('QCD', [
		(templPrefix+'Data_a.root', QCD_sf),
		(templPrefix+'Data_b.root', QCD_sf),
		(templPrefix+'Data_c.root', QCD_sf),
		(templPrefix+'Data_d.root', QCD_sf),
		(templPrefix+'TTJets1l.root', -1 * QCD_sf * gSF * TTJets1l_xs/TTJets1l_num),
		(templPrefix+'TTJets2l.root', -1 * QCD_sf * gSF * TTJets2l_xs/TTJets2l_num),
	], varlist, 46)
	return QCDTempl

def loadMCTemplates(varList, inputDir, prefix, titleSuffix, fillStyle):
	templPrefix = inputDir+prefix
	
	MCtemplates = {}
	
	#MCtemplates['WHIZARD'] = distribution('TTGamma'+titleSuffix, [
	#	(templPrefix+'WHIZARD.root', TopSF*gSF*TTgamma_xs/WHIZARD_num)
	#	], varList, 98, fillStyle)
	
	MCtemplates['WHIZARD'] = distribution('TTGamma'+titleSuffix, [
		(templPrefix+'TTGamma.root', TopSF*gSF*newTTgamma_xs/newTTgamma_num)
		], varList, 97, fillStyle)
	
	MCtemplates['TTJets'] = distribution('TTJets'+titleSuffix, [
		(templPrefix+'TTJets1l.root', TopSF*gSF*TTJets1l_xs/TTJets1l_num),
		(templPrefix+'TTJets2l.root', TopSF*gSF*TTJets2l_xs/TTJets2l_num),
		(templPrefix+'TTJetsHad.root', TopSF*gSF*TTJetsHad_xs/TTJetsHad_num),
		], varList ,11, fillStyle)
	
	###################################
	#return MCtemplates
	###################################
	nonWJetsSF = 1.0
		
	MCtemplates['Vgamma'] = distribution('Vgamma'+titleSuffix, [
        (templPrefix+'Zgamma.root', VgammaSF*nonWJetsSF*gSF*Zgamma_xs/Zgamma_num),
        (templPrefix+'Wgamma.root', VgammaSF*nonWJetsSF*gSF*Wgamma_xs/Wgamma_num),
    #    (templPrefix+'WWgamma.root', gSF*WWgamma_xs/WWgamma_num),
        ], varList, 90, fillStyle)

	MCtemplates['SingleTop'] = distribution('SingleTop'+titleSuffix, [
		(templPrefix+'SingleT_t.root',      nonWJetsSF*gSF*SingTopT_xs/SingTopT_num),
        (templPrefix+'SingleT_s.root',      nonWJetsSF*gSF*SingTopS_xs/SingTopS_num),
        (templPrefix+'SingleT_tw.root',     nonWJetsSF*gSF*SingToptW_xs/SingToptW_num),
        (templPrefix+'SingleTbar_t.root',   nonWJetsSF*gSF*SingTopbarT_xs/SingTopbarT_num),
        (templPrefix+'SingleTbar_s.root',   nonWJetsSF*gSF*SingTopbarS_xs/SingTopbarS_num),
        (templPrefix+'SingleTbar_tw.root',  nonWJetsSF*gSF*SingTopbartW_xs/SingTopbartW_num),
		], varList, 8, fillStyle)
	
	MCtemplates['WJets'] = distribution('WJets'+titleSuffix, [
        #(templPrefix+'WJets.root', WJetsSF*gSF*WJets_xs/WJets_num),
		(templPrefix+'W3Jets.root', WJetsSF*gSF*W3Jets_xs/W3Jets_num),
		(templPrefix+'W4Jets.root', WJetsSF*gSF*W4Jets_xs/W4Jets_num),
		], varList, 7, fillStyle)
		
	MCtemplates['ZJets'] = distribution('ZJets'+titleSuffix, [
		(templPrefix+'ZJets.root', ZJetsSF*nonWJetsSF*gSF*ZJets_xs/ZJets_num)], varList, 9, fillStyle)

	
	#MCtemplates['Other'] = distribution('Diboson'+titleSuffix, [

        #(templPrefix+'WZ_3lnu.root', nonWJetsSF*gSF*WZ_3lnu_xs/WZ_3lnu_num),
        #(templPrefix+'WZ_2l2q.root', nonWJetsSF*gSF*WZ_2l2q_xs/WZ_2l2q_num),
        
        #(templPrefix+'ZZ_2e2mu.root', nonWJetsSF*gSF*ZZ_2e2mu_xs/ZZ_2e2mu_num),
        #(templPrefix+'ZZ_2e2tau.root', nonWJetsSF*gSF*ZZ_2e2tau_xs/ZZ_2e2tau_num),
        #(templPrefix+'ZZ_2mu2tau.root', nonWJetsSF*gSF*ZZ_2mu2tau_xs/ZZ_2mu2tau_num),
        #(templPrefix+'ZZ_4e.root', nonWJetsSF*gSF*ZZ_4e_xs/ZZ_4e_num),
        #(templPrefix+'ZZ_4mu.root', nonWJetsSF*gSF*ZZ_4mu_xs/ZZ_4mu_num),
        #(templPrefix+'ZZ_4tau.root', nonWJetsSF*gSF*ZZ_4tau_xs/ZZ_4tau_num),
        
        #(templPrefix+'WW_2l2nu.root', nonWJetsSF*gSF*WW_2l2nu_xs/WW_2l2nu_num),

          #(templPrefix+'TTW.root', gSF*TTW_xs/TTW_num),
          #(templPrefix+'TTZ.root', gSF*TTZ_xs/TTZ_num),
	#	], varList, 49, fillStyle)

	return MCtemplates

def saveAccTemplates(inputDir, outFileName):
	varList = ['MCcategory']
	AccTemplates = {}
	
	AccTemplates['TTGamma'] = distribution('TTGamma_signal', [
		(inputDir+'hist_1pho_rs_barrel_top_TTGamma.root', 1.0),
		], varList, 97)
		
	AccTemplates['TTGamma_presel'] = distribution('TTGamma_presel', [
		(inputDir+'hist_1pho_top_TTGamma.root', 1.0),
		], varList, 97)
	AccTemplates['TTJets1l'] = distribution('TTJets1l_presel', [
		(inputDir+'hist_1pho_top_TTJets1l.root', 1.0),
		], varList ,11)
	AccTemplates['TTJets2l'] = distribution('TTJets2l_presel', [
		(inputDir+'hist_1pho_top_TTJets2l.root', 1.0),
		], varList ,11)
	AccTemplates['TTJetsHad'] = distribution('TTJetsHad_presel', [
		(inputDir+'hist_1pho_top_TTJetsHad.root', 1.0),
		], varList ,11)
	
	saveTemplatesToFile(AccTemplates.values(), varList, outFileName)

def saveNoMETTemplates(inputDir, inputData, outFileName):
	varList = ['MET','M3']
	DataTempl = loadDataTemplate(varList, inputData, 'hist_1phoNoMET_top_')
	MCTemplDict = loadMCTemplates(varList, inputDir, 'hist_1phoNoMET_top_','',1001)
	MCTempl = []
	MCTempl.append(MCTemplDict['WHIZARD'])
	MCTempl.append(MCTemplDict['TTJets'])
	MCTempl.append(MCTemplDict['Vgamma'])
	MCTempl.append(MCTemplDict['SingleTop'])
	MCTempl.append(MCTemplDict['WJets'])
	MCTempl.append(MCTemplDict['ZJets'])
	saveTemplatesToFile([DataTempl] + MCTempl, varList, outFileName)

def saveBarrelFitTemplates(inputDir, inputData,  outFileName):
	varList = ['MET','M3','photon1ChHadSCRIso', 'photon1ChHadRandIso', 'photon1_Sigma_ChSCRIso']
	DataTempl_b = loadDataTemplate(varList, inputData, 'hist_1pho_barrel_top_')
	
	MCTempl_b = loadMCTemplates(varList, inputDir, 'hist_1pho_barrel_top_','',1001)	
	MCTempl_rs_b = loadMCTemplates(varList, inputDir, 'hist_1pho_rs_barrel_top_', '_signal', 1001)
	MCTempl_fe_b = loadMCTemplates(varList, inputDir, 'hist_1pho_fe_barrel_top_', '_electron', 3005)
	MCTempl_fjrb_b = loadMCTemplates(varList, inputDir, 'hist_1pho_fjrb_barrel_top_', '_fake', 3005)
	
	saveTemplatesToFile([DataTempl_b] +  MCTempl_b.values() + MCTempl_rs_b.values() + MCTempl_fe_b.values() + MCTempl_fjrb_b.values(), varList, outFileName)

def savePreselTemplates(inputDir, qcdDir, inputData, outFileName):
	if WJetsSF != 1.0 or TopSF != 1.0:
		print 'We want to save templates for M3 fit, but the SFs are not 1.0'
		print 'exiting'
		return
	
	varList = ['MET','M3',]
	DataTempl = loadDataTemplate(varList, inputData, 'hist_1pho_top_')
	if QCDSF > 0.0001:
		QCDTempl = loadQCDTemplate(varList, qcdDir, 'hist_1pho_top_')
	else:
		print 'The purpose of this function is to save templates for M3 fit, without QCD it is useless'
	
	MCTemplDict = loadMCTemplates(varList, inputDir, 'hist_1pho_top_','',1001)
	MCTempl = []
	MCTempl.append(MCTemplDict['WHIZARD'])
	MCTempl.append(MCTemplDict['TTJets'])
	MCTempl.append(MCTemplDict['Vgamma'])
	MCTempl.append(MCTemplDict['SingleTop'])
	MCTempl.append(MCTemplDict['WJets'])
	MCTempl.append(MCTemplDict['ZJets'])
	if QCDSF > 0.0001:
		MCTempl.append(QCDTempl)
	saveTemplatesToFile([DataTempl] + MCTempl, varList, outFileName)


def makeAllPlots(varList, inputDir, qcdDir, dataDir, outDirName):
	# load templates PreSel	
	DataTempl = loadDataTemplate(varList, dataDir, 'hist_1pho_top_') #NoMET
	if QCDSF > 0.0001:
		QCDTempl = loadQCDTemplate(varList, qcdDir, 'hist_1pho_top_') #NoMET
	MCTemplDict = loadMCTemplates(varList, inputDir, 'hist_1pho_top_','',1001) #NoMET
	MCTempl = []
	MCTempl.append(MCTemplDict['WHIZARD'])
	MCTempl.append(MCTemplDict['TTJets'])
	MCTempl.append(MCTemplDict['Vgamma'])
	MCTempl.append(MCTemplDict['SingleTop'])
	MCTempl.append(MCTemplDict['WJets'])
	MCTempl.append(MCTemplDict['ZJets'])
	if QCDSF > 0.0001:
		MCTempl.append(QCDTempl)
	
	
	# save final templates, exactly as they are on the plots
	saveTemplatesToFile([DataTempl] + MCTempl, ['MET','M3','WtransMass','genPhoRegionWeight','MCcategory'], 'templates_presel_scaled.root')
	
	plotTemplates( DataTempl, MCTempl, [], varList, outDirName+'/presel')
	
	
	shortVarList = varList[:]
	shortVarList.remove('cut_flow')
	shortVarList.remove('genPhoRegionWeight')
	
	region = 'barrel'
	# load templates
	DataTempl_b = loadDataTemplate(shortVarList, dataDir, 'hist_1pho_'+region+'_top_')
	if QCDSF > 0.0001:
		QCDTempl_b = loadQCDTemplate(shortVarList, qcdDir, 'hist_1pho_'+region+'_top_')
	MCTemplDict_b = loadMCTemplates(shortVarList, inputDir, 'hist_1pho_'+region+'_top_','',1001)
	MCTempl_b = []
	MCTempl_b.append(MCTemplDict_b['WHIZARD'])
	MCTempl_b.append(MCTemplDict_b['TTJets'])
	MCTempl_b.append(MCTemplDict_b['Vgamma'])
	MCTempl_b.append(MCTemplDict_b['SingleTop'])
	MCTempl_b.append(MCTemplDict_b['WJets'])
	MCTempl_b.append(MCTemplDict_b['ZJets'])
	if QCDSF > 0.0001:
		MCTempl_b.append(QCDTempl_b)
	
	MCTempl_rs_b = loadMCTemplates(shortVarList, inputDir, 'hist_1pho_rs_barrel_top_', '_signal', 1001)
	MCTempl_fe_b = loadMCTemplates(shortVarList, inputDir, 'hist_1pho_fe_barrel_top_', '_electron', 3005)
	MCTempl_fjrb_b = loadMCTemplates(shortVarList, inputDir, 'hist_1pho_fjrb_barrel_top_', '_fake', 3005)
	
	# save final templates, exactly as they are on the plots and by categories
	saveTemplatesToFile([DataTempl_b] + MCTempl_b + MCTempl_rs_b.values() + MCTempl_fe_b.values() + MCTempl_fjrb_b.values(), 
		['MET','M3','WtransMass','MCcategory','nJets'], 
		'templates_barrel_scaled.root'
		)
	
	plotTemplates( DataTempl_b, MCTempl_b, [], shortVarList, outDirName+'/'+region+'_samples')
	
	############################
	return
	############################


varList_all = ['nVtx',
			'MET','Ht','WtransMass','M3', 
			#'M3_0_30', 'M3_30_100', 'M3_100_200', 'M3_200_300', 'M3_300_up', #'M3minPt',
			'mu1Pt','mu1Eta','mu1RelIso',
			'genPhoRegionWeight', 'MCcategory',
			'cut_flow',
			'nJets',
			'jet1Pt','jet2Pt','jet3Pt','jet4Pt','jet1Eta','jet2Eta','jet3Eta','jet4Eta',
			'photon1Et','photon1Eta','photon1HoverE','photon1SigmaIEtaIEta',
			'photon1DrElectron','photon1DrJet',
			'photon1ChHadIso','photon1NeuHadIso','photon1PhoIso',
			'photon1ChHadSCRIso','photon1PhoSCRIso',
			'photon1ChHadRandIso','photon1PhoRandIso',
			'photon1MotherID','photon1GMotherID','photon1DrMCbquark','GenPhotonEt',
			#'photon1_Sigma_ChSCRIso'
			]
# main part ##############################################################################################
if systematic in ['Btag_down','Btag_up','EleEff_down','EleEff_up','JEC_down','JEC_up','JER_down','JER_up','PU_down','PU_up','elesmear_down','elesmear_up','pho_down','pho_up','toppt_down','toppt_up']:
	outSuffix = '_'+systematic
else:
	outSuffix = ''

InputHist = '../../hist'+outSuffix+'/'
QCDHist = '../../QCD/'
DataHist = '../../hist/'

# TTJets and TTGamma acceptance histograms
saveAccTemplates(InputHist, 'ttbar_acceptance.root')

### templates for data driven fit or closure test. No rescaling necessary
saveBarrelFitTemplates(InputHist, DataHist, 'templates_barrel.root')
templateFits.InputFilename = 'templates_barrel.root'
templateFits.fitData = False ## to do closure test
##templateFits.NpseudoExp = 3000
#phoPurity,phoPurityError = 0.534, 0.0564 #0.506, 0.078  #0.564, 0.063 #### 0.556427532887, 0.0616417156454 ## auto binsize: 0.561220079533, 0.0529980243576
phoPurity,phoPurityError,MCfrac = templateFits.doTheFit()
#exit()
# for MET fit. No rescaling
if WJetsSF == 1.0 and TopSF == 1.0:
	saveNoMETTemplates(InputHist, DataHist, 'templates_presel_nomet.root')
	saveNoMETTemplates(QCDHist, QCDHist, 'templates_presel_nomet_qcd.root')

qcd_fit.qcdMETfile = 'templates_presel_nomet_qcd.root'
qcd_fit.normMETfile = 'templates_presel_nomet.root'

QCDSF,QCDSFerror = qcd_fit.doQCDfit()

# for systematics of QCD fit
if systematic == 'QCD_up':
	QCDSF *= 2
if systematic == 'QCD_down':
	QCDSF /= 2
# save templates for M3 fit
savePreselTemplates(InputHist, QCDHist, DataHist, 'templates_presel.root')

# do M3 fit, update SF for Top and WJets
qcd_fit.M3file = 'templates_presel.root'
TopSF, TopSFerror, WJetsSF, WJetsSFerror = qcd_fit.doM3fit()

makeAllPlots(varList_all, InputHist, QCDHist, DataHist, 'plots')

M3_photon_topFrac, M3_photon_topFracErr = vgamma_fit.doM3fit_photon()
print '*'*80
#exit()

calc_the_answer.TTJets1l_num = TTJets1l_num
calc_the_answer.TTJets2l_num = TTJets2l_num
calc_the_answer.TTJetsHad_num = TTJetsHad_num

calc_the_answer.photnPurity = phoPurity
calc_the_answer.photnPurityErr = phoPurityError
calc_the_answer.eleFakeSF = 1.5
calc_the_answer.eleFakeSFErr = 0.2
if systematic == 'EleFakeSF_up':
	calc_the_answer.eleFakeSF = 1.5 + 0.2
if systematic == 'EleFakeSF_down':
	calc_the_answer.eleFakeSF = 1.5 - 0.2

calc_the_answer.M3TopSF = TopSF
calc_the_answer.M3TopSFErr = TopSFerror
calc_the_answer.M3WJetsSF = WJetsSF
calc_the_answer.M3WJetsSFErr = WJetsSFerror
calc_the_answer.M3_photon_topFrac = M3_photon_topFrac
calc_the_answer.M3_photon_topFracErr = M3_photon_topFracErr

calc_the_answer.doTheCalculation()

