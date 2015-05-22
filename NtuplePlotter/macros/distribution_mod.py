import glob
import ROOT

class distribution:
	def shiftUnderOverFlow(self, histNameList):
		for histName in histNameList:
			nBins = self.histList[histName].GetNbinsX()

			# store bin information
			underFlow    = self.histList[histName].GetBinContent(0)
			underFlowErr = self.histList[histName].GetBinError(0)
			overFlow     = self.histList[histName].GetBinContent(nBins+1)
			overFlowErr  = self.histList[histName].GetBinError(nBins+1)
			
			firstBin    = self.histList[histName].GetBinContent(1)
			firstBinErr = self.histList[histName].GetBinError(1)
			lastBin     = self.histList[histName].GetBinContent(nBins)
			lastBinErr  = self.histList[histName].GetBinError(nBins)

			# overwrite with new values
			self.histList[histName].SetBinContent(0, 0)
			self.histList[histName].SetBinError(0, 0)
			self.histList[histName].SetBinContent(nBins+1, 0)
			self.histList[histName].SetBinError(nBins+1, 0)
			
			self.histList[histName].SetBinContent(1, firstBin + underFlow)
			self.histList[histName].SetBinError(1, (firstBinErr**2 + underFlowErr**2)**0.5)
			self.histList[histName].SetBinContent(nBins, lastBin + overFlow)
			self.histList[histName].SetBinError(nBins, (lastBinErr**2 + overFlowErr**2)**0.5)


	def __init__(self, name, inputFilesAndScales, histNameList, color=0, style=1001):
		self.name = name
		self.histList = {}

		for files,scale in inputFilesAndScales:
			for filename in glob.glob(files):
				print 'reading file ',filename
				tf = ROOT.TFile(filename, 'READ')
				for histName in histNameList:
					#print 'extracting histogram ',histName
					tempHist = tf.Get(histName)
					if not tempHist.__bool__():
						print '  ====  Error while extracting histogram ',histName
						break
					tempHist.Sumw2()
					tempHist.Scale(scale)
					if histName not in self.histList:
						self.histList[histName] = tempHist.Clone()
						self.histList[histName].SetDirectory(0)
						self.histList[histName].SetName(self.name + '_' + tempHist.GetName())
						self.histList[histName].SetFillColor(color)
						if color!=0: self.histList[histName].SetLineColor(color)
						self.histList[histName].SetFillStyle(style)
						self.histList[histName].SetTitle('')
					else:
						self.histList[histName].Add(tempHist)
				tf.Close()
		#self.shiftUnderOverFlow(histNameList)
	
	def mergeWith(self, other):
		for histName in self.histList:
			self.histList[histName].Add(other.histList[histName])
		


