import luigi
from luigi import Task, run, LocalTarget
import wget
import tarfile
import os

class DownloadTask(Task):
    
    url = luigi.Parameter(default="https://www.ncbi.nlm.nih.gov/geo/download/?acc=")
    NameDownload = luigi.Parameter(default="GSE68849&format=file")
    dir = luigi.Parameter(default="Root/")
    NameSave = luigi.Parameter(default='RootTAR.tar')
    
    def run(self):
        fileurl = self.url + self.NameDownload
        file_dir = self.dir + self.NameSave
        wget.download(fileurl, file_dir)
        
    def output(self):
        #return luigi.LocalTarget(self.dir + self.NameSave)
        return {'out1': luigi.LocalTarget(self.dir),'out2': luigi.LocalTarget(self.NameSave)}
    
class TempTask(Task):
    def output(self):
        #return luigi.LocalTarget("Root/RootTAR.tar")
        #return {'out1': luigi.LocalTarget('Root/RootTAR.tar'),'out2': 'RootTAR.tar','out3': 'Root/'}
        return {'out1': luigi.LocalTarget('Root/RootTAR.tar')}
        
class UnzipFirstArchive(Task):
    
    #filename = luigi.Parameter()
    #dir = luigi.Parameter()
    
    def requires(self):
        return TempTask()
    
    def run(self):
        file = self.input()['out1'].path
        print(file)
        # file = str(self.input())
        # file_path = file[:file.rfind('/')+1]
        # branch_count=1
        # branch_list = []
        # with tarfile.open(file, 'r') as tar:
        #     #print(tar.getnames())
        #     for i in tar.getnames():
        #         dir_name = str(branch_count) + ' branch'
        #         os.mkdir(file_path + dir_name)
        #         tar.extract(i, file_path + dir_name)
                
        #         branch_list.append(dir_name)
        #         branch_count += 1
    
    def output(self):
        pass
                
class UnzipSecondArchive(Task):
    def requires(self):
        return UnzipFirstArchive()
    
    
if __name__ == '__main__':
    run()