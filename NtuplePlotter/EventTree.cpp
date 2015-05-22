#include"EventTree.h"

EventTree::EventTree(int nFiles, char** fileNames){
	chain = new TChain("ggNtuplizer/EventTree");
	for(int fileI=0; fileI<nFiles; fileI++){
		chain->Add(fileNames[fileI]);
	}
	chain->SetBranchStatus("*",0);
	
	// keep some important branches
	chain->SetBranchStatus("nHLT",1);
	chain->SetBranchAddress("nHLT", &nHLT_);
	chain->SetBranchStatus("HLT",1);
	chain->SetBranchAddress("HLT", HLT_);
	chain->SetBranchStatus("HLTIndex",1);
	chain->SetBranchAddress("HLTIndex", HLTIndex_);
	chain->SetBranchStatus("bspotPos",1);
	chain->SetBranchAddress("bspotPos", bspotPos_);
	chain->SetBranchStatus("IsVtxGood",1);
	chain->SetBranchAddress("IsVtxGood", &IsVtxGood_);
	chain->SetBranchStatus("nPUInfo",1);
	chain->SetBranchAddress("nPUInfo", &nPUInfo_);
	nPU_ = new vector<int>;
	chain->SetBranchStatus("nPU",1);
	chain->SetBranchAddress("nPU", &nPU_);
	puBX_ = new vector<int>;
	chain->SetBranchStatus("puBX",1);
	chain->SetBranchAddress("puBX", &puBX_);
	puTrue_ = new vector<float>;
	chain->SetBranchStatus("puTrue",1);
	chain->SetBranchAddress("puTrue", &puTrue_);
	//chain->SetBranchStatus("",1);
	
	// event
	
	chain->SetBranchStatus("run",1);
	chain->SetBranchAddress("run", &run_);

	chain->SetBranchStatus("event",1);
	chain->SetBranchAddress("event", &event_);
	
	chain->SetBranchStatus("lumis",1);
	chain->SetBranchAddress("lumis", &lumis_);

	chain->SetBranchStatus("isData",1);
	chain->SetBranchAddress("isData", &isData_);

	chain->SetBranchStatus("nVtx",1);
	chain->SetBranchAddress("nVtx", &nVtx_);

	chain->SetBranchStatus("pfType01MET",1);    // FIXME
	chain->SetBranchAddress("pfType01MET", &pfMET_); // FIXME

	chain->SetBranchStatus("pfType01METPhi",1); // FIXME
	chain->SetBranchAddress("pfType01METPhi", &pfMETPhi_);  // FIXME

	chain->SetBranchStatus("pfMET*",1);
	chain->SetBranchStatus("pfType01MET*",1);
	
	// electrons	
	
	chain->SetBranchStatus("nEle",1);
	chain->SetBranchAddress("nEle", &nEle_);

	//chain->SetBranchStatus("eleEta",1);
	
	elePt_ = new vector<float>;
	chain->SetBranchStatus("elePt",1);
	chain->SetBranchAddress("elePt", &elePt_);

	eleSCEta_ = new vector<float>;
	chain->SetBranchStatus("eleSCEta",1);
	chain->SetBranchAddress("eleSCEta", &eleSCEta_);

	elePhi_ = new vector<float>;
	chain->SetBranchStatus("elePhi",1);
	chain->SetBranchAddress("elePhi", &elePhi_);

	elePFChIso03_ = new vector<float>;
	chain->SetBranchStatus("elePFChIso03",1);
	chain->SetBranchAddress("elePFChIso03", &elePFChIso03_);

	elePFNeuIso03_ = new vector<float>;
	chain->SetBranchStatus("elePFNeuIso03",1);
	chain->SetBranchAddress("elePFNeuIso03", &elePFNeuIso03_);

	elePFPhoIso03_ = new vector<float>;
	chain->SetBranchStatus("elePFPhoIso03",1);
	chain->SetBranchAddress("elePFPhoIso03", &elePFPhoIso03_);

	chain->SetBranchStatus("rho2012",1);
	chain->SetBranchAddress("rho2012", &rho2012_);

	eleIDMVATrig_ = new vector<float>;
	chain->SetBranchStatus("eleIDMVATrig",1);
	chain->SetBranchAddress("eleIDMVATrig", &eleIDMVATrig_);

	eleD0_ = new vector<float>;
	chain->SetBranchStatus("eleD0",1);
	chain->SetBranchAddress("eleD0", &eleD0_);

	eleMissHits_ = new vector<int>;
	chain->SetBranchStatus("eleMissHits",1);
	chain->SetBranchAddress("eleMissHits", &eleMissHits_);

	eleConvVtxFit_ = new vector<int>;
	chain->SetBranchStatus("eleConvVtxFit",1);
	chain->SetBranchAddress("eleConvVtxFit", &eleConvVtxFit_);

	eleDz_ = new vector<float>;
	chain->SetBranchStatus("eleDz",1);
	chain->SetBranchAddress("eleDz", &eleDz_);

	eleEoverP_ = new vector<float>;
	chain->SetBranchStatus("eleEoverP",1);
	chain->SetBranchAddress("eleEoverP", &eleEoverP_);

	// keep this branch in the skim
	chain->SetBranchStatus("elePin",1);

	eleSigmaIEtaIEta_ = new vector<float>;
	chain->SetBranchStatus("eleSigmaIEtaIEta",1);
	chain->SetBranchAddress("eleSigmaIEtaIEta", &eleSigmaIEtaIEta_);

	eledEtaAtVtx_ = new vector<float>;
	chain->SetBranchStatus("eledEtaAtVtx",1);
	chain->SetBranchAddress("eledEtaAtVtx", &eledEtaAtVtx_);

	eledPhiAtVtx_ = new vector<float>;
	chain->SetBranchStatus("eledPhiAtVtx",1);
	chain->SetBranchAddress("eledPhiAtVtx", &eledPhiAtVtx_);

	eleEcalEn_ = new vector<float>;
	chain->SetBranchStatus("eleEcalEn",1);
	chain->SetBranchAddress("eleEcalEn", &eleEcalEn_);

	eleHoverE_ = new vector<float>;
	chain->SetBranchStatus("eleHoverE",1);
	chain->SetBranchAddress("eleHoverE", &eleHoverE_);

	eleIsoTrkDR03_ = new vector<float>;
	chain->SetBranchStatus("eleIsoTrkDR03",1);
	chain->SetBranchAddress("eleIsoTrkDR03", &eleIsoTrkDR03_);

	eleIsoEcalDR03_ = new vector<float>;
	chain->SetBranchStatus("eleIsoEcalDR03",1);
	chain->SetBranchAddress("eleIsoEcalDR03", &eleIsoEcalDR03_);

	eleIsoHcalDR03_ = new vector<float>;
	chain->SetBranchStatus("eleIsoHcalDR03",1);
	chain->SetBranchAddress("eleIsoHcalDR03", &eleIsoHcalDR03_);

	eleGenIndex_ = new vector<int>;
	chain->SetBranchStatus("eleGenIndex",1);
	chain->SetBranchAddress("eleGenIndex", &eleGenIndex_);

	eleGenGMomPID_ = new vector<int>;
	chain->SetBranchStatus("eleGenGMomPID",1);
	chain->SetBranchAddress("eleGenGMomPID", &eleGenGMomPID_);

	eleGenMomPID_ = new vector<int>;
	chain->SetBranchStatus("eleGenMomPID",1);
	chain->SetBranchAddress("eleGenMomPID", &eleGenMomPID_);

	// muons
	// keep some branches in the skim
	muChi2NDF_ = new vector<float>;
	chain->SetBranchStatus("muChi2NDF", 1);
	chain->SetBranchAddress("muChi2NDF",&muChi2NDF_);

	muNumberOfValidTrkLayers_ = new vector<int>;
	chain->SetBranchStatus("muNumberOfValidTrkLayers",1);
	chain->SetBranchAddress("muNumberOfValidTrkLayers",&muNumberOfValidTrkLayers_);
		
	muNumberOfValidMuonHits_ = new vector<int>;
	chain->SetBranchStatus("muNumberOfValidMuonHits",1);
	chain->SetBranchAddress("muNumberOfValidMuonHits", &muNumberOfValidMuonHits_);

	muNumberOfValidPixelHits_ = new vector<int>;
	chain->SetBranchStatus("muNumberOfValidPixelHits",1);
	chain->SetBranchAddress("muNumberOfValidPixelHits",&muNumberOfValidPixelHits_);
	
	muDz_ = new vector<float>;
	chain->SetBranchStatus("muDz",1);
	chain->SetBranchAddress("muDz",&muDz_);
	
	muD0_ = new vector<float>;
	chain->SetBranchStatus("muD0",1);
	chain->SetBranchAddress("muD0",&muD0_);

	muStations_ = new vector<int>;
	chain->SetBranchStatus("muStations",1);
	chain->SetBranchAddress("muStations",&muStations_);

	chain->SetBranchStatus("nMu",1);
	chain->SetBranchAddress("nMu", &nMu_);

	muPt_ = new vector<float>;
	chain->SetBranchStatus("muPt",1);
	chain->SetBranchAddress("muPt", &muPt_);

	muEta_ = new vector<float>;
	chain->SetBranchStatus("muEta",1);
	chain->SetBranchAddress("muEta", &muEta_);

	muPhi_ = new vector<float>;
	chain->SetBranchStatus("muPhi",1);
	chain->SetBranchAddress("muPhi", &muPhi_);
	
	muPFIsoR04_CH_ = new vector<float>;
	chain->SetBranchStatus("muPFIsoR04_CH",1);
	chain->SetBranchAddress("muPFIsoR04_CH", &muPFIsoR04_CH_);
	
	muPFIsoR04_NH_ = new vector<float>;
	chain->SetBranchStatus("muPFIsoR04_NH",1);
	chain->SetBranchAddress("muPFIsoR04_NH", &muPFIsoR04_NH_);
	
	muPFIsoR04_Pho_ = new vector<float>;
	chain->SetBranchStatus("muPFIsoR04_Pho",1);
	chain->SetBranchAddress("muPFIsoR04_Pho", &muPFIsoR04_Pho_);

	muPFIsoR04_PU_ = new vector<float>;
	chain->SetBranchStatus("muPFIsoR04_PU",1);
	chain->SetBranchAddress("muPFIsoR04_PU", &muPFIsoR04_PU_);

	muType_ = new vector<int>;
	chain->SetBranchStatus("muType",1);
	chain->SetBranchAddress("muType",&muType_);
	
	// jets
	
	chain->SetBranchStatus("nJet",1);
	chain->SetBranchAddress("nJet", &nJet_);

	jetPt_ = new vector<float>;
	chain->SetBranchStatus("jetPt",1);
	chain->SetBranchAddress("jetPt", &jetPt_);

	jetRawPt_ = new vector<float>;
	chain->SetBranchStatus("jetRawPt",1);
        chain->SetBranchAddress("jetRawPt", &jetRawPt_);
	
	jetEta_ = new vector<float>;
	chain->SetBranchStatus("jetEta",1);
	chain->SetBranchAddress("jetEta", &jetEta_);
	
	jetPhi_ = new vector<float>;
	chain->SetBranchStatus("jetPhi",1);
	chain->SetBranchAddress("jetPhi", &jetPhi_);

	jetEn_ = new vector<float>;
	chain->SetBranchStatus("jetEn",1);
	chain->SetBranchAddress("jetEn", &jetEn_);

	jetArea_ = new vector<float>;
	chain->SetBranchStatus("jetArea",1);
	chain->SetBranchAddress("jetArea", &jetArea_);

	jetNConstituents_ = new vector<int>;
	chain->SetBranchStatus("jetNConstituents",1);
	chain->SetBranchAddress("jetNConstituents", &jetNConstituents_);
	
	jetNCharged_ = new vector<float>;
	chain->SetBranchStatus("jetNCharged",1);
	chain->SetBranchAddress("jetNCharged", &jetNCharged_);

	jetCEF_ = new vector<float>;	
	chain->SetBranchStatus("jetCEF",1);
	chain->SetBranchAddress("jetCEF", &jetCEF_);

	jetNHF_ = new vector<float>;
	chain->SetBranchStatus("jetNHF",1);
	chain->SetBranchAddress("jetNHF", &jetNHF_);
	
	jetNEF_ = new vector<float>;
	chain->SetBranchStatus("jetNEF",1);
	chain->SetBranchAddress("jetNEF", &jetNEF_);
	
	jetCHF_ = new vector<float>;
	chain->SetBranchStatus("jetCHF",1);
	chain->SetBranchAddress("jetCHF", &jetCHF_);

	jetCombinedSecondaryVtxBJetTags_ = new vector<float>;
	chain->SetBranchStatus("jetCombinedSecondaryVtxBJetTags",1);
	chain->SetBranchAddress("jetCombinedSecondaryVtxBJetTags", &jetCombinedSecondaryVtxBJetTags_);
	
	jetCombinedSecondaryVtxMVABJetTags_ = new vector<float>;
	chain->SetBranchStatus("jetCombinedSecondaryVtxMVABJetTags",1);
	chain->SetBranchAddress("jetCombinedSecondaryVtxMVABJetTags", &jetCombinedSecondaryVtxMVABJetTags_);

	jetPartonID_ = new vector<int>;
	chain->SetBranchStatus("jetPartonID",1);
	chain->SetBranchAddress("jetPartonID", &jetPartonID_);
	
	jetGenPartonID_ = new vector<int>;
	chain->SetBranchStatus("jetGenPartonID",1);
	chain->SetBranchAddress("jetGenPartonID", &jetGenPartonID_);
	
	jetGenJetIndex_ = new vector<int>;
	chain->SetBranchStatus("jetGenJetIndex",1);
	chain->SetBranchAddress("jetGenJetIndex", &jetGenJetIndex_);

	jetGenJetPt_ = new vector<float>;
	chain->SetBranchStatus("jetGenJetPt",1);
	chain->SetBranchAddress("jetGenJetPt", &jetGenJetPt_);

	jetGenPt_ = new vector<float>;
	chain->SetBranchStatus("jetGenPt",1);
	chain->SetBranchAddress("jetGenPt", &jetGenPt_);
	
	jetGenEta_ = new vector<float>;
	chain->SetBranchStatus("jetGenEta",1);
	chain->SetBranchAddress("jetGenEta", &jetGenEta_);
	
	jetGenPhi_ = new vector<float>;
	chain->SetBranchStatus("jetGenPhi",1);
	chain->SetBranchAddress("jetGenPhi", &jetGenPhi_);

	// photons
	
	chain->SetBranchStatus("nPho",1);
	chain->SetBranchAddress("nPho", &nPho_);

	phoEt_ = new vector<float>;	
	chain->SetBranchStatus("phoEt",1);
	chain->SetBranchAddress("phoEt", &phoEt_);
	
	phoEta_ = new vector<float>;
	chain->SetBranchStatus("phoEta",1);
	chain->SetBranchAddress("phoEta", &phoEta_);

	phoPhi_ = new vector<float>;
	chain->SetBranchStatus("phoPhi",1);
	chain->SetBranchAddress("phoPhi", &phoPhi_);
	
	phoIsConv_ = new vector<int>;
	chain->SetBranchStatus("phoIsConv",1);
	chain->SetBranchAddress("phoIsConv", &phoIsConv_);
	
	phohasPixelSeed_ = new vector<int>;
	chain->SetBranchStatus("phohasPixelSeed",1);
	chain->SetBranchAddress("phohasPixelSeed", &phohasPixelSeed_);

	phoEleVeto_ = new vector<int>;
	chain->SetBranchStatus("phoEleVeto",1);
	chain->SetBranchAddress("phoEleVeto", &phoEleVeto_);
	
	phoHoverE_ = new vector<float>;
	chain->SetBranchStatus("phoHoverE",1);
	chain->SetBranchAddress("phoHoverE", &phoHoverE_);

	phoSigmaIEtaIEta_ = new vector<float>;
	chain->SetBranchStatus("phoSigmaIEtaIEta",1);
	chain->SetBranchAddress("phoSigmaIEtaIEta", &phoSigmaIEtaIEta_);
	
	phoPFChIso_ = new vector<float>;
	chain->SetBranchStatus("phoPFChIso",1);
	chain->SetBranchAddress("phoPFChIso", &phoPFChIso_);
	
	phoPFNeuIso_ = new vector<float>;
	chain->SetBranchStatus("phoPFNeuIso",1);
	chain->SetBranchAddress("phoPFNeuIso", &phoPFNeuIso_);

	phoPFPhoIso_ = new vector<float>;
	chain->SetBranchStatus("phoPFPhoIso",1);
	chain->SetBranchAddress("phoPFPhoIso", &phoPFPhoIso_);

	phoSCRPhoIso_ = new vector<float>;
	chain->SetBranchStatus("phoSCRPhoIso",1);
	chain->SetBranchAddress("phoSCRPhoIso", &phoSCRPhoIso_);

	phoSCRChIso_ = new vector<float>;
	chain->SetBranchStatus("phoSCRChIso",1);
	chain->SetBranchAddress("phoSCRChIso", &phoSCRChIso_);
	
	phoRandConePhoIso_ = new vector<float>;
	chain->SetBranchStatus("phoRandConePhoIso",1);
	chain->SetBranchAddress("phoRandConePhoIso", &phoRandConePhoIso_);
	
	phoRandConeChIso_ = new vector<float>;
	chain->SetBranchStatus("phoRandConeChIso",1);
	chain->SetBranchAddress("phoRandConeChIso", &phoRandConeChIso_);

	phoGenIndex_ = new vector<int>;
	chain->SetBranchStatus("phoGenIndex",1);
	chain->SetBranchAddress("phoGenIndex", &phoGenIndex_);
	
	phoGenGMomPID_ = new vector<int>;
	chain->SetBranchStatus("phoGenGMomPID",1);
	chain->SetBranchAddress("phoGenGMomPID", &phoGenGMomPID_);
	
	phoGenMomPID_ = new vector<int>;
	chain->SetBranchStatus("phoGenMomPID",1);
	chain->SetBranchAddress("phoGenMomPID", &phoGenMomPID_);
	
	// MC gen particles
	
	chain->SetBranchStatus("nMC",1);
	chain->SetBranchAddress("nMC", &nMC_);
	
	mcPt = new vector<float>;
	chain->SetBranchStatus("mcPt",1);
	chain->SetBranchAddress("mcPt", &mcPt);
	
	mcEta = new vector<float>;
	chain->SetBranchStatus("mcEta",1);
	chain->SetBranchAddress("mcEta", &mcEta);
	
	mcPhi = new vector<float>;
	chain->SetBranchStatus("mcPhi",1);
	chain->SetBranchAddress("mcPhi", &mcPhi);
	
	mcMass = new vector<float>;
	chain->SetBranchStatus("mcMass",1);
	chain->SetBranchAddress("mcMass", &mcMass);
	
	mcPID = new vector<int>;
	chain->SetBranchStatus("mcPID",1);
	chain->SetBranchAddress("mcPID", &mcPID);
	
	mcMomPID = new vector<int>;
	chain->SetBranchStatus("mcMomPID",1);
	chain->SetBranchAddress("mcMomPID", &mcMomPID);
	
	mcGMomPID = new vector<int>;
	chain->SetBranchStatus("mcGMomPID",1);
	chain->SetBranchAddress("mcGMomPID", &mcGMomPID);
	
	mcDecayType = new vector<int>;
	chain->SetBranchStatus("mcDecayType",1);
	chain->SetBranchAddress("mcDecayType", &mcDecayType);
	
	mcIndex = new vector<int>;
	chain->SetBranchStatus("mcIndex",1);
	chain->SetBranchAddress("mcIndex", &mcIndex);
	
	mcMomPt = new vector<float>;
	chain->SetBranchStatus("mcMomPt",1);
	chain->SetBranchAddress("mcMomPt", &mcMomPt);
	
	mcMomEta = new vector<float>;
	chain->SetBranchStatus("mcMomEta",1);
	chain->SetBranchAddress("mcMomEta", &mcMomEta);
	
	mcMomPhi = new vector<float>;
	chain->SetBranchStatus("mcMomPhi",1);
	chain->SetBranchAddress("mcMomPhi", &mcMomPhi);
	
	mcMomMass = new vector<float>;
	chain->SetBranchStatus("mcMomMass",1);
	chain->SetBranchAddress("mcMomMass", &mcMomMass);
	
	mcParentage = new vector<int>;
	chain->SetBranchStatus("mcParentage",1);
	chain->SetBranchAddress("mcParentage", &mcParentage);
	
	//chain->SetBranchStatus("",1);
	//chain->SetBranchAddress("", _);
}

EventTree::~EventTree(){
	delete chain;
	// will be some memory leak due to created vectors
}

Long64_t EventTree::GetEntries(){
	return chain->GetEntries();
}

Int_t EventTree::GetEntry(Long64_t entry){
	chain->GetEntry(entry);
	return 0;
}
