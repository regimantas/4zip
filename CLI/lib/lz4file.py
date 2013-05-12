#!/usr/bin/env python

import lz4, zlib, os, os.path, shutil, threading
from glob import glob
import zipfile

class lz4o:

  def read_in_chunks(self, file_object, chunk_size):
      """Lazy function (generator) to read a file piece by piece.
      Default chunk size: 1k. 1024, 1m 1048576, 1g 1073741824"""
      while True:
          data = file_object.read(chunk_size)
          if not data:
              break
          yield data

  def CompressFile(self, Name, OutName, f):
    try:
      f2 = open(Name,'rb')
    except:
      return
    if os.stat(Name).st_size < 1073741824:
      data = f2.read()
      try:
        f.writestr(OutName, lz4.dumps(data))
      except:
        f.write(lz4.dumps(data))
    else:
      OutName_tmp = OutName.replace(os.path.basename(OutName),"")
      OutName = OutName_tmp+"@@"+os.path.basename(OutName)+"/"
      del OutName_tmp
      xpart = 0
      for piece in lz4o().read_in_chunks(f2, 104857600):
        f.writestr(OutName+str(xpart), lz4.dumps(piece))
        xpart += 1
    f2.close()

  
  def Decompress(self, Name, output_path="", data_lst=""):
    if output_path != "":
      os.chdir(output_path)
    if os.path.isdir(output_path):
      output_name = output_path+'/'+os.path.basename(Name.replace(".lz4",""))
    elif output_path == "":
      output_name = Name.replace(".lz4","")
    else:
      output_name = Name.replace(".lz4","")

    if zipfile.is_zipfile(Name) == False:
      f = open(output_name, "wb")
      f2 = open(Name,'rb')
      data = f2.read()
      f.write(lz4.loads(data))
      f.close()
      f2.close()
    else:
      f = zipfile.ZipFile(Name, 'r')
      for fname in f.namelist():
        if data_lst != "":
          if fname.find(data_lst) != -1:
            pass
          else:
            continue
        if fname.find("@@") != -1:
          larg_file_name = '/'+os.path.basename(fname)
          larg_file_name = fname.replace(larg_file_name,"").replace("@@","")
          try:
            extrakt_dir = larg_file_name.replace(os.path.basename(larg_file_name),"")
            os.makedirs(extrakt_dir)
          except:
            if os.path.exists(extrakt_dir):
              pass
            else:
              raise
          data = f.read(fname)
          f2 = open(larg_file_name,'ab')
          f2.write(lz4.loads(data))
          f2.close()
        else:
          try:
            extrakt_dir = fname.replace(os.path.basename(fname),"")
            os.makedirs(extrakt_dir)
          except:
            if os.path.exists(extrakt_dir):
              pass
            else:
              raise
          f2 = open(fname,'wb')
          #print fname
          data = f.read(fname)
          f2.write(lz4.loads(data))
          f2.close()
      f.close()

  def Compress(self, Name, output_path="", MakeFile=""):
    if os.path.isdir(output_path):
      outpu_name = output_path+"/"+os.path.basename(Name)+".lz4"
    elif output_path == "":
      outpu_name = Name+".lz4"
    else:
      outpu_name = Name+".lz4"
    
    if output_path == "" and MakeFile != "":
      outpu_name = MakeFile

    if os.path.isfile(Name):
      if os.stat(Name).st_size < 1073741824:
        f = open(outpu_name, "wb")
        self.CompressFile(Name, outpu_name, f)
      else:
        f = zipfile.ZipFile(outpu_name, mode='w', compression=zipfile.ZIP_STORED)
        self.CompressFile(Name, Name+".lz4", f)
    elif os.path.isdir(Name):
      f = zipfile.ZipFile(outpu_name, mode='w', compression=zipfile.ZIP_STORED)

      fname = os.path.basename(Name)+"/"

      start_dir = Name
      pattern   = "*"
      #print os.path.relpath(start_dir)
      for dir,_,_ in os.walk(start_dir):
          Filesx = glob(os.path.join(dir,pattern))
          for Filex in Filesx:
            #print fname+os.path.relpath(Filex, start_dir)
            self.CompressFile(Filex, fname+os.path.relpath(Filex, start_dir), f)
            #print os.path.abspath(Filex).replace(Name,'#'+Name)
            #quit()
    f.close()

  def Files_List(self, Name):
     File_List = []
     Black_File_List = []
     if zipfile.is_zipfile(Name) == True:
       f = zipfile.ZipFile(Name, 'r')
       for fname in f.namelist():
         if fname.find("@@") > -1:
           tname  = fname.replace("/"+os.path.basename(fname),"")
           if not tname in Black_File_List:     
             File_List.append(tname.replace("@@",""))
             Black_File_List.append(tname)
         else:
           File_List.append(fname)
     else:
       File_List.append(os.path.basename(Name))
     return File_List

#SuperFastCompression().Compress("/home/chaosas/Darbastalis/a10")
#SuperFastCompression().Compress("/home/chaosas/Darbastalis/a10/image/linaro-alip-armhf-t4.img", "/home/chaosas/Darbastalis/compression")
#SuperFastCompression().Decompress("/home/chaosas/Darbastalis/compression/linaro-alip-armhf-t4.img.lz4", "/home/chaosas/DB")
