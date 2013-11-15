from zope.interface import implements
from zope.component import adapts
from AccessControl import ClassSecurityInfo 
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document, image
from Products.ATContentTypes.content.base import ATCTFileContent
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.image import ATCTImageTransform

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from kk.teama.projects.interfaces import IProject
from kk.teama.projects.config import PROJECTNAME
from Products.ATContentTypes.configuration import zconf
from plone.app.blob.field import  ImageField as BlobImageField
from Products.CMFCore.permissions import View
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName


ProjectSchema = folder.ATFolderSchema.copy()  + Schema((
    ReferenceField('categories', 
    				required=True, 
     			    allowed_types=('ProjectCategoryFolder'), 
    			    multiValued = True, 
    			    vocabulary = "getCategoriesValues", 
    			    relationship="project_categories",  				
    				widget=ReferenceWidget(label="Categories")), 
    
    BlobImageField('image',
    			required = True,
                widget=ImageWidget(label='An image',
                                          description='Some image'),
                  ),

    TextField('text',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              #validators = ('isTidyHtml',),
              default_output_type = 'text/x-html-safe',
              widget = RichWidget(
                        description = '',
                        label = 'label_body_text',
                        rows = 25,
                        allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),  
    DateTimeField("project_date", 
    required=True,
    default = DateTime(),
 
    widget=CalendarWidget(label="Project date", 
    					  starting_year=1980,
					      ending_year = 2020, 
						  show_hm = False)
    
    ),
        
    BooleanField('tableContents',
        required = False,
        languageIndependent = True,
        widget = BooleanWidget(
            label= 'help_enable_table_of_contents',
            description = "help_enable_table_of_contents_description"
            )
    ),                                                  
                                                             
))
#ProjectSchema["subject"].schemata = "default"
#ProjectSchema["subject"].required = True
ProjectSchema["tableContents"].widget.visible = {"edit": "invisible", "view": "invisible"}
class Project(ATCTImageTransform, folder.ATFolder, document.ATDocument):
    """ project """
    schema = ProjectSchema
    implements(IProject)
    portal_type=meta_type="Project"
    security = ClassSecurityInfo()
    
    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.Title()
        return self.getField('image').tag(self, **kwargs)
    
    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATDocumentBase.__bobo_traverse__(self, REQUEST, name)

    def getProjectDate(self):
        date = self.getProject_date()
        prop_tool = getToolByName(self, "portal_properties")
        df = prop_tool.site_properties.getProperty("teama_date_format")
        return date.strftime(df)
    
    def getCategoriesValues(self):
        ptool = getToolByName(self, "portal_catalog")
        cats = [ (i.UID, i.Title) for i in ptool(portal_type="ProjectCategoryFolder") ]
        return DisplayList(tuple(cats))
        
    def getCategoriesIndex(self):
        return [i.UID() for i in self.getCategories()]  
        
    def getCategoriesList(self):
        return ", ".join(["<a href='%s'>%s</a>" % (i.absolute_url(), i.Title()) for i in self.getCategories()])
        
registerType(Project, PROJECTNAME)
