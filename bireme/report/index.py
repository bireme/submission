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
    center=fields.TEXT(stored=True),
    
    type=fields.TEXT(stored=True),
    current_status=fields.TEXT(stored=True),    
    
    bibliographic_type=fields.TEXT(stored=True),
    total_records=fields.NUMERIC(stored=True),
    certified=fields.NUMERIC(stored=True),
    lildbi_version=fields.TEXT(stored=True),
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
    
    if not type == "NoneType":
    
        submission = instance.submission
        current_status = submission.current_status
        type_submission = instance
        
        if type == "FollowUp":
            type_submission = TypeSubmission.objects.get(submission=submission)
            current_status = instance.current_status

        document = {}

        fields = ['created', 'updated']
        for field in fields:
            if hasattr(submission, field):
                attr = getattr(submission, field)
                if attr:
                    document[field] = attr

        fields = ['id', 'creator', 'updater', 'type']
        for field in fields:
            if hasattr(submission, field):
                attr = getattr(submission, field)
                if attr:
                    attr = unicode(attr)
                    document[field] = attr

        fields = ['total_records', 'certified', 'lildbi_version', 'bibliographic_type']
        for field in fields:
            if hasattr(type_submission, field):
                
                attr = getattr(type_submission, field)

                if attr:
                    if not isinstance(attr, int):
                        attr = unicode(attr)
                    document[field] = attr

        if current_status:
            document['current_status'] = unicode(current_status)

        if submission.creator.get_profile().center.code:
            document['center'] = submission.creator.get_profile().center.code
        
        # Daqui para baixo é padrão, não necessita alterar nada    
        # reading the index
        ix = index.open_dir(settings.WHOOSH_INDEX)
        
        # creating the writer object
        writer = ix.writer()
        writer.update_document(**document)

        writer.commit() 

def delete(sender, instance, **kwargs):

    type = instance.__class__.__name__    
    
    if not type == "NoneType":
    
        submission = instance.submission

        ix = index.open_dir(settings.WHOOSH_INDEX)

        writer = ix.writer()
        writer.delete_by_term('id', submission.id)

        writer.commit() 
        
    
signals.post_save.connect(update_index, sender=FollowUp)
signals.post_save.connect(update_index, sender=TypeSubmission)
signals.pre_delete.connect(delete, sender=TypeSubmission)