#include"Selector.h"


double dR(double eta1, double phi1, double eta2, double phi2){
	double dphi = phi2 - phi1;
	double deta = eta2 - eta1;
	static const double pi = TMath::Pi();
	dphi = TMath::Abs( TMath::Abs(dphi) - pi ) - pi;
	return TMath::Sqrt( dphi*dphi + deta*deta );
}

Selector::Selector(){
	// jets
	jet_Pt_cut = 30;
	btag_cut = 0.679;

	// electrons
	ele_Pt_cut = 35.0;
	ele_PtLoose_cut = 20.0;
	ele_RelIso_range[0] = 0.0;
	ele_RelIso_range[1] = 0.1;
	ele_RelIsoLoose_cut = 0.2;
	ele_MVA_range[0] = 0.9;
	ele_MVA_range[1] = 1.0;
	ele_MVALoose_cut = 0.0;
	ele_Dxy_cut = 0.02;
	ele_MissInnHit_cut = 0;
	ele_Iso_MVA_invert = false;

	// photons
	pho_Et_cut = 25.0; 
	pho_ID_ind = 0; // 0 - Loose, 1 - Medium, 2 - Tight
	pho_noPixelSeed_cut = false;
	pho_noEleVeto_cut = false;
	
	// muons
	mu_PtLoose_cut = 10.0;
	mu_RelIsoLoose_cut = 0.2;
        mu_RelIso_range[0] = 0.0;
        mu_RelIso_range[1] = 0.12;
	mu_Iso_MVA_invert = false;
}

void Selector::process_objects(const EventTree* inp_tree){
	tree = inp_tree;
	clear_vectors();
	filter_photons();
	filter_electrons();
	filter_muons();
	filter_jets();
}

void Selector::clear_vectors(){
	PhotonsPresel.clear();
	PhoPassChHadIso.clear();
	PhoPassPhoIso.clear();
	PhoPassSih.clear();
	
	Electrons.clear();
	ElectronsLoose.clear();
	Muons.clear();
	MuonsLoose.clear();
	Jets.clear();
	bJets.clear();
	
	Ele03RelIso.clear();
	Mu04RelIso.clear();
	Pho03ChHadIso.clear();
	Pho03ChHadSCRIso.clear();
	Pho03NeuHadIso.clear();
	Pho03PhoIso.clear();
	Pho03PhoSCRIso.clear();
	Pho03RandPhoIso.clear();
	Pho03RandChHadIso.clear();
}

void Selector::filter_photons(){
	for(int phoInd = 0; phoInd < tree->nPho_; ++phoInd){
		double eta = tree->phoEta_->at(phoInd);
		double et = tree->phoEt_->at(phoInd);

		Pho03ChHadIso.push_back(    tree->phoPFChIso_->at(phoInd)   - tree->rho2012_ * phoEffArea03ChHad(eta) );
		Pho03ChHadSCRIso.push_back( tree->phoSCRChIso_->at(phoInd)  - tree->rho2012_ * phoEffArea03ChHad(eta) );
		Pho03RandChHadIso.push_back(tree->phoRandConeChIso_->at(phoInd) - tree->rho2012_ * phoEffArea03ChHad(eta) );
		
		Pho03NeuHadIso.push_back(   tree->phoPFNeuIso_->at(phoInd) - tree->rho2012_ * phoEffArea03NeuHad(eta) );
		
		Pho03PhoIso.push_back(      tree->phoPFPhoIso_->at(phoInd)  - tree->rho2012_ * phoEffArea03Pho(eta) );
		Pho03PhoSCRIso.push_back(   tree->phoSCRPhoIso_->at(phoInd) - tree->rho2012_ * phoEffArea03Pho(eta) );
		Pho03RandPhoIso.push_back(  tree->phoRandConePhoIso_->at(phoInd) - tree->rho2012_ * phoEffArea03Pho(eta) );
		
		// manual spike cleaning (was necessary before)
		//if (dR(tree->phoEta_->at(phoInd), tree->phoPhi_->at(phoInd), -1.76, 1.37) < 0.05) continue;
		//if (dR(tree->phoEta_->at(phoInd), tree->phoPhi_->at(phoInd),  2.37, 2.69) < 0.05) continue;		

		int region = 0; //barrel
		if(TMath::Abs( eta )>1.5) region = 1; //endcap
		bool phoPresel = fidEtaPass( eta ) &&
						et > pho_Et_cut &&
						( pho_noPixelSeed_cut || tree->phohasPixelSeed_->at(phoInd) == 0 ) &&
						( pho_noEleVeto_cut || tree->phoEleVeto_->at(phoInd) == 0 ) &&
						tree->phoIsConv_->at(phoInd) == photonID_IsConv[region][pho_ID_ind] &&
						tree->phoHoverE_->at(phoInd) < photonID_HoverE[region][pho_ID_ind] &&
						Pho03NeuHadIso[phoInd] < 
			(photonID_RhoCorrR03NeuHadIso_0[region][pho_ID_ind] + et * photonID_RhoCorrR03NeuHadIso_1[region][pho_ID_ind]);
		
		if(phoPresel){
			PhotonsPresel.push_back(phoInd);
			PhoPassSih.push_back( tree->phoSigmaIEtaIEta_->at(phoInd) < photonID_SigmaIEtaIEta[region][pho_ID_ind] );
			// substitute ChHadIso cut to loose SC footprint removed ChHadIso cut of 5 GeV in photon selection
			PhoPassChHadIso.push_back( Pho03ChHadSCRIso[phoInd] < 5 /*photonID_RhoCorrR03ChHadIso[region][pho_ID_ind]*/ );
			PhoPassPhoIso.push_back( Pho03PhoIso[phoInd] < photonID_RhoCorrR03PhoIso_0[region][pho_ID_ind] + et * photonID_RhoCorrR03PhoIso_1[region][pho_ID_ind] );
		}
	}
}

void Selector::filter_electrons(){
	for(int eleInd = 0; eleInd < tree->nEle_; ++eleInd){
		double eta = tree->eleSCEta_->at(eleInd);
		double pt = tree->elePt_->at(eleInd);
		double rho_zero = std::max(0.0, (double)tree->rho2012_);
		Ele03RelIso.push_back( 
			(tree->elePFChIso03_->at(eleInd) + 
			 std::max(0.0, tree->elePFNeuIso03_->at(eleInd) + tree->elePFPhoIso03_->at(eleInd) - rho_zero * eleEffArea03(eta))
			) / pt );
		
		bool Iso_pass = ele_RelIso_range[0] <= Ele03RelIso[eleInd] &&
				Ele03RelIso[eleInd] < ele_RelIso_range[1];
		bool MVA_pass = ele_MVA_range[0] < tree->eleIDMVATrig_->at(eleInd) &&
				tree->eleIDMVATrig_->at(eleInd) <= ele_MVA_range[1];
		bool Iso_MVA_pass;
		if(ele_Iso_MVA_invert) Iso_MVA_pass = !Iso_pass || !MVA_pass;
		else Iso_MVA_pass = Iso_pass && MVA_pass;
		bool eleSel = fidEtaPass( eta ) &&
						pt > ele_Pt_cut &&
						Iso_MVA_pass &&
						tree->eleConvVtxFit_->at(eleInd) == 0 &&
						TMath::Abs(tree->eleD0_->at(eleInd)) < ele_Dxy_cut &&
						tree->eleMissHits_->at(eleInd) <= ele_MissInnHit_cut;
		
		bool looseSel = fabs(eta) < 2.5 && 
						pt > ele_PtLoose_cut && 
						Ele03RelIso[eleInd] < ele_RelIsoLoose_cut && 
						tree->eleIDMVATrig_->at(eleInd) > ele_MVALoose_cut;
		
		if( eleSel ){
			Electrons.push_back(eleInd);
		}
		else if( looseSel ){ 
			ElectronsLoose.push_back(eleInd);
		}
	}
}

void Selector::filter_muons(){
	for(int muInd = 0; muInd < tree->nMu_; ++muInd){
		const unsigned int GlobalMuon     =  1<<1;
		const unsigned int TrackerMuon    =  1<<2;
		const unsigned int PFMuon =  1<<5;
		bool isGlobalMuon  = tree->muType_->at(muInd) & GlobalMuon;
		bool isTrackerMuon = tree->muType_->at(muInd) & TrackerMuon;
		bool isPFMuon      = tree->muType_->at(muInd) & PFMuon;
		double eta = tree->muEta_->at(muInd);
		double pt = tree->muPt_->at(muInd);
		double frelIsocorr = ( tree->muPFIsoR04_CH_->at(muInd) + 
					fmax(0.0, tree->muPFIsoR04_NH_->at(muInd) + 
						tree->muPFIsoR04_Pho_->at(muInd) -
						0.5*tree->muPFIsoR04_PU_->at(muInd)
					) 
				     ) / pt;
	//	bool Iso_pass = mu_RelIso_range[0] <= Mu04RelIso[muInd] &&
         //                       Mu04RelIso[muInd] < mu_RelIso_range[1];

		double rho_zero = std::max(0.0, (double)tree->rho2012_);
		//Mu04RelIso.push_back( 
		//	(tree->muPFIsoR04_CH_->at(muInd) +
		//	 std::max(0.0, tree->muPFIsoR04_NH_->at(muInd) + tree->muPFIsoR04_Pho_->at(muInd) - rho_zero * muEffArea04(eta))
		//	) / pt );
		Mu04RelIso.push_back( frelIsocorr );
		// fill Muons vector with indices of muons passing selection
		bool passLoose = pt > 10.0 && TMath::Abs(eta) < 2.5 && frelIsocorr < 0.2 && isPFMuon && ( isGlobalMuon || isTrackerMuon);
		bool passTight = pt > 26.0 && TMath::Abs(eta) < 2.1 && 
				tree->muChi2NDF_->at(muInd) < 10 &&
				tree->muNumberOfValidTrkLayers_->at(muInd) > 5 &&
				tree->muNumberOfValidMuonHits_->at(muInd) > 0 &&
				tree->muD0_->at(muInd) < 0.2 &&
				fabs( tree->muDz_->at(muInd) ) < 0.5 && //check this
				tree->muNumberOfValidPixelHits_->at(muInd) > 0 &&
				tree->muStations_->at(muInd) > 1 &&
				frelIsocorr >= mu_RelIso_range[0] && frelIsocorr <= mu_RelIso_range[1] &&
				isPFMuon && isGlobalMuon && isTrackerMuon;
		
		//bool muSel = TMath::Abs(eta) < 2.5 &&
		//				pt > mu_PtLoose_cut &&
		//				Mu04RelIso[muInd] < mu_RelIsoLoose_cut;
		if( passTight && passLoose ){
			Muons.push_back(muInd);
		}
		if ( passTight && !passLoose){
			Muons.push_back(muInd);
		}
		if( passLoose && !passTight ){
			MuonsLoose.push_back(muInd);
		}
	}
}

// jet ID is not likely to be altered, so it is hardcoded
void Selector::filter_jets(){
	for(int jetInd = 0; jetInd < tree->nJet_; ++jetInd){
		bool jetPresel = TMath::Abs(tree->jetEta_->at(jetInd)) < 2.4 &&
						tree->jetCHF_->at(jetInd) > 0 &&
						tree->jetNHF_->at(jetInd) < 0.99 &&
						tree->jetCEF_->at(jetInd) < 0.99 &&
						tree->jetNEF_->at(jetInd) < 0.99 &&
						tree->jetNCharged_->at(jetInd) > 0 &&
						tree->jetNConstituents_->at(jetInd) > 1;
		
		if( jetPresel && tree->jetPt_->at(jetInd) > jet_Pt_cut){
			Jets.push_back(jetInd);
			if(tree->jetCombinedSecondaryVtxBJetTags_->at(jetInd) > btag_cut) bJets.push_back(jetInd);
		}
	}
}

bool Selector::fidEtaPass(double Eta){
	double fabsEta = TMath::Abs(Eta);
	if( fabsEta > 2.5) return false;
	if( 1.4442 < fabsEta && fabsEta < 1.566) return false;
	return true;
}

// kEleGammaAndNeutralHadronIso03
// http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h
double Selector::eleEffArea03(double SCEta){
	double eta = TMath::Abs(SCEta);
	static const double area[7] = {0.130, 0.137, 0.067, 0.089, 0.107, 0.110, 0.138};
	int region = 0;
	if( eta >= 1.0 )   region++;
	if( eta >= 1.479 ) region++;
	if( eta >= 2.0 )   region++;
	if( eta >= 2.2 )   region++;
	if( eta >= 2.3 )   region++;
	if( eta >= 2.4 )   region++;
	return area[region];
}

// kMuGammaAndNeutralHadronIso04
// http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/sixie/Muon/MuonAnalysisTools/interface/MuonEffectiveArea.h?revision=1.7&view=markup
double Selector::muEffArea04(double muEta){
	double eta = TMath::Abs(muEta);
	static const double area[6] = {0.674, 0.565, 0.442, 0.515, 0.821, 0.660};
	int region = 0;
	if( eta >= 1.0 )   region++;
	if( eta >= 1.479 ) region++;
	if( eta >= 2.0 )   region++;
	if( eta >= 2.2 )   region++;
	if( eta >= 2.3 )   region++;
	return area[region];
}

// https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012#Effective_Areas_for_rho_correcti
int Selector::phoRegion(double absEta){
	int region = 0;
	if( absEta >= 1.0  ) region++;
	if( absEta >= 1.479) region++;
	if( absEta >= 2.0  ) region++;
	if( absEta >= 2.2  ) region++;
	if( absEta >= 2.3  ) region++;
	if( absEta >= 2.4  ) region++;
	return region;
}
double Selector::phoEffArea03ChHad(double phoEta){
	double eta = TMath::Abs(phoEta);
	static const double area[7] = {0.012, 0.010, 0.014, 0.012, 0.016, 0.020, 0.012};
	return area[phoRegion(eta)];
}
double Selector::phoEffArea03NeuHad(double phoEta){
	double eta = TMath::Abs(phoEta);
	static const double area[7] = {0.030, 0.057, 0.039, 0.015, 0.024, 0.039, 0.072};
	return area[phoRegion(eta)];
}
double Selector::phoEffArea03Pho(double phoEta){
	double eta = TMath::Abs(phoEta);
	static const double area[7] = {0.148, 0.130, 0.112, 0.216, 0.262, 0.260, 0.266};
	return area[phoRegion(eta)];
}

Selector::~Selector(){
}
