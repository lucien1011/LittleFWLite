
from Utils.TextFileHandler import ReadEventList

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#____________________________________________________________________________||

options = VarParsing.VarParsing()

#____________________________________________________________________________||

options.register('dataset',
                 "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Primary dataset")

options.register('textFilePath',
                 "test.txt", #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Text file for event list")

#____________________________________________________________________________||

options.parseArguments()

#____________________________________________________________________________||

eventList = ReadEventList(options.textFilePath)
inputEvtList = [ ":".join(event) for event in eventList ]
print inputEvtList

#____________________________________________________________________________||

process = cms.Process('SKIM')

#____________________________________________________________________________||

process.source = cms.Source("PoolSource")

#____________________________________________________________________________||

inputFileNames = cms.untracked.vstring()
import InputDataset.QCDHT500To700 as qcdFiles
inputFileNames.extend( qcdFiles.inputList )
process.source.fileNames = inputFileNames

#____________________________________________________________________________||

process.source.eventsToProcess = cms.untracked.VEventRange(*inputEvtList)

#____________________________________________________________________________||

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

#____________________________________________________________________________||

process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string("test.root") )

#____________________________________________________________________________||

process.p = cms.Path()
process.e = cms.EndPath(process.out)

#____________________________________________________________________________||
