import csv, subprocess, re
import sys

class Main(object):
    def __init__(self, csv_file = "RunLanePlexByProject.csv"):
        self.samples = self.load_csv(csv_file)
        for sample in self.samples:
            self.samples[sample]["IRODS_BAM_PATH"] = "/seq/%(RUN_ID)s/%(RUN_ID)s_%(LANE)s.bam"%self.samples[sample]
            self.samples[sample]["IRODS_CRAM_PATH"] = "/seq/%(RUN_ID)s/%(RUN_ID)s_%(LANE)s.cram"%self.samples[sample]
            self.samples[sample]["IRODS_PATH"] = self.get_irods_path(sample)
            self.iget_file(self.samples[sample]["IRODS_PATH"], sample)
            print self.samples[sample]["IRODS_PATH"]
            sys.exit()
        #print self.samples

    def get_irods_path(self, sample, prefer = "BAM"):
        cmd = "ils %s"%(self.samples[sample]["IRODS_%s_PATH"%prefer])
        if self.run_script(cmd)[0]: #Was there any standard output?
            return self.samples[sample]["IRODS_%s_PATH"%prefer]
        return self.samples[sample]["IRODS_%s_PATH"%{"BAM":"CRAM", "CRAM":"BAM"}[prefer]]

    def iget_file(self, filename, save_name):
        cmd = "bsub -J irods -o irods.o -e irods.e -R 'select[cgp_irods>16] rusage[cgp_irods=16]' /software/irods/icommands/bin/iget %s ./irods_get/%s.bam"%(filename, save_name)
        stdout = self.run_script(cmd)[0]
        job_id = int(re.findall("<(.+?)>", stdout)[0])
        print job_id
    
    def run_script(self, cmd):
        sub = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        return sub.communicate()


    def load_csv(self, csv_filename):
        csv_file = open(csv_filename)
        reader = csv.DictReader(csv_file)
        rtn = {i["SAMPLE_SYNONYM"]:i for i in list(reader)}
        csv_file.close()
        return rtn

if __name__ == "__main__":
    Main()


