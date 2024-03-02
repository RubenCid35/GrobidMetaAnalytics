
from grobid_client.grobid_client import GrobidClient

grobid_client = GrobidClient(config_path="./config/python/config.json")

def main():
    papers = grobid_client.process("processFulltextDocument", "./papers", n=20)
    print(papers)

if '__main__' == __name__: main()