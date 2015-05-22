#include"HistCollect.h"
bool isSignalPhoton(EventTree* tree, int mcInd, int recoPhoInd);
bool isGoodElectron(EventTree* tree, int mcInd, int recoPhoInd);

HistCollect::HistCollect(std::string namePrefix, std::string nameSuffix){
	// book histogrammers:
	// everything
	histnom = new Histogrammer(namePrefix+"_"+nameSuffix);
	histnom_barrel = new Histogrammer(namePrefix+"_barrel_"+nameSuffix);
	histnom_endcap = new Histogrammer(namePrefix+"_endcap_"+nameSuffix);
	
	// MC only: photon is:  real signal / real background / fake from e / fake from jet 
	// photon is real signal
	histnom_rs = new Histogrammer(namePrefix+"_rs_"+nameSuffix);
	histnom_barrel_rs = new Histogrammer(namePrefix+"_rs_barrel_"+nameSuffix);
	histnom_endcap_rs = new Histogrammer(namePrefix+"_rs_endcap_"+nameSuffix);
	
	// photon is fake from e
	histnom_fe = new Histogrammer(namePrefix+"_fe_"+nameSuffix);
	histnom_barrel_fe = new Histogrammer(namePrefix+"_fe_barrel_"+nameSuffix);
	histnom_endcap_fe = new Histogrammer(namePrefix+"_fe_endcap_"+nameSuffix);
	
	// combination of fake jets and background photons
	histnom_fjrb = new Histogrammer(namePrefix+"_fjrb_"+nameSuffix);
	histnom_barrel_fjrb = new Histogrammer(namePrefix+"_fjrb_barrel_"+nameSuffix);
	histnom_endcap_fjrb = new Histogrammer(namePrefix+"_fjrb_endcap_"+nameSuffix);
	
	// set default flag values
	fillSum = true;
	fillMCCategSum = true;
	fillBarrel = true;
	fillEndcap = true;
	fillRS = true;
	fillFE = true;
	fillFJRB = true;
}

HistCollect::~HistCollect(){
	// delete Histogrammers?
}

void HistCollect::fill_histograms(Selector* selector, EventPick* selEvent, EventTree* tree, bool isMC, double weight){
	if(!(selEvent->passPreSel)) return; // event did not pass preselction
	// find the photon category
	bool barrel;
	int phoInd = -1;
	if(selEvent->Photons.size()>0){
		phoInd = selEvent->Photons[0];
	}
	else {
		// no good photons, but we may need this event for 2D histograms
		for(int phoItmp = 0; phoItmp < selEvent->PhotonsPresel.size(); phoItmp++){
			if((int)selEvent->PhoPassChHadIso[phoItmp] + 
			   (int)selEvent->PhoPassPhoIso[phoItmp]+
			   (int)selEvent->PhoPassSih[phoItmp] >= 1){
				// at least 1 cut passed. Maybe just take the first one?
				phoInd = selEvent->PhotonsPresel[phoItmp];
				break;
			}
		}
	}
	
	bool passAllTemp = selEvent->passAll;
	// make histograms for pre-selection cuts
	selEvent->passAll = true;
	if(fillSum) histnom->fill(selector, selEvent, tree, weight);
	// keep the true value
	selEvent->passAll = passAllTemp;

	if(phoInd<0) return; // no good photon candidates
	barrel = fabs(tree->phoEta_->at(phoInd)) < 1.5;
	
	if(fillBarrel && barrel) histnom_barrel->fill(selector, selEvent, tree, weight);
	if(fillEndcap && !barrel) histnom_endcap->fill(selector, selEvent, tree, weight);
	
	// the following applies to MC only
	if(!isMC) return;
	
	// split by photon origin
	bool rs = false, rb = false, fe = false, fj = false;
	findPhotonCategory(phoInd, tree, &rs, &rb, &fe, &fj);
	
	// filling
	if(rs && fillRS){
		if(fillMCCategSum) histnom_rs->fill(selector, selEvent, tree, weight);
		if(fillBarrel && barrel) histnom_barrel_rs->fill(selector, selEvent,tree, weight);
		if(fillEndcap && !barrel) histnom_endcap_rs->fill(selector, selEvent ,tree, weight);
	}
	if(fe && fillFE){
		if(fillMCCategSum) histnom_fe->fill(selector, selEvent, tree, weight);
		if(fillBarrel && barrel) histnom_barrel_fe->fill(selector, selEvent, tree, weight);
		if(fillEndcap && !barrel) histnom_endcap_fe->fill(selector, selEvent, tree, weight);
	}
	if((fj||rb) && fillFJRB){
		if(fillMCCategSum) histnom_fjrb->fill(selector, selEvent, tree, weight);
		if(fillBarrel && barrel) histnom_barrel_fjrb->fill(selector, selEvent, tree, weight);
		if(fillEndcap && !barrel) histnom_endcap_fjrb->fill(selector, selEvent, tree, weight);
	}
}

void HistCollect::write_histograms(EventPick* selEvent, bool isMC, std::string outDir){
	std::vector<TH1F*> emptyVec;
	if(fillSum) histnom->write_histograms(outDir,selEvent->histVector);
	if(fillBarrel) histnom_barrel->write_histograms(outDir,emptyVec);
	if(fillEndcap) histnom_endcap->write_histograms(outDir,emptyVec);
	
	if(isMC){
		if(fillRS){
			if(fillMCCategSum) histnom_rs->write_histograms(outDir,selEvent->histVector);
			if(fillBarrel) histnom_barrel_rs->write_histograms(outDir,emptyVec);
			if(fillEndcap) histnom_endcap_rs->write_histograms(outDir,emptyVec);
		}
		if(fillFE){
			if(fillMCCategSum) histnom_fe->write_histograms(outDir,selEvent->histVector);
			if(fillBarrel) histnom_barrel_fe->write_histograms(outDir,emptyVec);
			if(fillEndcap) histnom_endcap_fe->write_histograms(outDir,emptyVec);
		}
		if(fillFJRB){
			if(fillMCCategSum) histnom_fjrb->write_histograms(outDir,selEvent->histVector);
			if(fillBarrel) histnom_barrel_fjrb->write_histograms(outDir,emptyVec);
			if(fillEndcap) histnom_endcap_fjrb->write_histograms(outDir,emptyVec);
		}
	}
	
}

void HistCollect::setFlagsSaveAll(void){
	fillSum = true;
	fillMCCategSum = true;
	fillBarrel = true;
	fillEndcap = true;
	fillRS = true;
	fillFE = true;
	fillFJRB = true;	
}
void HistCollect::setFlags2D(void){
	fillSum = false;
	fillMCCategSum = false;
	fillBarrel = true;
	fillEndcap = false;
	fillRS = true;
	fillFE = true;
	fillFJRB = true;
	
}

void HistCollect::findPhotonCategory(int phoInd, EventTree* tree, bool* rs, bool *rb, bool *fe, bool *fj){
	*rs = false;
	*rb = false;
	*fe = false;
	*fj = false;

	//std::cout << "\n\n\n start matching photon\n";

	// try to match with MC photons and electrons
	int mcPhotonInd = -1;
	int mcEleInd = -1;
	for(int mcInd=0; mcInd<tree->nMC_; ++mcInd){
		// crude matching to get candidates
		bool etetamatch = dR(tree->mcEta->at(mcInd),tree->mcPhi->at(mcInd),tree->phoEta_->at(phoInd),tree->phoPhi_->at(phoInd)) < 0.2 && 
			(fabs(tree->phoEt_->at(phoInd) - tree->mcPt->at(mcInd)) / tree->mcPt->at(mcInd)) < 1.0;
		
		//if(etetamatch) {
		//	std::cout << "mc candidate:\n";
		//	std::cout << "dPt/pt " << ((tree->phoEt_->at(phoInd) - tree->mcPt->at(mcInd)) / tree->mcPt->at(mcInd)) << "\n";
		//	std::cout << "PID " << tree->mcPID->at(mcInd) << "\n";
		//	std::cout << "parentage " << tree->mcParentage->at(mcInd) << "\n";
		//	std::cout << "mom Dr " << dR(tree->mcEta->at(mcInd),tree->mcPhi->at(mcInd),tree->mcMomEta->at(mcInd),tree->mcMomPhi->at(mcInd)) << "\n";
		//}

		if( etetamatch && mcPhotonInd < 0 && tree->mcPID->at(mcInd) == 22)
			mcPhotonInd = mcInd; 
		if( etetamatch && mcEleInd < 0 && abs(tree->mcPID->at(mcInd)) == 11 )
			mcEleInd = mcInd;
	}
	// see OverlapRemove.cpp for definitions of isSignalPhoton and isGoodElectron	
	if(mcPhotonInd >= 0){
		// signal: parents are quarks, gluons, bosons or leptons
		if(isSignalPhoton(tree, mcPhotonInd, phoInd)) *rs = true;
		else *rb = true;
	}
	else{
		// no good matched Gen Photon found - our photon is fake
		if(mcEleInd >= 0 && isGoodElectron(tree, mcEleInd, phoInd)) *fe = true;
		else *fj = true;
	}
}
