from zope.interface import implements
from zope.component import adapts
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from kk.teama.projects.interfaces import IProjectCategoryFolder
from kk.teama.projects.config import PROJECTNAME
from Products.ATContentTypes.configuration import zconf

class ProjectCategoryFolder(folder.ATFolder):
    """ category folder """
    
    implements(IProjectCategoryFolder)
    portal_type=meta_type="ProjectCategoryFolder"
    

registerType(ProjectCategoryFolder, PROJECTNAME)