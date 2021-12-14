# ginkgo-backend
A prototype of a DNA alignment tool that searches specified genomes. The dynamic site can be run by pulling this repository and using python manage.py runserver for the backend and npm run build and npm start for the frontend. The static site can be viewed at: https://joeytab.github.io/ginkgo-project/

This service is built using django and react. This respository contains only the backend, which is hosted through pythonanywhere.com. 

The backend uses BioPython to query Blast for performing the alignments given the set of genomes to search.

### Newly Added/Updated Features
* The startup speed of the application is now increased by moving converting accession IDs to organism names to a separate script, that will only be run once. 
* requirements.txt is modified to resolve dependency issues 
* a worker queue is created to run async operations and place less pressure on the backend server
* the tool now uses redisLite, which is compatible with pythonanywhere

### Design Considerations
I chose to use NCBI's Blast tool, which involves querying the blast server. I acknowledge that this approach then causes the searches to take more time, but I chose this approach anyway for the following reasons 
* Given a DNA sequence, without knowing the open reading frame, it is impossible to know which of the DNA will actually be in the protein sequence. Querying an arbitrary DNA sequence against each genome would not provide much useful information. 
* Alternative splicing of DNA sequences (processing DNA for removal of exons and other regulatory regions) means that even knowing the start position of the nucleotide sequence, not all of the DNA in between is actually included. 
* Blast allows finding inexact matches. If we are attempting to query a sequence of interest to a list of organisms, there is a high chance of mutations or small sequencing errors, so we would want to determine similarity thresholds between matches rather than only finding exact matches. 
* Exact matches of DNA sequences are extremely rare, and even if they occur, given the variability in DNA processing, the match might not necessarily mean anything. Blast takes into account alternative reading frames and splicing variants, providing more useful information about whether the sequence matches an organism/gene.
            
