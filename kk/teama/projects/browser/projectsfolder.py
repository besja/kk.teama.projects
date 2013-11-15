from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class ProjectsFolderView(BrowserView):
    """ project view """
    __call__ = ViewPageTemplateFile('templates/projectsfolder.pt')
    
    
    def getProjects(self, category = ''):
        
        ptool = getToolByName(self, "portal_catalog")
        
        query = {}
        query["portal_type"] = ["Project"]
        query["sort_on"] = "project_date"
        query["sort_order"] = "descending"
        return ptool(**query)

class ProjectCategoryFolderView(ProjectsFolderView):
    """ project category """ 
    __call__ = ViewPageTemplateFile('templates/projectsfolder.pt')

    def getProjects(self, category = ''):
        
        ptool = getToolByName(self, "portal_catalog")
        uid = self.context.UID()
        query = {}
        query["portal_type"] = ["Project"]
        query["sort_on"] = "project_date"
        query["sort_order"] = "descending"
        query['project_categories'] = uid
        return ptool(**query)