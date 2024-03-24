import luigi
from luigi.util import requires, inherits
from luigi import Task, run, LocalTarget
import wget
import tarfile, gzip, shutil
import os
import pandas as pd
import io

# скачивание файла, в качестве аргументов:
# ссылка на скачивание;
# название файла, который скачивается; путь, куда скачивать файл; 
# имя, под которым сохранить файл 
class DownloadTask(Task):
    
    url = luigi.Parameter(default='https://www.ncbi.nlm.nih.gov/geo/download/?acc=')
    NameDownload = luigi.Parameter(default='GSE68849&format=file')
    dir = luigi.Parameter(default='Root/')
    NameSave = luigi.Parameter(default='Root.tar')
    
    def run(self):
        fileurl = self.url + self.NameDownload
        wget.download(fileurl, self.output().path)
        
    def output(self):
        return luigi.LocalTarget(self.dir + self.NameSave)
        
# распаковка первого архива
@requires(DownloadTask)
class UnzipTar(Task):
    
    def run(self):
        with tarfile.open(self.input().path, 'r') as tar:
            tar.extractall(self.dir)
    
    # возвращаем столько ссылок, сколько файлов содержал архив
    def output(self):
        if os.path.exists(self.dir + self.NameSave):
            result = []
            with tarfile.open(self.input().path, 'r') as tar:
                for i in tar.getnames():
                    result.append(luigi.LocalTarget(self.dir + i))
            return result
  
# распаковка второго уровня архивов
class UnzipGZ(Task):  
    
    file_name = luigi.Parameter()
    dir = luigi.Parameter()
    dir_num = luigi.IntParameter()
    
    def run(self):
        file_dir = self.dir + self.file_name
        with gzip.open(file_dir, 'rb') as f_in:
            dir_name = 'branch' + str(self.dir_num) + '/'
            os.mkdir(self.dir + dir_name)
            archive_name = self.dir + dir_name + self.file_name[:-3]
            with open(archive_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
    def output(self):
        result = self.dir + 'branch' + str(self.dir_num) + '/' + self.file_name[:-3]
        return luigi.LocalTarget(result)
        
# преобразование текста в csv, также внутри вызывается класс распаковки второго уровня архивов
class UnzipTXT(Task):
    
    dir = luigi.Parameter(default='Root/')
    
    # динамичсекий режим запуска распаковки архивов второго уровня
    def requires(self):
        task = []
        j = 0
        for i in os.listdir(self.dir):
            i = str(i)
            if i[-3:] == '.gz':
                params = {'file_name': i, 'dir': self.dir, 'dir_num': j}
                task.append(UnzipGZ(**params))
                j += 1
        return task
    
    def run(self):
        for i in self.input():
            dfs = {}
            # разбиение текстового файла на отдельные csv 
            with open(i.path) as f:
                write_key = None
                fio = io.StringIO()
                for l in f.readlines():
                    if l.startswith('['):
                        if write_key:
                            fio.seek(0)
                            header = None if write_key == 'Heading' else 'infer'
                            dfs[write_key] = pd.read_csv(fio, sep='\t', header=header)
                        fio = io.StringIO()
                        write_key = l.strip('[]\n')
                        continue
                    if write_key:
                        fio.write(l)
                fio.seek(0)
                dfs[write_key] = pd.read_csv(fio, sep='\t')
                
            # сохранение csv
            for table in dfs:
                i_str = str(i)
                table_dir = i_str[:i_str.rfind('/')+1]
                dfs[table].to_csv(table_dir + table + '.csv', index=False)
                
    # возвращаем ссылки на папки branch, посольку именно внутри этого класса вызывается
    # распаковка второго уровня архивов
    def output(self):
        result = []
        for i in os.listdir(self.dir):
            i = str(i)
            if i.startswith('branch'):
                result_str = self.dir + i
                result.append(luigi.LocalTarget(result_str))
                
        return result

# очищение таблиц Probes
# в качестве аргумента можно передать список столбцов на удаление
@requires(UnzipTXT)
class CleanProbes(Task):
    
    clean_list = ['Definition', 'Ontology_Component', 'Ontology_Process', 
                  'Ontology_Function', 'Synonyms', 'Obsolete_Probe_Id', 'Probe_Sequence']
    CleaningList = luigi.Parameter(default=clean_list)
    
    def run(self):
        for i in self.input():
            i = i.path
            for j in os.listdir(i):
                j = str(j)
                if j == 'Probes.csv':
                    df = pd.read_csv(str(i)+'/'+j)
                    df_col = df.columns.tolist()
                    df_col = list(set(df_col) - set(self.CleaningList))
                    df = df[df_col]
                    df.to_csv(str(i)+'/Probes_clean.csv', index=False)
      
    # возвращаем ссылки на все очищенные Probes              
    def output(self):
        result = []
        for i in os.listdir(self.dir):
            i = str(i)
            if i.startswith('branch'):
                result_str = self.dir + i
                result.append(luigi.LocalTarget(result_str +'/Probes_clean.csv'))
                
        return result
    
# удаление лишних файлов
@requires(CleanProbes)
class RemoveRoot(Task):
    
    def run(self):
        os.remove(self.dir + 'Root.tar')
        for i in os.listdir(self.dir):
            i = str(i)
            if i[-3:] == '.gz':
                os.remove(self.dir + i)
            if i.startswith('branch'):
                for j in os.listdir(self.dir + i):
                    j = str(j)
                    if j[-4:] == '.txt':
                        os.remove(self.dir + i + '/' + j)
    
# словарь для тестирования
params_dict = {'url': 'https://www.ncbi.nlm.nih.gov/geo/download/?acc=',
               'NameDownload': 'GSE68849&format=file',
               'dir': 'Root/',
               'NameSave': 'Root.tar'}
    
if __name__ == '__main__':
    run()