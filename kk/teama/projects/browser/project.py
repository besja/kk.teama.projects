from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class ProjectView(BrowserView):
    """ project view """
    __call__ = ViewPageTemplateFile('templates/project.pt')
  
    def getMedia(self):
   
        ptool = getToolByName(self, "portal_catalog")
        putils = getToolByName(self, "plone_utils")
        query = {}
        query["portal_type"] = ["Image", "Video"]
        query["sort_on"] = "getObjPositionInParent"
        if self.context.getImagesOrder(): 
            query["sort_order"] = "reverse"
        query["path"] = "/".join(self.context.getPhysicalPath())
        media = ptool(**query)
        result = []
        for m in media:
           obj = m.getObject()
           portal_type = putils.normalizeString(m.portal_type)
           if portal_type == "video":
               url = obj.absolute_url()
           else:
               url = obj.absolute_url() + "/image_preview"
           result.append ({
           		"url":url, 
           		"class": portal_type, 
           		"obj": obj
           
           })
           		
           
        return result