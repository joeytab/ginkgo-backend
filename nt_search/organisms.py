import Bio.Align as algn 
import Bio.Entrez as ent
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
genomes = ["NC_000852", "NC_007346", "NC_008724", "NC_009899", "NC_014637", "NC_020104", "NC_023423", "NC_023640", "NC_023719",
"NC_027867"]
ent.email="jbanerje@caltech.edu"
organisms = []
for g in genomes:
    handle = ent.efetch(db ="nucleotide", id = g, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    name = record.description.split(',')[0]
    organisms.append(name)
    print(name)
