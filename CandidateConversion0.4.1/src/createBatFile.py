import os
import sys
import math
import argparse

def retrieve_dir_paths(dirName):
 
  # setup file paths variable
  dirPaths = []
   
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for directory in directories:
        # Create the full filepath by using os module.
        dirPath = os.path.join(root, directory)
        dirPaths.append(dirPath)
         
  # return all paths
  return dirPaths


if __name__ == "__main__":
    ### ARGUMENT PARSING ###
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help = "How many batches should be listed in the bat file", type = int, default = 0)
    requiredNamed = parser.add_argument_group("Required Arguments")
    requiredNamed.add_argument("-p","--path", help = "Path to TaleoConnectClient.bat", required = True)
    requiredNamed.add_argument("-l","--log", help = "Path to where log files should be written during batch execution", required = True)
    args = parser.parse_args()
    launch_path = args.path
    import_file_log_path = args.log # + "\" #LOG PATH HERE
    loops = args.number + 1 if args.number != 0 else 0
    #print(loops)

    path = "TCC_Automation.bat"
    #launch_path = sys.argv[1]#"C:\\Taleo Connect Client\\TaleoConnectClient.bat"
    #import_result_log_path ="C:\\Taleo\\TaleoScripts\\NewHire\\Worker\\Files\\"
    #import_file_log_path = sys.argv[2]#"C:\\Taleo\TaleoScripts\\NewHire\\Worker\\Logs\\"
    #if len(sys.argv) == 4:
        #if math.isnan(int(sys.argv[3])):
            #raise Exception("the optional argument must be a number")
        #loops = int(sys.argv[3]) + 1
    dirNames = retrieve_dir_paths("../TCCScripts")
    cwd = os.getcwd()
    cwd = cwd[0:len(cwd)-4] + "\\TCCScripts\\"
    for i in range(0,len(dirNames)):
        dirNames[i] = dirNames[i].replace("../TCCScripts\\","")
    file = open(path,"w")
    #file.write("set ltime=%time:~1,8%\nset ldate=%date:~4,12%\nset ltime=%ltime::=-%\nset ltime=%ltime:.=%\nset ldate=%ldate:/=-%\n")
    #file.write("SET LogFile1 = \""+ import_file_log_path +
    count = 1
    #print(len(dirNames))
    if loops > len(dirNames):
        print("Greater number of batch files requested that avaliable, writing all")
    for dir in dirNames:
        if count == loops:
            #print("Broken")
            break
            #break
        #print("looping")
        config_path = cwd + dir + "\\" + dir + "_cfg.xml"
        batch_file_log_path = import_file_log_path + dir + "_log.txt"
        file.write(f"CALL \"{launch_path}\" \"{config_path}\" >> \"{batch_file_log_path}\"\n")
        count += 1
    file.close()
    print("Bat file written as TCC Automation.bat in src")
    #for dir in dirNames:


    




