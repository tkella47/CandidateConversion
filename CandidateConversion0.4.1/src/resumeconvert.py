import os
import sys
import argparse
import zipfile
import zlib
import csv
import shutil
import pathlib
from docx2pdf import convert
#import docx
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
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
def retrieve_file_paths_nonTuple(dirName):
 
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
def retrieve_file_paths_zip(dirName):
 
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

def zipBatchFolder(path): #Compress Batch folder in to a zip folder.
    filePaths = retrieve_file_paths_nonTuple(path)
    zip_file = zipfile.ZipFile(path + ".zip",mode = "w", compression = zipfile.ZIP_DEFLATED)
    with zip_file:
        for file in filePaths:
            #prePath and file cut are there to make zip_file.write write the proper structure. Needs to be editted to address beyond Blobfiles
            prePath = pathlib.PurePath(file)
            fileCut = ""
            if ".xml" not in prePath.name and ".txt" not in prePath.name:
                if prePath.parent.name == "BlobFiles":# or prePath.parent.name == "Data":
                    fileCut = prePath.parent.name + "/" + prePath.name 
                else:
                    fileCut = prePath.name
                zip_file.write(file,fileCut)
    zip_file.close()
def retrieve_file_paths(dirName):
  # setup file paths variable
  dirPaths = []
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for file in files:
        # Create the full filepath by using os module.
        dirPath = os.path.join(root, file)
        dirPaths.append((dirPath,file.replace(".zip","")))
         
  # return all paths
  return dirPaths
def decompress(zippath):
        if not os.path.exists(zippath.replace(".zip","")):
            os.mkdir(zippath.replace(".zip",""))
        zipObj = zipfile.ZipFile(zippath,"r")
        zipObj.extractall(zippath.replace(".zip",""))
        zipObj.close()
def createZipFileNames(path):
    tempfileNames = retrieve_file_paths(path)
    fileNames = []
    for i in range(0,len(tempfileNames)):
        if ".zip" in tempfileNames[i][0]:
            fileNames.append(tempfileNames[i])
    return fileNames

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path", help = "path to errored zip files", required = True)
    args = parser.parse_args()
    path = args.path
    csv.register_dialect("piper", delimiter= "|", quoting =csv.QUOTE_NONE)
    if not os.path.exists(path):
        raise Exception("Path does not exist")
    fileNames = retrieve_file_paths(path)
    if not os.path.exists("oldDocx"):
        os.mkdir("oldDocx")
    else:
        shutil.rmtree("oldDocx")
        os.mkdir("oldDocx")
    for file in fileNames:
        if not os.path.exists("oldDocx"):
            os.mkdir("oldDocx")
        decompress(file[0])
        path_nonzip = file[0].replace(".zip","")
        os.rename(path_nonzip + "\Candidate.dat", path_nonzip + "\CandidateB.dat")
        #oldCand = open(path_nonzip + "\CandidateB.dat","r")
        newCand = open(path_nonzip + "\Candidate.dat","w")
        newCand.write("METADATA|Attachment|CandidateNumber|DataTypeCode|Category|Title|File|URLorFileName\n")
        with open(path_nonzip + "\CandidateB.dat","r") as csvfile:
            for row in csv.DictReader(csvfile, dialect = "piper"):
                if ".docx" in row["Title"] or ".DOCX" in row["Title"] or ".doc" in row["Title"] or ".DOC" in row["Title"]:
                    shutil.move(path_nonzip + "/BlobFiles/" + row["Title"],"oldDocx")
                    #line.replace(".docx")
                if ".docx" in row["Title"]:
                    newCand.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"].replace(".docx",".pdf") + "|" +row["File"].replace(".docx",".pdf") + "|" + row["URLorFileName"].replace(".docx",".pdf") + "\n")
                elif ".DOCX" in row["Title"]:
                    newCand.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"].replace(".DOCX",".pdf") + "|" +row["File"].replace(".DOCX",".pdf") + "|" + row["URLorFileName"].replace(".DOCX",".pdf") + "\n")
                elif ".doc" in row["Title"]:
                    newCand.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"].replace(".doc",".pdf") + "|" +row["File"].replace(".doc",".pdf") + "|" + row["URLorFileName"].replace(".doc",".pdf") + "\n")
                elif ".DOC" in row["Title"]:
                    newCand.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"].replace(".DOC",".pdf") + "|" +row["File"].replace(".DOC",".pdf") + "|" + row["URLorFileName"].replace(".DOC",".pdf") + "\n")
                else:
                    newCand.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"].replace(".DOC",".pdf") + "|" +row["File"].replace(".DOC",".pdf") + "|" + row["URLorFileName"].replace(".DOC",".pdf") + "\n")
                    #newCand.write(line)
        missedFileNames = retrieve_file_paths(path_nonzip + "/BlobFiles")
        
        for item in missedFileNames:
            if ".docx" in item[0] or ".DOCX" in item[0] or ".doc" in item[0] or ".DOC" in item[0]:
                shutil.move(item[0],"oldDocx")
        newCand.close()
        #docxFileNames = retrieve_file_paths("oldDocx")

        #docxFileNames = retrieve_file_paths(o)
        convert("oldDocx/",path_nonzip + "/BlobFiles/")

        #print("There was an error")
        shutil.rmtree("oldDocx")
        os.remove(path_nonzip + "/CandidateB.dat")
        os.remove(file[0])
        zipBatchFolder(path_nonzip)
        shutil.rmtree(path_nonzip)


        





















   