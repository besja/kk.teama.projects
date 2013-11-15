from zope.interface import implements
from zope.component import adapts
from AccessControl import ClassSecurityInfo 
from Products.CMFCore.permissions import View
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import file
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from kk.teama.projects.interfaces import IVideo
from kk.teama.projects.config import PROJECTNAME

from plone.app.blob.field import  ImageField as BlobImageField, FileField as BlobFileField

from Products.validation import V_REQUIRED

from Products.validation.interfaces import ivalidator
from Products.validation import validation
import mimetypes

class VideoValidator:
    implements(ivalidator)
    def __init__(self, name):
        self.name = name
    def __call__(self, value, *args, **kwargs):

        filename =  getattr(value, "filename")
        t = filename.split(".") 
        ext = t[-1].lower()
        if ext != 'flv':
            return ("Validation failed: file is not FLV ")
        return 1
        
validation.register(VideoValidator('isVideo'))

FileSchema = file.ATFileSchema.copy()
del(FileSchema['file'])
VideoSchema = FileSchema + Schema((
    BlobFileField('file',
              required=True,
              primary=True,
              searchable=True,
              validators = (('isNonEmptyFile', V_REQUIRED),
                             ('checkFileMaxSize', V_REQUIRED), ('isVideo')),
              widget = FileWidget(
                        description = '',
                        label="File",
                        show_content_type = False,)
        		),
  
    BlobImageField('image',
    			required = True,
                  widget=ImageWidget(label='Clip',
                                          description=''),
                  ),
))



class Video(file.ATFile):
    """ video """
    schema = VideoSchema
    implements(IVideo)
    portal_type=meta_type="Video"
    security = ClassSecurityInfo() 
    security.declareProtected(View, 'tag') 
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.Title()
        return self.getField('image').tag(self, **kwargs)    

registerType(Video, PROJECTNAME)
