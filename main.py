import csv, json

class Main(object):
    def __init__(self, csv_file = "RunLanePlexByProject.csv"):
        rows = self.load_csv(csv_file)
        for row in rows:
            rows[row]["IRODS_PATH"] = "/seq/%(RUN_ID)s/%(RUN_ID)s_%(LANE)s.bam"%rows[row]
        print rows

    def load_csv(self, csv_filename):
        csv_file = open(csv_filename)
        reader = csv.DictReader(csv_file)
        rtn = {i["SAMPLE_SYNONYM"]:i for i in list(reader)}
        csv_file.close()
        return rtn

if __name__ == "__main__":
    Main()


