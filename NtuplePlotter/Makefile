all: makeTemplates makeSkim signalAcceptance

makeTemplates: Histogrammer.o HistCollect.o Selector.o EventPick.o EventTree.o makeTemplates.cpp OverlapRemove.cpp PUReweight.cpp PUReweight.h JECvariation.cpp
	g++ -o makeTemplates `root-config --libs` -I`root-config --incdir` EventTree.o Selector.o EventPick.o Histogrammer.o HistCollect.o makeTemplates.cpp OverlapRemove.cpp PUReweight.cpp JetMETObjects/FactorizedJetCorrector.o JetMETObjects/JetCorrectorParameters.o JetMETObjects/SimpleJetCorrector.o JetMETObjects/JetCorrectionUncertainty.o JetMETObjects/SimpleJetCorrectionUncertainty.o

makeSkim: Selector.o EventPick.o EventTree.o makeSkim.cpp OverlapRemove.cpp
	g++ -o makeSkim `root-config --libs` -I`root-config --incdir` EventTree.o EventPick.o Selector.o OverlapRemove.cpp makeSkim.cpp

signalAcceptance: Selector.o EventPick.o EventTree.o signalAcceptance.cpp OverlapRemove.cpp
	g++ -o signalAcceptance `root-config --libs` -I`root-config --incdir` EventTree.o EventPick.o Selector.o OverlapRemove.cpp signalAcceptance.cpp

EventTree.o: EventTree.cpp EventTree.h
	g++ -c -I`root-config --incdir` EventTree.cpp

Selector.o: Selector.cpp Selector.h
	g++ -c -I`root-config --incdir` Selector.cpp

EventPick.o: EventPick.cpp EventPick.h
	g++ -c -I`root-config --incdir` EventPick.cpp 

Histogrammer.o: Histogrammer.cpp Histogrammer.h
	g++ -c -I`root-config --incdir` Histogrammer.cpp

HistCollect.o: HistCollect.cpp HistCollect.h
	g++ -c -I`root-config --incdir` HistCollect.cpp

clean:
	rm EventTree.o Selector.o Histogrammer.o HistCollect.o EventPick.o
