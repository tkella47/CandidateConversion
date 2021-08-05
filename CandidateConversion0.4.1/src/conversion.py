################################
#Written By : Thomas J. Kelly  #
#For: NorthPoint Group LLC     #
#Version: 1.0.0                #
#Purpose:Convert any resume TCC#
#extract to ORC                #
################################
import xml
import xml.etree.ElementTree as ET
import zipfile
import os
import zlib
import shutil
import sys
import pathlib
import pandas as pd
import argparse
#import base64

class TranslationFrame():
    def __init__(self,path):
        self.df  = pd.read_csv(path, dtype=str)
        
# Print iterations progress https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
def retrieve_file_paths(dirName):
 
  # setup file paths variable
  filePaths = []
   
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in files:
        # Create the full filepath by using os module.
        filePath = os.path.join(root, filename)
        filePaths.append(filePath)
         
  # return all paths
  return filePaths

def prepend_line(file_name, line):
   # """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = file_name + '.txt'
    # open original file in read mode and dummy file in write mode
    read_obj = open(file_name, 'r')
    write_obj = open(dummy_file, 'w')
        # Write given line to the dummy file
    write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
    for line in read_obj:
        write_obj.write(line)
    write_obj.close()
    read_obj.close()
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

def error_wrap():

    print("Error: Translation file moved back to original destination")
    print("Each batch folder should contain structure of Batch#: BlobFile [Folder with resume documents], candidate_info")
    raise Exception("Exiting wtih parsing with error: Translation file moved back to original destination")

def writeCandidateInfo(path, df_obj,columns):
    #print(path)
    filenames = retrieve_file_paths(path+"/Data")
    xml_file = ""
    for files in filenames:
        if ".xml" in files:
            xml_file = files
    if xml_file == "" or xml_file is None:
        raise Exception("XML file not found")
    tree =ET.parse(xml_file)
    root = tree.getroot()
    #print(root.tag)
    f = open(path+ "/Data/Candidate.dat","w")
    f.write("METADATA|Attachment|CandidateNumber|DataTypeCode|Category|Title|File|URLorFileName\n")
    file = open(path + "/debug.txt","w")
    file.write("CandidateId for resume not found in map\n")
    file_name = path + "/debug.txt"
    file.close()
    file = open(path + "/debug.txt","a")
    count = 0
    total = 0
    for child in root:
    #print(child.tag, child.attrib)
        total += 1
        underscoreIndex = child.attrib["path"].index("_")
        candidateId = child.attrib["path"][0:underscoreIndex]
        fileName = child.attrib["path"]
        
        df = df_obj.df
        #print("\n")
        #print(candidateId)
        OrcCandID = df.loc[df[columns[0]] == str(candidateId),columns[1]]
        if len(OrcCandID) == 0:
            #print("Match not found")
            #file.write("ID not contained in document:" + candidateId + "\n")
            file.write(candidateId + "\n")
            count +=1
        else:
            OrcCandID = OrcCandID.iloc[0]
            if OrcCandID == "!NotFound!" or OrcCandID == "!NotConverted!" or "!" in OrcCandID or "#" in OrcCandID:
                count += 1
                file.write(candidateId + "\n")
            else:
                candidateId = OrcCandID
                resultString = "MERGE|Attachment|" + candidateId + "|FILE|IRC_CANDIDATE_RESUME|" + fileName + "|" + fileName + "|" + fileName + "\n"
                f.write(resultString)
    f.close()
    file.close()
    #file.write("CandidateId for resume not found in map")
    #prepend_line_str = "CandidateId for resume not found in map")# + str(count) + " out of  "+ str(total)
    #prepend_line(file_name,prepend_line_str)
    #print("Finished with the write")
  


def zipBatchFolder(path): #Compress Batch folder in to a zip folder.
    filePaths = retrieve_file_paths(path)
    zip_file = zipfile.ZipFile(path + ".zip",mode = "w", compression = zipfile.ZIP_DEFLATED)
    with zip_file:
        for file in filePaths:
            #prePath and file cut are there to make zip_file.write write the proper structure. Needs to be editted to address beyond Blobfiles
            prePath = pathlib.PurePath(file)
            fileCut = ""
            if prePath.parent.name == "BlobFiles": # Move anything in blobFiles
                fileCut = prePath.parent.name + "/" + prePath.name
            elif ".dat" in prePath.name:
                fileCut = prePath.name
            if fileCut != "":
                zip_file.write(file,fileCut)
    zip_file.close()
def selectColumns(file):
    df = pd.read_csv(file)
    #print(df.columns)
    col_list = df.columns
    taleo_col = None
    oracle_col = None
    while(taleo_col == None):
        print(df.columns)
        taleo_col = input("Enter Taleo ID column name: ")
        print(taleo_col)
        if taleo_col in col_list:
            break
        else:
            print("column ",taleo_col," not found. Please enter a different column") 
            taleo_col = None
    while(oracle_col == None):
        print(df.columns)
        oracle_col = input("Enter Oracle ID column name: ")
        print(oracle_col)
        if oracle_col in col_list:
            break
        else:
            print("column ",oracle_col," not found. Please enter a different column") 
            oracle_col = None
    columns = (taleo_col,oracle_col)
    return columns


if __name__ == "__main__":
    argpath = ""   
    parser = argparse.ArgumentParser()
    requiredArgs = parser.add_argument_group("Required Arguments")
    requiredArgs.add_argument("-p", "--path",help = "path to where the resume batch folders are (do not provide path to single batch folder)(Additionally ensure the HCM_Candidate_Map.csv is located in this folder)", required = True)
    args = parser.parse_args()
    argpath = args.path
    if not os.path.exists(argpath):
        raise Exception("Path does not exist")
    argpath = argpath + "/"
    """

    ### ARGUMENT HANDLING ###
    if len(sys.argv) == 1: # Default to TCCBatch folder
        print("Searching for batch folders in ../TCCBatch")
        if not os.path.exists("../TCCBatch"):
            raise Exception("Please ensure batches are in TCCBatch folder")
        argpath = "../TCCBatch/"

    elif len(sys.argv) > 1 and len(sys.argv) < 3:
        print("Searching for batch files in", sys.argv[1])
        if not os.path.exists(sys.argv[1]):
            raise Exception("Directory does not exist")
        argpath = sys.argv[1] + "\\"
    else: 
        raise Exception("conversion.py takes an optional path argument for Batch folder source or defaults to ../TCCBatch, please ensure you are only passing 0 or 1 arguments")
    """
    ### MOVE TRANSLATION FILE TO SRC#
    cwd = os.getcwd()
    #Remove to implement translation
    if not os.path.exists(argpath + "/HCM_Candidate_Map.csv"):
        raise Exception("Please ensure HCM_Candidate_Map.csv is located in directory with all of the batch folders at the time of execution. Was looking in ",argpath)
    if not os.path.exists("HCM_Candidate_Map.csv"):
        shutil.move(argpath + "/HCM_Candidate_Map.csv" , cwd)
    translation_obj = TranslationFrame("HCM_Candidate_Map.csv")
    columns = selectColumns("HCM_Candidate_Map.csv")
    #"""
    
    
    
    
    ### MAIN PROCESSING ###
    raw_batches = os.listdir(argpath) # has all contents in directory

    if len(raw_batches) == 0: #If folder is empty, raise exception
        raise Exception("Folder is empty")
    
    num = 0
    print("Writing Candidate.dat and compressing")
    #printProgressBar(0, len(raw_batches), prefix = "Progress: ", suffix = "Complete")
    #print(raw_batches)
    try:
        for batch in raw_batches: #start going through every batch folder in the directory
            printProgressBar(num, len(raw_batches)*3, prefix = "Progress: ", suffix = "Complete || " + batch + "  ")
            #printProgressBar(num, len(raw_batches)*3, prefix = "Progress: ", suffix = "Complete " + batch)
            #print(batch)
            path = argpath + batch #path of batch folder
            #print(path)
            try:
                writeCandidateInfo(path,translation_obj, columns)#,translation_obj)
                num +=1 #progress bar tracker
               
                printProgressBar(num, len(raw_batches)*3, prefix = "Progress: ", suffix = "Complete || " + batch + "  ")
      
                zipBatchFolder(path) # Zip Batch folders
                num +=1 #progress bar tracker
                printProgressBar(num, len(raw_batches)*3, prefix = "Progress: ", suffix = "Complete || " + batch + "  ")
                if not os.path.exists("../ORCBatch"): #If output folder does not exist, create it. If it does, overwrite any copies in the folder
                    os.mkdir("../ORCBatch") #Makes directory
        
                src = path #source 
                dst = cwd[0:len(cwd)-4] + "\ORCBatch" #Destination (Places it right above the src directory into ORCBatch
                #print("cwd:",cwd)
                #print("src:",src)
                #print("src + .zip:", src + ".zip")
                #print("dst:",dst)

                shutil.move(src + ".zip" , dst + "/" + batch + ".zip") #Move zipped files from original directory to ORCBranch
                num += 1 #progress bar tracker
                printProgressBar(num, len(raw_batches)*3, prefix = "Progress: ", suffix = "Complete || " + batch + "  ")
            except:
                print("\nAn error occured for " + batch + ". Skipping this and moving to the next batch\n")
                num+= 3
            finally:
                pass
    except:
        print("\nAn error occured while executing script: moving back HCM file and exiting\n")
        shutil.move(cwd + "/HCM_Candidate_Map.csv" , argpath) #Move translation file back to original folder
    
    #""" Remove comments to add in translation function
    if os.path.exists(argpath + "/HCM_Candidate_Map.csv"):
        os.remove("HCM_Candidate_Map.csv")
    else:
        shutil.move(cwd + "/HCM_Candidate_Map.csv" , argpath) #Move translation file back to original folder
    
    print("\n")
    print("***Complete***")
    print("Files located at /ORCBatch, the directory above the script")
    #base64.encode(open(path + ".zip","rb"),open(path + ".dat","wb")
   # base64.decode(open(path + ".dat","rb"),open(path + "2.zip","wb"))
    





