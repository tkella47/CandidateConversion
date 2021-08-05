from PyPDF4 import PdfFileReader,PdfFileWriter
import shutil
import argparse
import os
import docx
import comtypes.client
import csv
import pathlib
import zipfile
import zlib
import sys


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
def retrieve_dir_paths(dirName):
  #print(dirName)
  # setup file paths variable
  dirPaths = []
   
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    #print(root)
    for dirname in directories:
        # Create the full filepath by using os module.
        #print(dirName)
        dirPath = os.path.join(root, dirname)
        dirPaths.append(dirPath)
         
  # return all paths
  return dirPaths
def decompress(zippath):
        if os.path.exists(zippath.replace(".zip","")):
            print(zippath,"it exists")
            os.mkdir(zippath.replace(".zip",""))
        with zipfile.ZipFile(zippath,"r") as zip_ref:
            zip_ref.extractall(zippath.replace(".zip",""))
        #zipObj.close()

def resave_pdf(path):
    pdf_writer = PdfFileWriter()
    #read_file = open(path,"rb")
    pdf_reader = PdfFileReader(path)

    num_of_pages = pdf_reader.getNumPages()
    for i in range(0,num_of_pages):
        pdf_writer.addPage(pdf_reader.getPage(i))
    #read_file.close()
    os.remove(path)
    with open(path, 'wb') as write_file:
        pdf_writer.write(write_file)

def docx_2_pdf(inFile,word):
    wdFormatPDF = 17
    outFile = inFile.replace("docx","pdf")
    outFile = outFile.replace("DOCX","pdf")
    outFile = outFile.replace("doc","pdf")
    outFile = outFile.replace("DOC","pdf")
    #word = comtypes.client.CreateObject("Word.Application")
    failed = None
    
    try:
        doc = word.Documents.Open(inFile)
        #os.remove(inFile)
    except:
        print("There was an error opening document ", inFile)
        file_name = pathlib.PurePath(inFile)
        failed = file_name.name
    finally:
        try:
            doc.SaveAs(outFile, FileFormat = wdFormatPDF)
        except:
            print("There was an error saving document ", inFile)
        finally:
            try:
                doc.Close()
                os.remove(inFile)
            except:
                print("There was an error closing document " ,inFile)
            finally:
                pass
        #word.Quit()
    return failed
    
        


def rewrite_candidate(path,list_of_failed):
    csv.register_dialect("piper", delimiter= "|", quoting =csv.QUOTE_NONE)
    alt_path = path.replace(".dat","B.dat")
    csvfile = open(path,"r")
    newcsvfile = open(alt_path,"w")
    for row in csvfile:#csv.DictReader(csvfile, dialect = "piper"):
        update = True
        for name in list_of_failed:
            if name in row:
                update = False
        if update:
            row = row.replace(".docx",".pdf")
            row = row.replace(".DOCX",".pdf")
            row = row.replace(".doc",".pdf")
            row = row.replace(".DOC",".pdf")
        newcsvfile.write(row)
    csvfile.close()
    newcsvfile.close()
    os.remove(path)
    os.rename(alt_path,path)
    
def zipBatchFolder(path): #Compress Batch folder in to a zip folder.
    #print(path)
    filePaths = retrieve_file_paths(path)
    for file in filePaths:
        if "~$" in file:
            filePaths.remove(file)
    #print(filePaths)
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
     
    
    
    
#docx_2_pdf(r"C:\UAT\FailedBatch4\BlobFiles\1954655_2163489.docx")
#rewrite_candidate(r"C:\UAT\FailedBatch4\Candidate.dat")
if __name__ == "__main__":
    #############Argparse#################
    parser = argparse.ArgumentParser()
    requiredArgs = parser.add_argument_group("Required Arguments")
    requiredArgs.add_argument("-p","--path", help = "Collection of zip files that failed upload", required = True)
    args = parser.parse_args()
    path = args.path
    #path = "C:\\UAT\\Testbatch2"
    if not os.path.exists(path):
        raise Exception("Path does not exist")
    
    
    ######################################
    #print(path)
    fileNames = retrieve_file_paths(path)
    #print(fileNames)
    
    for file in fileNames:
        zip_file_name= pathlib.PurePath(file)
        print("******Converting files in ", zip_file_name.name, " ********")
        decompress(file)
        word = comtypes.client.CreateObject("Word.Application")
        os.remove(file)
        dirNames = retrieve_dir_paths(path)
        list_of_failed = []
        candidateDat = ""
        for directory in dirNames:
            directory_purepath = pathlib.PurePath(directory)
            if "BlobFiles" == directory_purepath.name:
                
                resumes = retrieve_file_paths(directory)
                #print(resumes)
                for resume in resumes:
                    resume_filename = pathlib.PurePath(resume)
                    if "~$" in resume_filename.name:
                        os.remove(resume)
                    elif ".pdf" in resume_filename.name.lower():
                        #print( " pdf method")
                        try:
                            resave_pdf(resume)
                        except:
                            print("Error resave_pdf. The file was ", resume)
                        finally:
                            pass
                    elif ".doc" in resume_filename.name.lower() or ".docx" in resume_filename.name.lower():
                        #print( " docx2pdf")
                        failed = docx_2_pdf(resume,word)
                        if failed != None:
                            list_of_failed.append(failed)
                        
                        """
                        try:
                            docx_2_pdf(resume,word)      
                        except:
                            print("Error docx_2_pdf. The file was" , resume)
                        finally:
                            pass
                        """
            
                #print("rewrote")
            else:
                candidateDat = directory + "\\Candidate.dat"
        word.Quit()
        rewrite_candidate(candidateDat,list_of_failed)
        zipBatchFolder(file.replace(".zip",""))
        shutil.rmtree(file.replace(".zip",""))
    #word.Quit()
        #print(dirNames)
    #Get directory Contents
    #For dir in directory
        #Decompress
        #Remove decompressed file
        #Set Candidate.dat path
        #For file in BlobFiles:
            #PurePath
            #If lower(file name) is .pdf:
                #resave_pdf(file)
            #If lower(file name) is ."docx","doc"
        #Rewrite Candidate.dat
        #Compress(zip)
       
    
