import ROOT
ROOT.gROOT.SetBatch()
import array

def makeFit(varname, varmin, varmax, signalHist, backgroundHist, dataHist, plotName):
	# RooFit variables
	sihihVar = ROOT.RooRealVar(varname, varname, varmin, varmax)
	sihihArgList = ROOT.RooArgList()
	sihihArgList.add(sihihVar)
	sihihArgSet = ROOT.RooArgSet()
	sihihArgSet.add(sihihVar)

	# create PDFs
	signalDataHist = ROOT.RooDataHist('signalDataHist','signal RooDataHist', sihihArgList, signalHist)
	signalPdf = ROOT.RooHistPdf('signalPdf',varname+' of signal', sihihArgSet, signalDataHist)

	backgroundDataHist = ROOT.RooDataHist('backgroundDataHist','background RooDataHist', sihihArgList, backgroundHist)
	backgroundPdf = ROOT.RooHistPdf('backgroundPdf',varname+' of background', sihihArgSet, backgroundDataHist)

	# data
	dataDataHist = ROOT.RooDataHist('data '+varname, varname+' in Data', sihihArgList, dataHist)

	# signal fraction parameter
	signalFractionVar = ROOT.RooRealVar('signal fraction','signal fraction', 0.5, 0.0, 1.0)
	sumPdf = ROOT.RooAddPdf('totalPdf','signal and background', signalPdf, backgroundPdf, signalFractionVar)
	
	# fit
	sumPdf.fitTo( dataDataHist, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.PrintLevel(-1) )
	
	if plotName!='':
		# plot results
		c1 = ROOT.TCanvas('c1', 'c1', 800, 600)
		plotter = ROOT.RooPlot(sihihVar,varmin,varmax,20) # nBins is dummy 
		dataDataHist.plotOn(plotter, ROOT.RooFit.Name('data'))
		sumPdf.plotOn(plotter, ROOT.RooFit.Name('sum'), ROOT.RooFit.LineColor(ROOT.kRed))
		sumPdf.plotOn(plotter, ROOT.RooFit.Components('signalPdf'), ROOT.RooFit.Name('signal'), 
			ROOT.RooFit.LineColor(ROOT.kGreen))
		sumPdf.plotOn(plotter, ROOT.RooFit.Components('backgroundPdf'), ROOT.RooFit.Name('background'), 
			ROOT.RooFit.LineColor(ROOT.kBlue))
		sumPdf.paramOn(plotter)

		plotter.Draw()
		c1.SaveAs(plotName)
	print 'fit returned value ',signalFractionVar.getVal(),' +- ',signalFractionVar.getError()
	return (signalFractionVar.getVal(),signalFractionVar.getError())
	

openfiles = {}

def get1DHist(filename, histname):
	if filename not in openfiles:
		openfiles[filename] = ROOT.TFile(filename,'READ')
	file = openfiles[filename]
		
	hist = file.Get(histname)
	hist.SetDirectory(0)
	hist.SetFillColor(0)
	#hist.Sumw2()
	return hist

def getTemplFrom2Dhist(filename, histname, auxAxis, minval, maxval):
	if filename not in openfiles:
		openfiles[filename] = ROOT.TFile(filename,'READ')
	file = openfiles[filename]

	hist2d = file.Get(histname)
	hist2d.SetDirectory(0)
	
	if auxAxis == 'Y':
		firstBin = hist2d.GetYaxis().FindBin(minval)
		lastBin = hist2d.GetYaxis().FindBin(maxval)# - 1
	elif auxAxis == 'X':
		firstBin = hist2d.GetXaxis().FindBin(minval)
		lastBin = hist2d.GetXaxis().FindBin(maxval)# - 1
	else:
		print 'ERROR: valid values for auxAxis are X or Y'
		return None

	#print 'Getting histogram ',filename,' : ',histname
	#print 'Projection with auxAxis ', auxAxis, '  range ', minval, maxval, '  bins ', firstBin, lastBin
	
	if auxAxis == 'Y':
		templhist = hist2d.ProjectionX('projX'+filename+histname+'_'+str(minval)+'_'+str(maxval), firstBin,lastBin)
	else:
		templhist = hist2d.ProjectionY('projY'+filename+histname+'_'+str(minval)+'_'+str(maxval), firstBin,lastBin)
	templhist.SetDirectory(0)
	templhist.SetFillColor(0)
	#templhist.Sumw2()
	
	return templhist

def optimizeBinBoundaries(hist, minAcc, firstBinValue=-9999, lastBinValue=9999):
	nbins = hist.GetNbinsX()
	accu = 0
	binlist = []
	
	# ignore empty bins in the beginning
	for firstind in xrange(1,nbins+1):
		#if hist.GetBinContent(firstind) > 0.0001 and hist.GetBinLowEdge(firstind)>=firstBinValue:
		if hist.GetBinLowEdge(firstind)>=firstBinValue:
			binlist.append(hist.GetBinLowEdge(firstind))
			break
	
	for ind in xrange(firstind,nbins+1):
		if hist.GetBinLowEdge(ind)>=lastBinValue:
			binlist.append(lastBinValue)
			break
		if accu > minAcc:
			accu=0
			binlist.append(hist.GetBinLowEdge(ind))
		accu+=hist.GetBinContent(ind)
		#print 'bin ', ind, '  value ', hist.GetBinContent(ind), '  low and high edges ', hist.GetBinLowEdge(ind), hist.GetBinLowEdge(ind+1)
	binlist.append(hist.GetBinLowEdge(nbins+1))
	print binlist
	newarray = array.array('d')
	newarray.fromlist(binlist)
	return newarray
	
def makeUniformHist(hist):
	nbins = hist.GetNbinsX()
	#print 'nbins',nbins
	outhist = ROOT.TH1F(hist.GetName()+'_uni',hist.GetName()+'_uni',nbins,1,nbins+1)
	for ind in xrange(1,nbins+1):
		outhist.SetBinContent(ind,hist.GetBinContent(ind))
		outhist.SetBinError(ind,hist.GetBinError(ind))
	return outhist


random = ROOT.TRandom3()

def makeRandUniformHist(hist):
	nbins = hist.GetNbinsX()
	#print 'nbins',nbins
	outhist = ROOT.TH1F(hist.GetName()+'_uni',hist.GetName()+'_uni',nbins,1,nbins+1)
	for ind in xrange(1,nbins+1):
		outhist.SetBinContent(ind, random.Poisson(hist.GetBinContent(ind)))
	return outhist


def getWeightedHist(selection, filename, histName, leftCut=None, rightCut=None):
	suffix = None
	if selection=='': suffix = '_'
	elif selection=='data': suffix = '_'
	elif selection=='rs': suffix = '_signal_'
	elif selection=='fjrb': suffix = '_fake_'
	elif selection=='fe': suffix = '_electron_'
	if suffix==None: 
		print '#############################  wrong parameter!!!'
		return None
	global datasetsToMix
	Snames = datasetsToMix
	if selection=='data':
		Snames = ['Data']
	
	global signalSF
    
	if leftCut==None and rightCut==None:
		# 1d histogram 
		sumHist = get1DHist(filename, Snames[0]+suffix+histName)
		sumHist.Scale(signalSF)
		for sampl in Snames[1:]:
			sumHist.Add(get1DHist(filename, sampl+suffix+histName))
		return sumHist
	else:
		# 2d histogram projection
		sumHistp = getTemplFrom2Dhist(filename, Snames[0]+suffix+histName, 'X', leftCut, rightCut)
		sumHistp.Scale(signalSF)
		for sampl in Snames[1:]:
			sumHistp.Add(getTemplFrom2Dhist(filename, sampl+suffix+histName, 'X', leftCut, rightCut))
		return sumHistp

# fit range
lowFitrange = -0.6
highFitrange = 19.99
#highFitrange = 4.99

selectionRange = 4.99

# signal scale factor. for procedure linearity test
signalSF = 1.0
# datasets to mix
datasetsToMix = ['TTGamma','TTJets', 'Vgamma', 'ZJets', 'SingleTop']  #,'Vgamma','SingleTop','Other']

# number of pseudo experiments. off by default reasonable resuts for 1000 or so
NpseudoExp = 0

# use MC (closure test) or Data
fitData = True

# photon Et range
#phoEtrange = '_60_up_'
phoEtrange = '_' # all Et

FitVarname = 'SCRChHadIso'
hist2d_name = 'photon1'+phoEtrange+'Sigma_ChSCRIso'
if phoEtrange=='_': phoEtrange = ''
hist_sig_templ_name = 'photon1'+phoEtrange+'ChHadRandIso'
hist_sig_name = 'photon1ChHadSCRIso'

InputFilename =  'templates_barrel.root'
#ZeroBFilename = 'zerob_templ/templates_barrel.root'

usePhoIso = False
#usePhoIso = True
# for Pho Iso
if usePhoIso:
	FitVarname = 'SCRPhoIso'
	hist2d_name = 'photon1_Sigma_PhoSCRIso'
	hist_sig_templ_name = 'photon1PhoRandIso'
	hist_sig_name = 'photon1PhoSCRIso'
	lowFitrange = -3.0
	highFitrange = 9.99


# nominal selection cut
sihihSelCut = 0.01199

# sideband in sigmaIetaIeta
sbLeft = 0.012
sbRight = 0.01599

#sbLeft = 0.011
#sbRight = 0.014

def doTheFit():

	if fitData:
		reqStr = 'data'
	else:
		reqStr = ''

	# signal template, data driven, random cone isolation
	sig_templ = getWeightedHist(reqStr, InputFilename, hist_sig_templ_name)
	
	# experiment: MC truth shapes
	#sig_templ = getWeightedHist('rs', InputFilename, hist2d_name, 0.0, sihihSelCut)
	#sig_templ.Add(getWeightedHist('fe', InputFilename, hist2d_name, 0.0, sihihSelCut))
	#bckg_templ = getWeightedHist('fjrb', InputFilename, hist2d_name, 0.0, sihihSelCut)
	
	# background template, data driven, sideband in sihih
	# experiment
	#bckg_templ = getWeightedHist(reqStr, ZeroBFilename, hist2d_name, sbLeft, sbRight)
	bckg_templ = getWeightedHist(reqStr, InputFilename, hist2d_name, sbLeft, sbRight)
	
	# data, no cut on isolation, cut on sihih
	pseudodata = getWeightedHist(reqStr, InputFilename, hist2d_name, 0.0, sihihSelCut)


	### MC truth for SCR isolation selection, for true signal fraction calculation
	pseudosignal = getWeightedHist('rs', InputFilename, hist2d_name, 0.0, sihihSelCut)
	pseudosignal.Add( getWeightedHist('fe', InputFilename, hist2d_name, 0.0, sihihSelCut) )
	
	leftbin = pseudodata.FindBin(lowFitrange)
	rightbin = pseudodata.FindBin(highFitrange)
	print 'calculating integrals in bins',leftbin,rightbin
	#print 'MC truth signal integral in fitrnge',pseudosignal.Integral(leftbin, rightbin)
	MCtrueSelSignalFraction = pseudosignal.Integral(leftbin, rightbin)/pseudodata.Integral(leftbin, rightbin)
	########################################

	if phoEtrange:
		print 'Photon Et range: ',phoEtrange
	else:
		print 'Photon Et range: all'

	print 'Signal Integral: ',sig_templ.Integral()
	print 'Background Integral: ',bckg_templ.Integral()
	print 'Data Integral: ',pseudodata.Integral()

	# make equal binning in all histograms
	bckg_templ.Rebin(2)
	pseudodata.Rebin(2)

	#boundaries = optimizeBinBoundaries(pseudodata,15,lowFitrange,highFitrange)
	boundaries = optimizeBinBoundaries(bckg_templ, 10, lowFitrange, highFitrange)
	
	if fitData:
		binlist = [-0.5, 0.8, 2.2, 5.0, 10.0, 20.0]
		print 'using custom bins for Data:',binlist
		boundaries = array.array('d')
		boundaries.fromlist(binlist)

	#### test with MC truth shapes ###
	#sig_templ = pseudosignal
	#sig_templ.Rebin(2)
	#bckg_templ = getWeightedHist('fjrb', InputFilename, hist2d_name, 0.0, sihihSelCut)
	#elefakes = getWeightedHist('fe', InputFilename, hist2d_name, 0.0, sihihSelCut)
	#print 'ele fakes integral ',elefakes.Integral()
	#bckg_templ.Add(elefakes)
	#################################

	print 'new number of boundaries ',len(boundaries)
	pseudodataR = pseudodata.Rebin(len(boundaries)-1,pseudodata.GetName()+'rebin',boundaries)
	bckg_templR = bckg_templ.Rebin(len(boundaries)-1,bckg_templ.GetName()+'rebin',boundaries)
	sig_templR  = sig_templ.Rebin(len(boundaries)-1,sig_templ.GetName()+'rebin',boundaries)
	# to avoid signal going below fit range in the plot
	print 'sig_templR underflow ', sig_templR.GetBinContent(0)
	print 'setting to 0'
	sig_templR.SetBinContent(0,0)
	
	
	pseudodataU = makeUniformHist(pseudodataR)
	bckg_templU = makeUniformHist(bckg_templR)
	sig_templU  = makeUniformHist(sig_templR)

	print '#'*50

	# does not work well
	#makeFit(FitVarname,lowFitrange,highFitrange, sig_templR, bckg_templR, pseudodataR, 'fit_'+FitVarname+'.png')

	# do fit for fixed bin size histogram
	lowUFitRange = pseudodataR.FindBin(lowFitrange)
	if lowUFitRange == 0:
		print 'lower bin is underfow, setting to 1'
		lowUFitRange = 1
	highUFitRange = pseudodataR.FindBin(highFitrange) + 1
	if pseudodataR.GetBinLowEdge(highUFitRange-1) == highFitrange:
		print 'upper bin in on the border of fit range, reducing'
		highUFitRange -= 1

	print 'fitting in the bin range ',lowUFitRange, highUFitRange
	(fitSigFrac,fitSigFracErr) = makeFit(FitVarname+' bin number',lowUFitRange,highUFitRange, sig_templU, bckg_templU, pseudodataU, 'fitplots/fit_'+phoEtrange+FitVarname+'_uniform.png')

	# pseudo-experiments:
	pe_results = ROOT.TH1F('pe_results','Pseudo-experiments',100,0,1)
	pe_pull = ROOT.TH1F('pe_pull','Pseudo-experiments pull',80,-4,4)
	#pe_results = ROOT.TH1F('pe_results','Pseudo-experiments',50,0.4,0.9)
	for npi in xrange(NpseudoExp):
		print '-'*80
		print 'pe # ',npi
		pseudodataUrand = makeRandUniformHist(pseudodataR)
		bckg_templUrand = makeRandUniformHist(bckg_templR)
		sig_templUrand  = makeRandUniformHist(sig_templR)
		#bckg_templUrand = bckg_templU
		#sig_templUrand  = sig_templU
		(fitSigFracRand,fitSigFracErrRand) = makeFit(FitVarname+' bin number',lowUFitRange, highUFitRange, sig_templUrand, bckg_templUrand, pseudodataUrand, '')
		pe_results.Fill(fitSigFracRand)
		pe_pull.Fill( (fitSigFracRand - fitSigFrac)/fitSigFracErr )
		

	# draw the result
	ROOT.gStyle.SetOptFit(111)
	c1 = ROOT.TCanvas('c1','c1',800,800)
	pe_results.GetXaxis().SetTitle('signal fraction')
	pe_results.Draw()
	pe_results.Fit('gaus')
	pefit = pe_results.GetFunction('gaus')
	fitPEsigma = fitSigFracErr # start with fit error
	if NpseudoExp > 500:
		fitPEsigma = pefit.GetParameter(2)
		print 'sigma from fit',fitPEsigma

	if NpseudoExp > 0:
		c1.SaveAs('fitplots/pe_results.png')
		pe_pull.GetXaxis().SetTitle('signal fraction pull')
		pe_pull.Draw()
		pe_pull.Fit('gaus')
		c1.SaveAs('fitplots/pe_pull.png')

	ROOT.gStyle.SetOptStat(0)

	leg = ROOT.TLegend(0.6,0.7,0.99,0.94)
	leg.SetFillColor(0)

	# calculate signal fraction in selected regoin (iso < 5.0) ##########
	fitleftbinsig = sig_templ.FindBin(lowFitrange)
	fitrightbinsig = sig_templ.FindBin(highFitrange)
	print 'Signal Fit Range bins',fitleftbinsig,fitrightbinsig
	fitleftbinbckg = bckg_templ.FindBin(lowFitrange)
	fitrightbinbckg = bckg_templ.FindBin(highFitrange)
	print 'Background Fit Range bins',fitleftbinbckg,fitrightbinbckg

	selleftbinsig = sig_templ.FindBin(lowFitrange)
	selrightbinsig = sig_templ.FindBin(selectionRange)
	print 'Signal Nominal selection bins',selleftbinsig,selrightbinsig
	selleftbinbckg = bckg_templ.FindBin(lowFitrange)
	selrightbinbckg = bckg_templ.FindBin(selectionRange)
	print 'Background Nominal selection bins',selleftbinbckg,selrightbinbckg

	sig_templ.Scale(1.0/sig_templ.Integral(fitleftbinsig,fitrightbinsig))
	bckg_templ.Scale(1.0/bckg_templ.Integral(fitleftbinbckg,fitrightbinbckg))

	sig_templ_IntErr = ROOT.Double()
	sig_templ_Int = sig_templ.IntegralAndError(selleftbinsig,selrightbinsig,sig_templ_IntErr)
	bckg_templ_IntErr = ROOT.Double()
	bckg_templ_Int = bckg_templ.IntegralAndError(selleftbinbckg,selrightbinbckg,bckg_templ_IntErr)
	
	SFNomSel = 1.
	SFNomSelError = 1.
	
	print '#'*50
	print 'Signal fraction in Nominal selected region: ',(sig_templ_Int)/(sig_templ_Int + bckg_templ_Int*(1.0/fitSigFrac - 1))
	
	SFNomSel = 1. / (1. + bckg_templ_Int/sig_templ_Int*(1./fitSigFrac - 1) )
	# all relative uncertainties add in quadratures
	print 'relative error on signal fraction after PE fit: ',fitPEsigma/fitSigFrac
	Term1 = (1./fitSigFrac - 1)
	# relative error of the Term1
	relErrTerm1 = ((1./fitSigFrac)*fitPEsigma/fitSigFrac)/Term1
	#print 'relative error on Term1: ',relErrTerm1
	print 'relative error on sig. and bckg. integrals:',sig_templ_IntErr/sig_templ_Int,bckg_templ_IntErr/bckg_templ_Int
	Term2 = bckg_templ_Int/sig_templ_Int*(1./fitSigFrac - 1)
	relErrTerm2 = ((relErrTerm1)**2 + (sig_templ_IntErr/sig_templ_Int)**2 + (bckg_templ_IntErr/bckg_templ_Int)**2)**0.5
	absErrTerm2 = Term2*relErrTerm2
	# total relative error, same as relative error of denominator
	# absolute error of denominator same as absErrTerm2
	# relative error of denominator:
	relErrDenom = absErrTerm2 / ( 1. + Term2 )
	SFNomSelError = SFNomSel * relErrDenom
	print 'Final Signal Fraction value with error: ', SFNomSel, ' +-',SFNomSelError
	print '#'*50

	#######################################################################

	leftbin = lowUFitRange
	rightbin = highUFitRange - 1

	print 'bins for normalization ',leftbin,rightbin
	bckg_templR.Scale((1.0-fitSigFrac)*pseudodataR.Integral(leftbin,rightbin)/bckg_templR.Integral(leftbin,rightbin))
	sig_templR.Scale(fitSigFrac*pseudodataR.Integral(leftbin,rightbin)/sig_templR.Integral(leftbin,rightbin))

	sig_templR.SetFillColor(ROOT.kGreen)
	bckg_templR.SetFillColor(ROOT.kBlue)
	sig_templR.SetLineColor(ROOT.kGreen)
	bckg_templR.SetLineColor(ROOT.kBlue)
	sig_templR.GetXaxis().SetRangeUser(lowFitrange,highFitrange)
	bckg_templR.GetXaxis().SetRangeUser(lowFitrange,highFitrange)

	stack = ROOT.THStack(FitVarname+'_stack',FitVarname+'_stack')
	stack.Add(bckg_templR)
	stack.Add(sig_templR)
	stack.SetTitle('')
	stack.Draw('hist')
	stack.GetXaxis().SetTitle('photon '+FitVarname+' (GeV)')
	stack.SetMaximum(1.2*stack.GetMaximum())
	stack.GetXaxis().SetRangeUser(lowFitrange,highFitrange)

	if fitData:
		leg.AddEntry(pseudodataR, 'Data', 'lfp')
	else: 
		leg.AddEntry(pseudodataR, 'Pseudo Data', 'lfp')
	leg.AddEntry(sig_templR, 'Signal', 'lf')
	leg.AddEntry(bckg_templR, 'Background', 'lf')
	leg.Draw()
	pseudodataR.SetMarkerStyle(8)
	pseudodataR.SetLineColor(1)
	pseudodataR.Draw('esame')
	c1.SaveAs('fitplots/plot_'+phoEtrange+FitVarname+'.png')

	if fitData:
		print 'Fitting of Data is done'
		return (SFNomSel, SFNomSelError, -1.0)


	leg.Clear()

	## compare template shapes here

	# signal template: compare MC truth photon isolation with random cone isolation
	trueSignalIso = getWeightedHist('rs', InputFilename, hist2d_name, 0.0, sihihSelCut)
	trueSignalIso.Add(getWeightedHist('fe', InputFilename, hist2d_name, 0.0, sihihSelCut))
	trueSignalIso.Rebin(2)
	trueSignalIso.GetXaxis().SetRangeUser(lowFitrange,highFitrange)
	trueSignalIso.Scale(1.0/trueSignalIso.Integral())
	trueSignalIso.SetLineColor(1)

	randCone_Iso = getWeightedHist('', InputFilename, hist_sig_templ_name)
	randCone_Iso.GetXaxis().SetRangeUser(lowFitrange,highFitrange)
	randCone_Iso.Scale(1.0/randCone_Iso.Integral())
	randCone_Iso.SetLineColor(2)

	leg.AddEntry(trueSignalIso, 'MC truth signal','lf')
	leg.AddEntry(randCone_Iso, 'Random cone', 'lf')
	randCone_Iso.SetTitle('')
	randCone_Iso.GetXaxis().SetTitle('photon '+FitVarname+' (GeV)')
	randCone_Iso.Draw()
	trueSignalIso.Draw('same')
	leg.Draw()
	c1.SaveAs('fitplots/'+hist_sig_name+'_sig'+phoEtrange+'templ.png')
	c1.SetLogy(1)
	c1.SaveAs('fitplots/'+hist_sig_name+'_sig'+phoEtrange+'templ_log.png')
	c1.SetLogy(0)
	leg.Clear()

	# background template comparison:
	# pseudodata sideband
	# experiment
	#sbIso = getWeightedHist('', ZeroBFilename, hist2d_name, sbLeft, sbRight)
	sbIso = getWeightedHist('', InputFilename, hist2d_name, sbLeft, sbRight)
	sbIso.Rebin(2)
	# MC truth signal iso in side-band
	sbIsoMCtrue = getWeightedHist('rs', InputFilename, hist2d_name, sbLeft, sbRight)
	sbIsoMCtrue.Add(getWeightedHist('fe', InputFilename, hist2d_name, sbLeft, sbRight))
	sbIsoMCtrue.Rebin(2)
	# calculate true signal fraction in side-band
	print 'Side-band used: ',sbLeft,sbRight
	print 'Fit range considered: ',lowFitrange, highFitrange
	leftbin = sbIso.FindBin(lowFitrange)
	rightbin = sbIso.FindBin(highFitrange)
	print 'Fraction of MC truth signal in the side-band with respect to pseudodata: ',\
		sbIsoMCtrue.Integral(leftbin,rightbin)/sbIso.Integral(leftbin,rightbin)

	sbIso.Scale(1.0/sbIso.Integral())
	sbIso.SetLineColor(2)

	# MC truth background (fjrb) shape
	true_bckg = getWeightedHist('fjrb', InputFilename, hist2d_name, 0.0, sihihSelCut)
	true_bckg.Rebin(2)
	true_bckg.Scale(1.0/true_bckg.Integral())
	true_bckg.SetLineColor(1)

	#true_sel_bckg = getWeightedHist('fjrb', InputFilename, hist_sig_name)
	#true_sel_bckg.Scale(1.0/true_sel_bckg.Integral())
	#true_sel_bckg.SetLineColor(3)

	leg.AddEntry(true_bckg,'MC truth bckg','lf')
	leg.AddEntry(sbIso,'#sigma_{i#etai#eta} side band', 'lf')
	#leg.AddEntry(true_sel_bckg,'MC truth backg, nom. selection', 'lf')

	#true_sel_bckg.Draw()
	true_bckg.SetTitle('')
	true_bckg.GetXaxis().SetTitle('photon '+FitVarname+' (GeV)')
	true_bckg.Draw()
	sbIso.Draw('same')
	leg.Draw()
	c1.SaveAs('fitplots/'+hist_sig_name+phoEtrange+'_bckg.png')
	c1.SetLogy(1)
	c1.SaveAs('fitplots/'+hist_sig_name+phoEtrange+'_bckg_log.png')
	c1.SetLogy(0)

	true_bckg.GetXaxis().SetRangeUser(lowFitrange,highFitrange)
	true_bckg.Scale(1.0/true_bckg.Integral())
	sbIso.GetXaxis().SetRangeUser(lowFitrange,highFitrange)
	sbIso.Scale(1.0/sbIso.Integral())
	#true_sel_bckg.GetXaxis().SetRangeUser(lowFitrange,highFitrange)
	#true_sel_bckg.Scale(1.0/true_sel_bckg.Integral())

	#true_sel_bckg.Draw()
	true_bckg.Draw()
	sbIso.Draw('same')
	leg.Draw()
	c1.SaveAs('fitplots/'+hist_sig_name+phoEtrange+'_bckg_fitrange.png')
	c1.SetLogy(1)
	c1.SaveAs('fitplots/'+hist_sig_name+phoEtrange+'_bckg_fitrange_log.png')
	c1.SetLogy(0)

	leg.Clear()


	# find MC truth signal fraction in nominal selection #############################################################################
	# extract "rs" and "fe" parts, divide by "photon1ChHadSCRIso" sum
	totalSigInt = getWeightedHist('', InputFilename, hist_sig_name).Integral()
	trueSignalInt = getWeightedHist('rs', InputFilename, hist_sig_name).Integral() + getWeightedHist('fe', InputFilename, hist_sig_name).Integral()
	#print 'MC truth signal integral',trueSignalInt
	print 'MC truth signal fraction afetr Nominal selection is ', trueSignalInt/totalSigInt
	print 'MC truth signal fraction if SCR iso in fit range used as selection: ',MCtrueSelSignalFraction
	return (SFNomSel, SFNomSelError, trueSignalInt/totalSigInt)
