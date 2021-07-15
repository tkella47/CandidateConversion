
def decompress(zippath):
        if not os.path.exists(zippath.replace(".zip","")):
            os.mkdir(zippath.replace(".zip",""))
        zipObj = zipfile.ZipFile(zippath,"r")
        zipObj.extractall(zippath.replace(".zip",""))
        zipObj.close()



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


#Create progress bar class.
