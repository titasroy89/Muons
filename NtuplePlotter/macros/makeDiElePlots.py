from distribution_mod import distribution
import ROOT

ROOT.gROOT.SetBatch()

# initialize variables, assign values later
WJetsSF = 0.0
TopSF = 1.0
QCDSF = 0.0

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


def loadMCTemplates(varList, inputDir, prefix, titleSuffix, fillStyle):
	templPrefix = inputDir+prefix
	
	MCtemplates = {}
	
	#MCtemplates['mst_510_200'] = distribution('mst_510_200'+titleSuffix,[
	#		(templPrefix+'mst_510_M3_5050_M1_200.root', gSF*0.0751004/15000)
	#	],varList, 620,3244)
	
	#MCtemplates['WHIZARD'] = distribution('TTGamma'+titleSuffix, [
	#	(templPrefix+'WHIZARD.root', TopSF*gSF*TTgamma_xs/WHIZARD_num)
	#	], varList, 98, fillStyle)
	
	MCtemplates['WHIZARD'] = distribution('TTGamma'+titleSuffix, [
		(templPrefix+'TTGamma.root', TopSF*gSF*newTTgamma_xs/newTTgamma_num)
		], varList, 97, fillStyle)
	
	MCtemplates['TTJets'] = distribution('TTJets'+titleSuffix, [
		(templPrefix+'TTJets1l.root', TopSF*gSF*TTJets1l_xs/TTJets1l_num),
		(templPrefix+'TTJets2l.root', TopSF*gSF*TTJets2l_xs/TTJets2l_num),
		#(templPrefix+'TTJetsHad.root', TopSF*gSF*TTJetsHad_xs/TTJetsHad_num),
		], varList ,11, fillStyle)
	
	###################################
	#return MCtemplates
	###################################
	nonWJetsSF = 1.0
	#nonWJetsSF = WJetsSF
	
	MCtemplates['Vgamma'] = distribution('Vgamma'+titleSuffix, [
        (templPrefix+'Zgamma.root', nonWJetsSF*gSF*Zgamma_xs/Zgamma_num),
        (templPrefix+'Wgamma.root', nonWJetsSF*gSF*Wgamma_xs/Wgamma_num),
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
		(templPrefix+'ZJets.root', nonWJetsSF*gSF*ZJets_xs/ZJets_num)], varList, 9, fillStyle)

	
	MCtemplates['Other'] = distribution('Diboson'+titleSuffix, [

        (templPrefix+'WZ_3lnu.root', nonWJetsSF*gSF*WZ_3lnu_xs/WZ_3lnu_num),
        (templPrefix+'WZ_2l2q.root', nonWJetsSF*gSF*WZ_2l2q_xs/WZ_2l2q_num),
        
        (templPrefix+'ZZ_2e2mu.root', nonWJetsSF*gSF*ZZ_2e2mu_xs/ZZ_2e2mu_num),
        (templPrefix+'ZZ_2e2tau.root', nonWJetsSF*gSF*ZZ_2e2tau_xs/ZZ_2e2tau_num),
        (templPrefix+'ZZ_2mu2tau.root', nonWJetsSF*gSF*ZZ_2mu2tau_xs/ZZ_2mu2tau_num),
        (templPrefix+'ZZ_4e.root', nonWJetsSF*gSF*ZZ_4e_xs/ZZ_4e_num),
        (templPrefix+'ZZ_4mu.root', nonWJetsSF*gSF*ZZ_4mu_xs/ZZ_4mu_num),
        (templPrefix+'ZZ_4tau.root', nonWJetsSF*gSF*ZZ_4tau_xs/ZZ_4tau_num),
        
        (templPrefix+'WW_2l2nu.root', nonWJetsSF*gSF*WW_2l2nu_xs/WW_2l2nu_num),

          #(templPrefix+'TTW.root', gSF*TTW_xs/TTW_num),
          #(templPrefix+'TTZ.root', gSF*TTZ_xs/TTZ_num),
		], varList, 49, fillStyle)

	return MCtemplates


def makeAllPlots(varList, inputDir, dataDir, outDirName):
	# load templates PreSel	
	DataTempl = loadDataTemplate(varList, dataDir, 'hist_1pho_top_')

	MCTemplDict = loadMCTemplates(varList, inputDir, 'hist_1pho_top_','',1001)
	MCTempl = []
	MCTempl.append(MCTemplDict['WHIZARD'])
	MCTempl.append(MCTemplDict['TTJets'])
	MCTempl.append(MCTemplDict['Vgamma'])
	MCTempl.append(MCTemplDict['SingleTop'])
	MCTempl.append(MCTemplDict['WJets'])
	MCTempl.append(MCTemplDict['ZJets'])
	MCTempl.append(MCTemplDict['Other'])
	
	saveTemplatesToFile([DataTempl] + MCTempl, ['MET','ele1ele2Mass'], outDirName+'/templates_presel.root')
	
	plotTemplates( DataTempl, MCTempl, [], varList, outDirName+'/presel')
	


varList_all = ['nVtx',
			'MET','Ht','WtransMass','M3','M3first','minM3','M3pho','dRpho3j','M3phoMulti', 
			#'M3_0_30', 'M3_30_100', 'M3_100_200', 'M3_200_300', 'M3_300_up', #'M3minPt',
			'ele1Pt','ele1Eta','ele1RelIso',
			'ele1D0','ele1MVA','ele1Dz',
			'ele2Pt','ele2RelIso',
			'ele1ele2Mass',
			'ele1sigmaIetaIeta','ele1EoverP',
			'ele1DrJet','ele1pho1Mass',
			'looseEleDrGenPho',
			'cut_flow',
			'genPhoRegionWeight',
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

InputHist = '/Users/makouski/dis/plotting_trees/new_hist/hist_zeroB_twoEle/'
DataHist = '/Users/makouski/dis/plotting_trees/new_hist/hist_zeroB_twoEle/'

#InputHist = '/Users/makouski/dis/plotting_trees/new_hist/hist_twoEle/'
#DataHist = '/Users/makouski/dis/plotting_trees/new_hist/hist_twoEle/'


makeAllPlots(varList_all, InputHist, DataHist, 'di_ele_cross_check/plots')
