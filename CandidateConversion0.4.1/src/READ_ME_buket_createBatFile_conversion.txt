Documentation for buket,conversion, and createBatFile
Scripts created by Thomas Kelly
For Northpoint Group LLC
Org: May 20th, 2021
Updated: May 24th, 2021

Version 0.2:
added resumeconvert.py and halfer.py


Version 0.1:
added argparse for arguments


Dependencies required:
    Python 3.9.2 or later
    pandas any current version
    
    To install pandas:
    from cmd line : pip install pandas
    
buket.py     [type -h for help]
    PURPOSE: Creates the config and export xml scripts for Taleo TCC.
    
    ARGUMENTS: Buket takes 2 required arguments and 1 options
        Required Argument 1: -p/--path    : Path to ResumeValues.csv or equivalent file (Must contain file size and docuNumber)
        Required Argument 2: -s/--storage : Path to TCC data storage: Path will be written in the config files
        Optional Argument 3: -l/--limit   : Data limit in MB: Default = 50 MB. In case Taleo TCC has data tranfer limits, allows batches to be broken up in to smaller sizes
    	Optional Argument 4: -n/--number  : Limit how many batches are created.
    TO RUN:
        Navigate to src folder
        Surround argument1 and argument2 with quote
        python buket.py -p "argument1" -s "argument2"
        or 
        python buket.py -p "argument1 -s "argument2" -l optional3
        etc
        
        Example: python buket.py -p "../dat/ResumeValues.csv" -s "C:\Users\VNRTHPT\OneDrive - PearFruit PLC\Documents\TCC" -l 100
        
    AFTER EXECUTION:
        Script files can be found under ../TCCScripts
        Each is nested under a Batch folder

         
createBatFile.py     [type -h for help]
    PURPOSE: Create .bat file from config and export xml scripts
    
    ARGUMENTS: 2 required arguments
        buket.py must have successfully executed first.
        Required Argument 1: -p/--path   : path where TaleoConnectClient.bat is located
        Required Argument 2: -l/--log    : path to where the log files will be stored
	    Optional Argument 3: -n/--number : limit how many batches will be run
    
    TO RUN:
        Navigate to src folder
        Surround argument1 and argument2 with quotes
        python createBatFile.py -p "argument1" -l "argument2"
        
        Example: python createBatFile.py -p "C:\\Taleo Connect Client\TaleoConnectClient.bat" -l "C:\Taleo\TaleoScripts\NewHire\Worker\Logs\"
        
    AFTER EXECUTION:
        bat file will have been created under src as TCC_Automation.bat
        ./src/TCC_Automation.bat
        
conversion.py    [type -h for help]
    PURPOSE: Writes Candidate.dat and compresses contents from extract
    
    ARGUMENTS: 1 required argument
        Required Argument 1: Path to folder where Batch files containing Blobfile directory and Data directory with .xml for resume. 
        File HCM_Candidate_Map must be in the same directory containing the batch directories
    EXAMPLE: conversion.py -p "../TCCBatches"

    DIRECTORY STRUCTURE
    /TCCBatches (or custom name)
    --/HCM_Candidate_Map.csv
    --/Batch01
    ----/BlobFiles
    ------/Resume1.pdf
    ------/Resume2.docx
    ----/Data
    ------/ResumeInfo123.xml
    
    HCM_Candidate_Map.csv Structure:
	Program will ask you to select the candidate mapping
	HCM_Candidate_Map must have at least two columns to enable mapping

    TO RUN:
        Navigate to src folder
        Surround optional argument 1 with quotes
        
        python conversion.py 
        or
        python conversion.py -p "../TCCBatchsCustom"
        
    AFTER EXECUTION:
        Zipped batches will be written in ../ORCBatch
        If an error occurs during the execution, the batch where the error occured will be skipped. 

In solutions folder:
	resume-resave.py
		PURPOSE:To resave any PDFs and covert doc/xs to PDFs
		ARGUMENTS 1: -p/--path: Path to folder with failed batches
		OUTPUT: Will output corrected zipfolders to same directory
		
		NOTE:You may see various errors on command line, that is okay.

      
    
        
