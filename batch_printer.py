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



class printer:

    def __init__(self):
        pass

    def print_file(self, path, copies):
        filename = path
        for copy in range(copies):
            
            win32api.ShellExecute (
              0,
              "print",
              filename,
              None,
              ".",
              0
            )
            time.sleep(10)

    def print_file_gs(self, path, copies):

        p = subprocess.Popen(["C:\Program Files\Ghostgum\gsview\gsprint.exe", "-landscape", "-copies", str(copies), path], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print stdout
        print stderr

    def get_list_with_copies(self, input_list):
                                                                       
        output_list = []

        i = 0
                                                    
        while i < len(input_list):
            
            copies = 1
            count = 1
            if i != len(input_list) - 1:
                while input_list[i] == input_list[i + 1]:
                    copies = copies + 1
                    i = i + 1

            output_list.append((input_list[i], copies))
            i = i + 1

        return output_list

    def print_all(self, file_list):
        copy_list = self.get_list_with_copies(file_list)

        
        number_of_copies = len(copy_list)
        current_copy = 1
        for file in copy_list:
            print "Printing file " + str(current_copy) + " out of " + str(number_of_copies)
            self.print_file_gs(file[0], file[1])
            current_copy = current_copy + 1
        
        
class windows_api:

    def __init__(self):
        pass

    def open_file(self, filename):
        try:
            os.startfile(filename)
        except AttributeError:
            call(['open', filename])


                                                           
root_directory = ""
pdf_crawler = crawler(root_directory)
pdf_crawler.crawl()
file_list_object = file_list(pdf_crawler.master_file_list)


while True:
    input_files = []
    print "Paste drawings to print: "
    #print "Paste drawings to open: "

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
        matching_files_list.append(matching_files[-1])

    print "Found these matches as latest revisions:"
    for item in matching_files_list: print item

    matching_file_paths = []

    for item in matching_files_list:
        matching_file_paths.append(file_list_object.get_path(item))

    #print matching_file_paths

    printy = printer()

    windows = windows_api()

    #printy.print_all(matching_file_paths)


    


    print "Opening..."
    for patho in matching_file_paths:
        time.sleep(1)
        windows.open_file(patho)
                                              
                                                









                                                                   
