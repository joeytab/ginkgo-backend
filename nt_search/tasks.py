from celery import Celery
import sys, os 
sys.path.append(os.path.dirname(__file__))
from align import searchSeq

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def get_alignments(sequence):
    return searchSeq(sequence)