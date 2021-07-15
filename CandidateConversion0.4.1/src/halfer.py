import os
import sys
import argparse
import pathlib
import zipfile
import csv
import shutil


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

def getDirSize(path):
    size = 0
    for ele in os.scandir(path):
        size += os.path.getsize(ele)
    return size

def decompress(zippath):
        if not os.path.exists(zippath.replace(".zip","")):
            os.mkdir(zippath.replace(".zip",""))
        zipObj = zipfile.ZipFile(zippath,"r")
        zipObj.extractall(zippath.replace(".zip",""))
        zipObj.close()


def get_fileNames_only(path): #returns tuple (paths of files in the top level directory, file name)
    dirlist = os.listdir(path)
    fileNames = []
    for item in dirlist:
        if os.path.isfile(path +"\\" + item):
            fileNames.append((path + "\\" + item, item))
    return fileNames
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

if __name__ == "__main__":
    ### Variable declaration###
    csv.register_dialect("piper", delimiter= "|", quoting =csv.QUOTE_NONE)
    #############################################

    ### ARGUMENT PARSING ###
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path", help = "Path to batch files", required = True)
    parser.add_argument("-d","--delete", help = "Remove uncompressed and working files, Default is True", default = "True")
    args = parser.parse_args()
    if args.delete.upper() == "FALSE":
        delete = False
    else:
        delete = True
    path = args.path
    if not os.path.exists(path):
        raise Exception("Path does not exist")
    ##############################################
    
    ### Obtain names of zip files and decompress###
    fileNames = get_fileNames_only(path)
    count = 0
    for file in fileNames:
        printProgressBar(count,len(fileNames)*2,prefix = "Progress", suffix = "Complete || " + file[1] + "     ")
        nonzip_path = file[0].replace(".zip","")
        decompress(file[0])
    ##############################################

        ### Create directories A and B ###
        if not os.path.exists(nonzip_path + "A"):
            os.mkdir(nonzip_path + "A")
            os.mkdir(nonzip_path + "A\\BlobFiles" )
        if not os.path.exists(nonzip_path + "B"):
            os.mkdir(nonzip_path + "B")
            os.mkdir(nonzip_path + "B\\BlobFiles" )
        ############################################
        
        ### Make new files ###    
        csvfile = open(nonzip_path + "\\Candidate.dat","r")
        new_file_a = open(nonzip_path + "A\\Candidate.dat","w")
        new_file_b = open(nonzip_path + "B\\Candidate.dat","w")
        new_file_a.write("METADATA|Attachment|CandidateNumber|DataTypeCode|Category|Title|File|URLorFileName\n")
        new_file_b.write("METADATA|Attachment|CandidateNumber|DataTypeCode|Category|Title|File|URLorFileName\n")
        ############################################
        ### Reading and writing Candidate.dat and dividing based on size ###
        dirSize = getDirSize(nonzip_path + "\\BlobFiles") 
        size = 0
        ### GO
        for row in csv.DictReader(csvfile, dialect = "piper"):

            #files = get_fileNames_only(nonzip_path + "A\\BlobFiles" )
            #print("size",size)
            #print(len(files))
            if size <= dirSize/2:
                
                try:
                    shutil.move(nonzip_path + "\\BlobFiles\\" + row["File"], nonzip_path + "A\\BlobFiles")
                    size = getDirSize(nonzip_path + "A\\BlobFiles\\")
                except:
                    pass
                finally:
                    new_file_a.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"] + "|" +row["File"] + "|" + row["URLorFileName"] + "\n")
                    #size = os.path.getsize(nonzip_path + "A\\BlobFiles")
            else:
                try:
                    shutil.move(nonzip_path + "\\BlobFiles\\" + row["File"], nonzip_path + "B\\BlobFiles")
                except:
                    pass
                finally:
                    new_file_b.write(row["METADATA"] + "|" + row["Attachment"] + "|" + row["CandidateNumber"] + "|" + row["DataTypeCode"] + "|" + row["Category"] + "|" +row["Title"] + "|" +row["File"] + "|" + row["URLorFileName"] + "\n")
                    #size = os.path.getsize(nonzip_path + "B\\BlobFiles")
        remainingFiles = get_fileNames_only(nonzip_path + "\\BlobFiles")
        count += 1
        printProgressBar(count,len(fileNames)*2,prefix = "Progress", suffix = "Complete || " + file[1] + "     ")
        if len(remainingFiles) != 0:
            for item in remainingFiles:
                
                if size <= dirSize/2:
                    shutil.move(item[0],nonzip_path + "A\\BlobFiles")
                    size = getDirSize(nonzip_path + "A\\BlobFiles\\")
                else:
                    shutil.move(item[0],nonzip_path + "B\\BlobFiles")
        new_file_a.close()
        csvfile.close()
        new_file_b.close()
        previous_path = file[0].replace(file[1],"Previous") 
        if not os.path.exists(previous_path):
            os.mkdir(previous_path)

        move_zip_to_previous_path = file[0].replace(file[1],"Previous\\" + file[1]) 
        shutil.move(file[0],move_zip_to_previous_path)
        zipBatchFolder(nonzip_path + "A")
        zipBatchFolder(nonzip_path + "B")
        #print(type(delete))
        if delete:
            shutil.rmtree(nonzip_path)
            shutil.rmtree(nonzip_path + "A")
            shutil.rmtree(nonzip_path + "B")
        count +=1
        printProgressBar(count,len(fileNames)*2,prefix = "Progress", suffix = "Complete || " + file[1] + "     ")
    print("\nComplete")
        #count += 1
        

