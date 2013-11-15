from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements, alsoProvides

from Products.CMFPlone import utils
from Acquisition import aq_inner, aq_base, aq_parent

from zope.viewlet.interfaces import IViewlet
from Products.CMFPlone.interfaces import INonStructuralFolder, IBrowserDefault

from zope.app.component.hooks import getSite
from Products.CMFPlone.Portal import PloneSite
from Products.CMFCore.interfaces import ISiteRoot
from kk.teama.projects.interfaces import IProjectsFolder
import urllib

class NavBarViewlet(ViewletBase):
    implements(IViewlet)

    render = ViewPageTemplateFile('templates/navbar.pt')
    
    navitems = None
    navroot = None
    
    def available(self):
        """Returns true or false depending on of the nav has any results
        """
        if self.navroot:
            return True
        else:
            return False
    
    def update(self):
        """Needed to use the build-in script for finding the selectedTab.
        This script is the one used by the Portal Tabs. 
        """
        self.navroot = self.getAcquisitionChain()

        self.navitems = []
        
        subjects = list(self.context.portal_catalog.uniqueValuesFor('Subject'))
        #subjects.sort()
        if not self.navroot:
            return
        base_url = self.navroot.absolute_url()
        current = self.request.get("category", "")
        tab_class = "plain"
        if current == "":
            tab_class="active"     
        self.navitems.append({'url': base_url, 
                                  'title':"All projects", 
                                  'class':tab_class})        
        for s in subjects:
            tab_class = "plain"
            if s == current:
        	    tab_class = "active"
            self.navitems.append({'url': base_url+"?"+urllib.urlencode({"category":s}), 
                                  'title':s, 
                                  'class':tab_class})
    def getAcquisitionChain(self):
    
        inner = self.context.aq_inner

        iter = inner
        
        result = None
        
        
        while iter is not None:
 
            if IProjectsFolder.providedBy(iter):
                result = iter 
                break

            if not hasattr(iter, "aq_parent"):
                break

            iter = iter.aq_parent
        return result
       