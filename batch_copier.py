import os
from subprocess import check_output, call
import subprocess
import time
import re

import tempfile
import win32api
import win32print

# Loading the pyPdf Library
from pyPdf import PdfFileWriter, PdfFileReader


class crawler:
    
    master_file_list = []
    extension = ".pdf"
    
    def __init__(self, root):
        self.root = root

    def crawl(self, root=None):

        if root == None:
            root = self.root
        
        os.chdir(root)

        current_contents = os.listdir(root)
        #for item in current_contents: print item
        directories = []

        for item in current_contents:
            if os.path.isdir(root + "\\" + item):
                directories.append(item)
                

        if directories != []:  
            for folder in directories:
                self.crawl(root + "\\" + folder)

        pdfs = []
        for item in current_contents:
            if item[-4:] == ".pdf":
                pdfs.append(item)
                
        
        for pdf in pdfs:
            path =  root + "\\" + pdf
            if path not in self.master_file_list:
                self.master_file_list.append(path)

        return


class file_list:

    def __init__(self, file_list):
        self.file_list = file_list

    def search(self, keyword_regex):

        match_list = []

        for file in self.file_list:
            match = re.match(keyword_regex, file.split("\\")[-1])
            if match is not None:
                match_list.append(file.split("\\")[-1])

        return match_list

    def count(self):
        return str(len(self.file_list))

    def get_path(self, file_name):
        for file in self.file_list:
            if file_name in file:
                return file



class windows_api:

    def __init__(self):
        pass

    def open_file(self, filename):
        try:
            os.startfile(filename)
        except AttributeError:
            call(['open', filename])


                                                           
root_directory = "C:\\Users\\wwfield1509\\Desktop\\Drawings"
pdf_crawler = crawler(root_directory)
pdf_crawler.crawl()
file_list_object = file_list(pdf_crawler.master_file_list)
copy_directory = "C:\\Users\\wwfield1509\\Desktop\\folderino"

while True:
    input_files = []
    print "Paste drawings to open: "

    while True:
        line = raw_input()
        if line.strip() == "":
            break
        input_files.append(line)

    matching_files_list = []

    for drawing in input_files:
        regex_query = "("+ drawing + "_).{3,4}.pdf"

        matching_files = file_list_object.search(regex_query)
        matching_files.sort()
        if matching_files != []:
            matching_files_list.append(matching_files[-1])

    print "Found these matches as latest revisions:"
    for item in matching_files_list: print item

    matching_file_paths = []

    for item in matching_files_list:
        matching_file_paths.append(file_list_object.get_path(item))


    windows = windows_api()


    print "Opening..."
    for patho in matching_file_paths:
        command = 'COPY "%s" "%s" ' % (patho, copy_directory + "\\" + patho.split("\\")[-1])
        print "command:"
        print command
        check_output(command, shell=True)

        
                                              
                                                









                                                                   
