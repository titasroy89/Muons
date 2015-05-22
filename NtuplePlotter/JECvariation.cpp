#include"JetMETObjects/JetCorrectorParameters.h"
#include"JetMETObjects/FactorizedJetCorrector.h"
#include"JetMETObjects/JetCorrectionUncertainty.h"

#include<iostream>

class JECvariation{
public:
	JECvariation(std::string inputPrefix, bool isMC);
	~JECvariation();
	
	void applyJEC(EventTree* tree, int scaleDownNormUp012);

private:
	JetCorrectionUncertainty *jecUnc;

	JetCorrectorParameters *ResJetPar;
	JetCorrectorParameters *L3JetPar;
	JetCorrectorParameters *L2JetPar;
	JetCorrectorParameters *L1JetPar;

	FactorizedJetCorrector *JetCorrector;
};

JECvariation::JECvariation(std::string inputPrefix, bool isMC){
	if( isMC ){
		jecUnc = new JetCorrectionUncertainty((inputPrefix+"_MC_Uncertainty_AK5PF.txt").c_str());
		ResJetPar = new JetCorrectorParameters((inputPrefix+"_MC_L2L3Residual_AK5PF.txt").c_str());
		L3JetPar  = new JetCorrectorParameters((inputPrefix+"_MC_L3Absolute_AK5PF.txt").c_str());
		L2JetPar  = new JetCorrectorParameters((inputPrefix+"_MC_L2Relative_AK5PF.txt").c_str());
		L1JetPar  = new JetCorrectorParameters((inputPrefix+"_MC_L1FastJet_AK5PF.txt").c_str());
	}
	else{
		jecUnc = new JetCorrectionUncertainty((inputPrefix+"_DATA_Uncertainty_AK5PF.txt").c_str());
		ResJetPar = new JetCorrectorParameters((inputPrefix+"_DATA_L2L3Residual_AK5PF.txt").c_str());
		L3JetPar  = new JetCorrectorParameters((inputPrefix+"_DATA_L3Absolute_AK5PF.txt").c_str());
		L2JetPar  = new JetCorrectorParameters((inputPrefix+"_DATA_L2Relative_AK5PF.txt").c_str());
		L1JetPar  = new JetCorrectorParameters((inputPrefix+"_DATA_L1FastJet_AK5PF.txt").c_str());
	}
	std::vector<JetCorrectorParameters> vPar;
	vPar.push_back(*L1JetPar);
	vPar.push_back(*L2JetPar);
	vPar.push_back(*L3JetPar);
	if (!isMC) vPar.push_back(*ResJetPar);
	JetCorrector = new FactorizedJetCorrector(vPar);
}

JECvariation::~JECvariation(){

}

void JECvariation::applyJEC(EventTree* tree, int scaleDownNormUp012){
	if(scaleDownNormUp012 == 1) return; 
	for(int jetInd = 0; jetInd < tree->nJet_ ; ++jetInd){
		if(tree->jetPt_->at(jetInd) < 20) continue;
		JetCorrector->setJetEta(tree->jetEta_->at(jetInd));
		JetCorrector->setJetPt(tree->jetRawPt_->at(jetInd));
		JetCorrector->setJetA(tree->jetArea_->at(jetInd));
		JetCorrector->setRho(tree->rho2012_);
		
		double correction = JetCorrector->getCorrection();
		//std::cout << tree->jetPt_->at(jetInd) << "  " << tree->jetRawPt_->at(jetInd) << "  " << tree->jetPt_->at(jetInd)/tree->jetRawPt_->at(jetInd) << "  " << correction << std::endl;
		// assume jets are corrected, no need to change unless we want Up Down variation
		//tree->jetPt_->at(jetInd) = tree->jetRawPt_->at(jetInd) * correction;
		//tree->jetEn_->at(jetInd) = tree->jetRawEn_->at(jetInd) * correction;
		
		jecUnc->setJetEta(tree->jetEta_->at(jetInd));
		jecUnc->setJetPt(tree->jetPt_->at(jetInd)); // here you must use the CORRECTED jet pt
		double unc = jecUnc->getUncertainty(true);
		//std::cout << "unc " << unc << std::endl;
		if(scaleDownNormUp012==0) correction-=unc;
		if(scaleDownNormUp012==1) continue;
		if(scaleDownNormUp012==2) correction+=unc;
		
		tree->jetPt_->at(jetInd) = tree->jetRawPt_->at(jetInd) * correction;
		//tree->jetEn_->at(jetInd) = tree->jetRawEn_->at(jetInd) * correction;
	}
}

