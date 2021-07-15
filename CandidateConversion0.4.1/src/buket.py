################################
#Written By : Thomas J. Kelly  #
#For: NorthPoint Group LLC     #
#Version: 1.0.0                #
#Purpose:Written to produce XML#        
#config and expot for Taleo    #
################################
import numpy as np
import pandas as pd
import xml
import xml.etree.ElementTree as ET
import math
import shutil
import os
import glob
import sys
import argparse

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
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def docuNumBinding(path,limit):
    #Working as expected! Counts check out 
    df = pd.read_csv(path, dtype = str)
    docuNumArray = []
    sum = 0
    index_list=[]
    #printProgressBar(0, len(df), prefix = "Extraction Progress: ", suffix = "Complete")
    for index, row in df.iterrows():
        if int(row[2]) == 0:
            pass
        elif sum + int(row[2]) > limit:
            docuNumArray.append(index_list.copy())
            index_list = [row[1]]
            sum = int(row[2])
        else:
            index_list.append(row[1])
            sum += int(row[2])
        if index % 10 ==0:
            printProgressBar(index, len(df), prefix = "Progress: ", suffix = "Complete")
    #try:
    #    if not math.isnan(index_list[0]):
    docuNumArray.append(index_list.copy())
    #except:
    #    pass
    #finally:
    #    pass
    return docuNumArray

def writeConfig(index, base):
    tree = ET.parse("Template_cfg.xml")
    batch_key = "Batch" + str(index)
    writeGlobal(tree,batch_key,base)
    writeBoardSymbol(tree,batch_key,base)
    tree.write( batch_key+ "_pre_cfg.xml")
    

def writeGlobal(tree,batch_key,base):
    root = tree.getroot()
    items = root.findall("./{http://www.taleo.com/ws/integration/client}Global/{http://www.taleo.com/ws/integration/client}General/{http://www.taleo.com/ws/integration/client}ConfigurationIdentifier")
    items[0].text = batch_key
    items = root.findall("./{http://www.taleo.com/ws/integration/client}Global/{http://www.taleo.com/ws/integration/client}General/{http://www.taleo.com/ws/integration/client}RequestMessage/{http://www.taleo.com/ws/integration/client}File/{http://www.taleo.com/ws/integration/client}SpecificFile")
    items[0].text = "[TCC_SCRIPT_DIR]\\" + batch_key + "_sq.xml"


def writeBoardSymbol(tree,batch_key,base):
   
    #tree = ET.parse("Template_cfg.xml")
    root = tree.getroot()
    taleo = None
    items = root.findall("./{http://www.taleo.com/ws/integration/client}Global/{http://www.taleo.com/ws/integration/client}Board/{http://www.taleo.com/ws/integration/client}Symbols/{http://www.taleo.com/ws/integration/client}Symbol")#[@name='DATA_OUTPUT_DIR']")
                           #///[@name='DATA_OUTPUT_DIR']")
    cwd = os.getcwd()
    script_dir = cwd.replace("src","TCCScripts\\" + batch_key)
    items[0].text = base + "\\Resume\\" +  batch_key + "\\Data"
    items[1].text = base + "\\Resume\\" +  batch_key + "\\BlobFiles"
    items[2].text = script_dir
    items[3].text = cwd + "\\templates"
    

    
def writeExtract(docArray, index):
    tree = ET.parse("Template_sq.xml")
    root = tree.getroot()
    items = root.findall("./{http://www.taleo.com/ws/integration/query}filterings//{http://www.taleo.com/ws/integration/query}list")
    list_obj = items[0]
    for num in docArray:
        element = list_obj.makeelement("quer:integer",{})
        element.text = str(num)
        list_obj.append(element)
    filename = "Batch" + str(index) + "_pre_sq.xml"
    tree.write(filename)

def postProcess(path):
    fin = open(path + "_pre_cfg.xml", "rt")
    fout = open(path + "_cfg.xml", "wt")
    for line in fin:
        fout.write(line.replace("ns0","quer"))
    fin.close()
    fout.close()
    os.remove(path + "_pre_cfg.xml")
    fin = open(path + "_pre_sq.xml", "rt")
    fout = open(path + "_sq.xml", "wt")
    for line in fin:
        fout.write(line.replace("ns0","quer"))
    fin.close()
    fout.close()
    os.remove(path + "_pre_sq.xml")


if __name__ == "__main__":
    limit = 1024*1000*100
    path = "../dat/ResumeValues.csv"
    base = "C:\\Users\\VKELLTI\\OneDrive - Pearson PLC\\Documents\\TCC"
    num_of_batches = 0
    #print(len(sys.argv))
    #print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--limit", help = "The memory chunk size. Default is 100 MB", default = 100, type = int)
    parser.add_argument("-n","--number",help = "The number of batches you want scripts to be created for", default = 0, type =int)
    requiredNamed = parser.add_argument_group("Required Arguments")
    requiredNamed.add_argument("-p","--path", help = "path to csv with resumeValues (Must include the file name)",required = True)
    requiredNamed.add_argument("-s", "--storage", help = "TCC Memory storage path", required = True)
    args = parser.parse_args()
    limit = 1024 * 1000 * args.limit
    path = args.path
    base = args.storage
    num_of_batches = args.number
    if not os.path.exists(path):
        raise Exception("Path does not exists")
    #print(args)

    print("Extracting document number keys")
    docNum_2dArray = docuNumBinding(path,limit) #pull 2D list of docuNums based on chunk sizes
    #writeConfig(2,base)f
    #writeExtract([1,2,3],"1")
    print("\n")
    print("Success: Writing config and extract files")
    
    if num_of_batches != 0:
        if len(docNum_2dArray)  < num_of_batches:
            print("There are fewer batches than requested, so creating files for all batches")
    else:
        num_of_batches = len(docNum_2dArray)
    
    for i in range(0,num_of_batches):
        writeConfig(i+1,base)
        writeExtract(docNum_2dArray[i], i+1)
        if not os.path.exists("../TCCScripts"):
            os.mkdir("../TCCScripts")
        if not os.path.exists("../TCCScripts/Batch" + str(i+1)):
            os.mkdir("../TCCScripts/Batch" + str(i+1))
        else:
            shutil.rmtree("../TCCScripts/Batch" + str(i+1))
            os.mkdir("../TCCScripts/Batch" + str(i+1))

        #os.mkdir("../TCCScripts/Batch" + str(i+1))
        shutil.move("Batch" + str(i+1) + "_pre_cfg.xml","../TCCScripts/Batch" + str(i+1))
        shutil.move("Batch" + str(i+1) + "_pre_sq.xml","../TCCScripts/Batch" + str(i+1))
        postProcess("../TCCScripts/Batch" + str(i+1) + "/Batch"  + str(i+1))
        printProgressBar(i+1, num_of_batches, prefix = "Progress: ", suffix = "Complete")
    print("\nComplete")
    print("scripts located in TCCScripts above src")

        

    






    

    


        



