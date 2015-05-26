#! /usr/bin/env python
from ROOT import *
from ROOT import RooFit
import sys
import os
import math
import re

def makeFit(varname, varmin, varmax, signalHist, backgroundHist, dataHist, plotName):
        # RooFit variables
        sihihVar = RooRealVar(varname, varname, varmin, varmax)
        sihihArgList = RooArgList()
        sihihArgList.add(sihihVar)
        sihihArgSet = RooArgSet()
        sihihArgSet.add(sihihVar)

        # create PDFs
        signalDataHist = RooDataHist('signalDataHist','signal RooDataHist', sihihArgList, signalHist)
        signalPdf = RooHistPdf('signalPdf',varname+' of signal', sihihArgSet, signalDataHist)

        backgroundDataHist = RooDataHist('backgroundDataHist','background RooDataHist', sihihArgList, backgroundHist)
        backgroundPdf = RooHistPdf('backgroundPdf',varname+' of background', sihihArgSet, backgroundDataHist)



        # data
        dataDataHist = RooDataHist('data '+varname, varname+' in Data', sihihArgList, dataHist)

        # signal fraction parameter
        sfname = 'signal fraction'
        if 'MET' in varname:
                sfname = 'multijet fraction'
        if 'M3' in varname:
                sfname = 'ttbar fraction'
        signalFractionVar = RooRealVar(sfname,sfname, 0.5, 0.0, 1.0)
        sumPdf = RooAddPdf('totalPdf','signal+background', signalPdf, backgroundPdf, signalFractionVar)

        # fit
        sumPdf.fitTo( dataDataHist, RooFit.SumW2Error(ROOT.kFALSE),RooFit.PrintLevel(-1) )

        if plotName!='':
        	  # plot results
                c1 = TCanvas('c1', 'c1', 800, 600)
                plotter = RooPlot('myplot','',sihihVar,varmin,varmax,20) # nBins is dummy
                dataDataHist.plotOn(plotter, RooFit.Name('data'))
                sumPdf.plotOn(plotter, RooFit.Name('sum'), RooFit.LineColor(kRed))
                sumPdf.plotOn(plotter, RooFit.Components('signalPdf'), RooFit.Name('signal'),
                        RooFit.LineColor(kGreen))
                sumPdf.plotOn(plotter, RooFit.Components('backgroundPdf'), RooFit.Name('background'),
                        RooFit.LineColor(kBlue))
                sumPdf.paramOn(plotter) # fix

                plotter.Draw()
                plotter.GetYaxis().SetTitleOffset(1.4)
                c1.SaveAs(plotName)
        print 'fit returned value ',signalFractionVar.getVal(),' +- ',signalFractionVar.getError()
        return (signalFractionVar.getVal(),signalFractionVar.getError())


def makenewFit(varname, varmin, varmax, signalHist, backgroundHist, qcdHist, dataHist, plotName):
        # RooFit variables
        sihihVar = RooRealVar(varname, varname, varmin, varmax)
        sihihArgList = RooArgList()
        sihihArgList.add(sihihVar)
        sihihArgSet = RooArgSet()
        sihihArgSet.add(sihihVar)

        # create PDFs
        signalDataHist = RooDataHist('signalDataHist','signal RooDataHist', sihihArgList, signalHist)
        signalPdf = RooHistPdf('signalPdf',varname+' of signal', sihihArgSet, signalDataHist)

        backgroundDataHist = RooDataHist('backgroundDataHist','background RooDataHist', sihihArgList, backgroundHist)
        bkgPdf = RooHistPdf('backgroundPdf',varname+' of background', sihihArgSet, backgroundDataHist)
                                                                                                                                     73,1          15%
	qcdDataHist = RooDataHist('qcdDataHist','qcd RooDataHist', sihihArgList, qcdHist)
        qcdPdf = RooHistPdf('qcdPdf',varname+' of qcd', sihihArgSet, qcdDataHist)



        # data
        dataDataHist = RooDataHist('data '+varname, varname+' in Data', sihihArgList, dataHist)

        # signal fraction parameter
        sfname = 'signal fraction'
        if 'MET' in varname:
                sfname = 'multijet fraction'
        if 'M3' in varname:
                sfname = 'ttbar fraction'
                qcdfname = ' qcd fraction'
                bkgfname = 'background fraction'

        signalFractionVar = RooRealVar(sfname,sfname, 0.5, 0., 1.)
        bkgFractionVar = RooRealVar(bkgfname,bkgfname, 0.5, 0., 1.)
        qcdFractionVar = RooRealVar(qcdfname,qcdfname, 0.5,0.,1.)
        listPdfs = RooArgList(signalPdf,\
                                   qcdPdf,\
                                   bkgPdf)
        listcoeff = RooArgList(signalFractionVar,\
                                  qcdFractionVar,\
                                  bkgFractionVar)


        #qcdFractionVar.setConstant(True) #making the fraction variable for qcd constant
        #backgroundFractionVar.setConstant(True) 
        qcd = qcdHist.Integral(-1,-1)
        bkg = backgroundHist.Integral(-1,-1)

        sumPdf = RooAddPdf('totalPdf','signal+background+qcd', listPdfs, listcoeff)
        qcdFractionVar.setVal(qcd)
        #bkgFractionVar.setVal(bkg)
        qcdFractionVar.setConstant(True)
        #bkgFractionVar.setConstant(True) 

	      sumPdf.fitTo( dataDataHist, RooFit.SumW2Error(kFALSE), RooFit.PrintLevel(-1) )

        if plotName!='':
                # plot results
                c1 = TCanvas('c1', 'c1', 800, 600)
                plotter = RooPlot('myplot','',sihihVar,varmin,varmax,20) # nBins is dummy
                dataDataHist.plotOn(plotter, RooFit.Name('data'))
                sumPdf.plotOn(plotter, RooFit.Name('sum'), RooFit.LineColor(kRed))
                sumPdf.plotOn(plotter, RooFit.Components('signalPdf'), RooFit.Name('signal'),
                    RooFit.LineColor(kGreen))
                sumPdf.plotOn(plotter, RooFit.Components('backgroundPdf'), RooFit.Name('background'),
                    RooFit.LineColor(kBlue))
                sumPdf.plotOn(plotter, RooFit.Components('qcdPdf'), RooFit.Name('qcd'),
                    RooFit.LineColor(kYellow))

                sumPdf.paramOn(plotter) # fix

                plotter.Draw()
                plotter.GetYaxis().SetTitleOffset(1.4)
                c1.SaveAs(plotName)
        print 'fit returned value ',signalFractionVar.getVal(),' +- ',signalFractionVar.getError()
        return (signalFractionVar.getVal(),signalFractionVar.getError())




openfiles = {}

def get1DHist(filename, histname):
        if filename not in openfiles:
                openfiles[filename] = TFile(filename,'READ')
        file = openfiles[filename]
           hist = file.Get(histname)
        hist.SetDirectory(0)
        hist.SetFillColor(0)
        #hist.Sumw2()
        return hist

qcdMETfile = 'templates_presel_nomet_qcd.root'
normMETfile = 'templates_presel_nomet.root'

M3file = 'templates_presel.root'

M3file_photon = 'templates_barrel_scaled.root'
M3file_presel_scaled = 'templates_presel_scaled.root'

def doQCDfit():
        varToFit = 'MET'

        qcdDataHist = get1DHist(qcdMETfile, 'Data_'+varToFit)
        # remove MC contribution
        qcdDataHist.Add(get1DHist(qcdMETfile, 'TTJets_'+varToFit), -1)
        qcdDataHist.Add(get1DHist(qcdMETfile, 'WJets_'+varToFit), -1)
        qcdDataHist.Add(get1DHist(qcdMETfile, 'SingleTop_'+varToFit), -1)

        DataHist = get1DHist(normMETfile, 'Data_'+varToFit)

        MCHist = get1DHist(normMETfile, 'TTJets_'+varToFit)
        MCHist.Add(get1DHist(normMETfile, 'TTGamma_'+varToFit))
        MCHist.Add(get1DHist(normMETfile, 'WJets_'+varToFit))
        MCHist.Add(get1DHist(normMETfile, 'ZJets_'+varToFit))
        MCHist.Add(get1DHist(normMETfile, 'SingleTop_'+varToFit))
                                                                                                                                                                                                          106,1         49%
	  (metFrac, metFracErr) = makeFit(varToFit, 0., 300.0, qcdDataHist, MCHist, DataHist, varToFit+'_QCD_fit.png')
        # recalculate data-driven QCD normalization
        lowbin = 1   #DataHist.FindBin(20.01)
        highbin = DataHist.GetNbinsX()+1 # overflow bin included
        metFracwithcut = 0.0350778569386
        print 'Will calculate integral in the bin range:', lowbin, highbin
        dataInt = DataHist.Integral(lowbin, highbin)
        dataIntwithMETcut = DataHist.Integral(3,highbin)
        print 'Integral of Data total: ', dataInt
        qcdInt = qcdDataHist.Integral(lowbin, highbin)
        mcInt = MCHist.Integral(lowbin, highbin)
        print 'Integral of data-driven QCD in the desired range: ', qcdInt
        print '#'*80
        # take into account only fit error
        # stat errors on histograms are treated while calculating the final answer
        print 'the met fraction:', metFrac
        print 'the met fraction with met cuts:', metFracwithcut
        print 'the amount of Data with MET cut:' ,dataIntwithMETcut
        QCDsignal = metFracwithcut*dataIntwithMETcut
        QCDamount = metFrac*dataInt
        print 'Total Amount of QCD without MET cut:',QCDamount
        print 'Amount of QCD in signal :' ,QCDsignal
        QCDSF = metFrac*dataInt/qcdInt
        QCDSFerror = metFracErr*dataInt/qcdInt
        print 'Scale factor for QCD in nominal MET range: ', QCDSF,' +-',QCDSFerror,'(fit error only)'
        print 'Correction to all MC scale factors: ', (1-metFrac)*dataInt/mcInt, ' +-',metFracErr*dataInt/mcInt,'(fit error only)'
        print '#'*80
        return (QCDSF, QCDSFerror)



def doM3fit():
           print 'now do M3 fit'

        varToFit = 'M3'

        DataHist = get1DHist(M3file, 'Data_'+varToFit)

        TopHist = get1DHist(M3file, 'TTJets_'+varToFit)
        TopHist.Add(get1DHist(M3file, 'TTGamma_'+varToFit))



        WJHist = get1DHist(M3file, 'WJets_'+varToFit)

        # remove other suspects from data
        DataHist.Add(get1DHist(M3file, 'ZJets_'+varToFit), -1.0)
        DataHist.Add(get1DHist(M3file, 'SingleTop_'+varToFit), -1.0)
        DataHist.Add(get1DHist(M3file, 'Vgamma_'+varToFit), -1.0)

        QCDHist = get1DHist(M3file_presel_scaled, 'QCD_'+varToFit)

        (m3TopFrac, m3TopFracErr) = makenewFit(varToFit+'(GeV)', 40.0, 660.0, TopHist, WJHist, QCDHist, DataHist, varToFit+'_fit.png')
        lowfitBin = DataHist.FindBin(40.01)
        highfitBin = DataHist.FindBin(659.99)

        dataInt = DataHist.Integral(lowfitBin,highfitBin)
        topInt = TopHist.Integral(lowfitBin,highfitBin)
        WJInt = WJHist.Integral(lowfitBin,highfitBin)
        num_top = TopHist.Integral(-1,1)
         num_wjet = WJHist.Integral(-1,1)
        num_qcd = QCDHist.Integral(-1,1)


        QCDInt = QCDHist.Integral(lowfitBin,highfitBin)
        TopSF = m3TopFrac * dataInt / topInt
        TopSFerror = m3TopFracErr * dataInt / topInt
        print '#'*80
        print 'Correction to the Top scale factor: ', TopSF, ' +-', TopSFerror, '(fit error only)'
        WJetsSF = (1.0-m3TopFrac) * dataInt / WJInt
        WJetsSFerror = m3TopFracErr * dataInt / WJInt
        print 'Correction to WJets scale factor: ', WJetsSF, ' +-',WJetsSFerror,'(fit error only)'
        print '#'*80
        return (TopSF, TopSFerror, WJetsSF, WJetsSFerror)

                                                                                                                                     253,0-1       Bot
                                                                                                                   210,1         79%

                                                           
