import ROOT

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


# calculate average photon and electron fractions for 2 cases:
# ttbar+photon
# bg+photon
# 
# get photon and electron fractions from 'templates_barrel.root' (non-scaled)
# re-weight fractions according to sample contribution after M3 fit and including QCD

def getInt_Err(hist):
	err = ROOT.Double(0.0)
	integr = hist.IntegralAndError(0,hist.GetNbinsX() + 1, err)
	return (integr,err)


def addEle_Pho_contributions(sample, all, fake, ele, pho):
	fileName = 'templates_barrel_scaled.root'
	
	allHist = get1DHist(fileName, sample+'_MET')
	fakeHist = get1DHist(fileName, sample+'_fake_MET')
	eleHist = get1DHist(fileName, sample+'_electron_MET')
	phoHist = get1DHist(fileName, sample+'_signal_MET')
	
	allInt,allErr = getInt_Err(allHist)
	fakeInt,fakeErr = getInt_Err(fakeHist)
	eleInt,eleErr = getInt_Err(eleHist)
	phoInt,phoErr = getInt_Err(phoHist)
	
	if allInt <  0.0001:
		return all, ele, pho
	
	newall = (all[0] + allInt, ( (all[1])**2 + allErr**2 )**0.5 )
	
	print 'sample, all, fake, ele, pho : ',sample, allInt,'+-', allErr, '  ', fakeInt,'+-',fakeErr,'  ', eleInt,'+-', eleErr, '  ', phoInt,'+-', phoErr
	newfake = (fake[0] + fakeInt, ((fake[1])**2 + (fakeErr)**2 )**0.5 )
	newele = (ele[0] + eleInt, ( (ele[1])**2 + (eleErr)**2 )**0.5 )
	newpho = (pho[0] + phoInt, ( (pho[1])**2 + (phoErr)**2 )**0.5 )
	
	return (newall, newfake, newele, newpho)



ttbar_all = (0.0, 0.0)
ttbar_fake = (0.0, 0.0)
ttbar_ele = (0.0, 0.0)
ttbar_pho = (0.0, 0.0)

bg_all = (0.0, 0.0)
bg_fake = (0.0, 0.0)
bg_ele = (0.0, 0.0)
bg_pho = (0.0, 0.0)

ttbar_all, ttbar_fake, ttbar_ele, ttbar_pho = addEle_Pho_contributions('TTJets', ttbar_all, ttbar_fake, ttbar_ele, ttbar_pho)
ttbar_all, ttbar_fake, ttbar_ele, ttbar_pho = addEle_Pho_contributions('TTGamma', ttbar_all, ttbar_fake, ttbar_ele, ttbar_pho)

bg_all, bg_fake, bg_ele, bg_pho = addEle_Pho_contributions('WJets', bg_all, bg_fake, bg_ele, bg_pho)
bg_all, bg_fake, bg_ele, bg_pho = addEle_Pho_contributions('ZJets', bg_all, bg_fake, bg_ele, bg_pho)
bg_all, bg_fake, bg_ele, bg_pho = addEle_Pho_contributions('Vgamma', bg_all, bg_fake, bg_ele, bg_pho)
bg_all, bg_fake, bg_ele, bg_pho = addEle_Pho_contributions('SingleTop', bg_all, bg_fake, bg_ele, bg_pho)
qcdInt,qcdErr = getInt_Err(get1DHist('templates_barrel_scaled.root', 'QCD_MET'))
print 'QCD total: ',qcdInt,qcdErr
bg_all = (bg_all[0] + qcdInt, ((bg_all[1])**2 + qcdErr**2)**0.5 )

print 'ttbar all, ele, pho ',ttbar_all, ttbar_ele, ttbar_pho
print 'bg all, ele, pho ',bg_all, bg_ele, bg_pho
print
print 'ttbar ele and pho fractions',ttbar_ele[0]/ttbar_all[0], '  ', ttbar_pho[0]/ttbar_all[0]
print 'bg ele and pho fractions',bg_ele[0]/bg_all[0], '  ', bg_pho[0]/bg_all[0]

