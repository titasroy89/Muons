#ifndef HISTOGRAMMER_H
#define HISTOGRAMMER_H

#include<iostream>
#include<vector>
#include<map>
#include<string>
#include<TFile.h>
#include<TH1F.h>
#include<TH2F.h>
#include<TMath.h>
#include<TLorentzVector.h>

#include"EventTree.h"
#include"Selector.h"
#include"EventPick.h"

class Histogrammer{
public:
	Histogrammer(std::string titleIn);
	~Histogrammer(void);
	void fill(Selector* selector, EventPick* evtPick, EventTree* tree, double weight);
	void write_histograms(std::string folder, std::vector<TH1F*> histVector);
	
private:
	std::string title;
	std::map< std::string, TH1F* > hists;
	std::map< std::string, TH2F* > hists2d;
	
	void make_hist(const char* hname, const char* htitle, int nbins, double xlow, double xhigh, const char* xlabel, const char* ylabel);
	void make_hist2d(const char* hname, const char* htitle, int nxbins, double xlow, double xhigh, int nybins, double ylow, double yhigh);
	int minDrIndex(double myEta, double myPhi, std::vector<int> Inds, std::vector<float> *etas, std::vector<float> *phis);
	double minDr(double myEta, double myPhi, std::vector<int> Inds, std::vector<float> *etas, std::vector<float> *phis);
	double minDrPhoB(int PhoInd, EventTree* tree);
	double calc_ht(EventPick* evtPick, EventTree* tree);
};
#endif
