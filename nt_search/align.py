from Bio.Blast import NCBIWWW, NCBIXML
import Bio.Align as algn
import Bio.Entrez as ent
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
import urllib.request,urllib.parse,urllib.error

from rq import Queue
import sys
import os
sys.path.append('../')
sys.path.append(os.path.dirname(__file__))
from worker import conn

q = Queue(connection=conn)

genomes = ["NC_000852", "NC_007346", "NC_008724", "NC_009899", "NC_014637", "NC_020104", "NC_023423", "NC_023640", "NC_023719",
"NC_027867"]
ent.email="jbanerje@caltech.edu"
# organisms = []
# for g in genomes:
#     handle = q.enqueue(ent.efetch, (db ="nucleotide", id = g, rettype="gb", retmode="text"))
#     record = q.enqueue(SeqIO.read(handle, "genbank"))
#     name = record.description.split(',')[0]
#     organisms.append(name)
f = open("/home/jbanerjee02/ginkgo-backend/nt_search/organisms.txt")
organisms = f.read().splitlines()

def print_alignments(blast_record):
    info = dict()
    for alignment in blast_record.alignments:
         for hsp in alignment.hsps:
            if hsp.expect < 0.05:
                info["sequence"] = alignment.title
                info["length"] = alignment.length
                info["e_val"] = hsp.expect
                info["query"] = hsp.query[0:75]
                info["match"] = hsp.match[0:75]
                info["subject"] = hsp.sbjct[0:75]
    return info
def searchSeq(seq):
    print("entered " + seq)
    for name in organisms:
        print("querying " + name)
        try:
            result_handle = NCBIWWW.qblast("blastn", "nt", seq, entrez_query = "\"" + name + "\"[organism]")
        except:
            continue
        print("Parsing query results")
        blast_records = NCBIXML.parse(result_handle)
        print("parsed")
        num_results = 0
        alignments = []
        for blast in blast_records:
            num_results += 1
            alignments.append(print_alignments(blast))
        if(num_results != 0):
            print("return alignments")
            return alignments
    print("No alignments found!")
    return [dict()]



