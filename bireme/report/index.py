#! coding: utf-8
import os
from django.db.models import signals
from django.conf import settings
from whoosh import store, fields, index, qparser
from submission.models import *

WHOOSH_SCHEMA = fields.Schema(
    
    id=fields.NUMERIC(stored=True, unique=True),
    created=fields.DATETIME(stored=True),
    creator=fields.TEXT(stored=True),
    updated=fields.DATETIME(stored=True),
    updater=fields.TEXT(stored=True),
    
    type=fields.TEXT(stored=True),
    current_status=fields.TEXT(stored=True),
    observation=fields.TEXT(stored=True),
    
    bibliographic_type=fields.TEXT(stored=True),
    total_records=fields.TEXT(stored=True),
    certified=fields.TEXT(stored=True),
    iso_file=fields.TEXT(stored=True),
    lildbi_version=fields.TEXT(stored=True),
    
    center=fields.TEXT(stored=True),
)

def search(query, field=None, limit=None, sortedby='created', type=None):
    
    query = unicode(query)

    ix = index.open_dir(settings.WHOOSH_INDEX)
    searcher = ix.searcher()

    parser = qparser.QueryParser("id", ix.schema)
    myquery = parser.parse(query)
    
    return searcher.search(myquery, limit=None, sortedby=sortedby)

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        ix = index.create_in(settings.WHOOSH_INDEX, WHOOSH_SCHEMA)
signals.post_syncdb.connect(create_index)

def update_index(sender, instance, created, **kwargs):

    type = instance.__class__.__name__
    
    submission = instance.submission
    current_status = submission.current_status
    type_submission = instance
    
    if type == "FollowUp":
        current_status = instance.current_status

    document = {
        "id": unicode(submission.id),
        "created": submission.created,
        "creator": submission.creator.username,
        "updated": submission.updated,
        "updater": submission.updater.username,
        
        "type": unicode(submission.type),
        "current_status": unicode(current_status),
        "observation": submission.observation,
        "center": unicode(submission.creator.get_profile().center.code),

        "bibliographic_type": unicode(type_submission.bibliographic_type),
    }

    if type_submission.total_records:
        document["total_records"] = type_submission.total_records,

    if type_submission.certified:
        document["certified"] = type_submission.certified,

    if type_submission.certified:
        document["lildbi_version"] = type_submission.lildbi_version,    

    # Daqui para baixo é padrão, não necessita alterar nada    
    # reading the index
    ix = index.open_dir(settings.WHOOSH_INDEX)
    
    # creating the writer object
    writer = ix.writer()
    writer.update_document(**document)

    writer.commit() 

signals.post_save.connect(update_index, sender=FollowUp)
signals.post_save.connect(update_index, sender=TypeSubmission)