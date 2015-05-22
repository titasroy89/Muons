#ifndef HISTCOLLECT_H
#define HISTCOLLECT_H

#include<string>
#include"EventTree.h"
#include"Histogrammer.h"
#include"EventPick.h"

class HistCollect{
public:
	HistCollect(std::string namePrefix, std::string nameSuffix);
	~HistCollect();
	void fill_histograms(Selector* selector, EventPick* selEvent, EventTree* tree, bool isMC, double weight);
	void write_histograms(EventPick* selEvent, bool isMC, std::string outDir);
	void setFlagsSaveAll(void);
	void setFlags2D(void);
	
	bool fillSum;
	bool fillMCCategSum;
	bool fillBarrel;
	bool fillEndcap;
	bool fillRS;
	bool fillFE;
	bool fillFJRB;
	
private:
	void findPhotonCategory(int phoInd, EventTree* tree, bool* rs, bool *fb, bool *fe, bool *fj);
	
	Histogrammer* histnom;
	Histogrammer* histnom_barrel;
	Histogrammer* histnom_endcap;
	Histogrammer* histnom_rs;
	Histogrammer* histnom_barrel_rs;
	Histogrammer* histnom_endcap_rs;
	Histogrammer* histnom_fe;
	Histogrammer* histnom_barrel_fe;
	Histogrammer* histnom_endcap_fe;
	Histogrammer* histnom_fjrb;
	Histogrammer* histnom_barrel_fjrb;
	Histogrammer* histnom_endcap_fjrb;
	
};
#endif
