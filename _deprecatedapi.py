################################################################################
# _deprecated.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
################################################################################

# Imports.
from App.special_dtml import HTMLFile
import warnings
# Product Imports.
import _globals
import _zreferableitem


# ------------------------------------------------------------------------------
#  getLinkList_ZMSLinkElement:
#
#  Returns list of URLs of links.
# ------------------------------------------------------------------------------
def getLinkList_ZMSLinkElement(self, REQUEST=None, allow_none=0):
  value = []
  ref = self.getObjAttrValue(self.getObjAttr('attr_ref'),REQUEST)
  dct = {}
  dct['dst'] = self.getLinkObj(ref,REQUEST)
  dct['url'] = self.getLinkUrl(ref,REQUEST)
  dct['title'] = self.getObjProperty('title',REQUEST)
  dct['description'] = self.getObjProperty('attr_dc_description',REQUEST)
  dct['internal'] = _zreferableitem.isInternalLink(ref)
  medline = dct['title'].lower()=='medline'
  if medline:
    dct['url'] = _zreferableitem.getMedlineLink(dct['url'])
  if dct['url'] is not None or allow_none:
    value.append(dct)
  return value


################################################################################
################################################################################
###
###   class DeprecatedAPI:
###
################################################################################
################################################################################
class DeprecatedAPI:

  f_bo_area = '' 
  f_eo_area = '' 

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.getTitleimage
  # ----------------------------------------------------------------------------
  def getTitleimage( self, REQUEST): 
    warnings.warn('Using <%s @ %s>.getTitleimage(REQUEST) is deprecated.'
                 ' Use getObjProperty(\'titleimage\',REQUEST) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.getObjProperty('titleimage',REQUEST) 

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.getImage
  # ----------------------------------------------------------------------------
  def getImage(self,REQUEST):
    warnings.warn('Using <%s @ %s>.getImage(REQUEST) is deprecated.'
                 ' Use getObjProperty(\'img\',REQUEST) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.getObjProperty('img',REQUEST)

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.getFile
  # ----------------------------------------------------------------------------
  def getFile(self,REQUEST):
    warnings.warn('Using <%s @ %s>.getFile(REQUEST) is deprecated.'
                 ' Use getObjProperty(\'file\',REQUEST) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.getObjProperty('file',REQUEST)

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.getFormat
  # ----------------------------------------------------------------------------
  def getFormat(self,REQUEST):
    print "[getFormat]: @deprecated: returns \"getObjProperty('format',REQUEST)\" for compatibility reasons!"
    return self.getObjProperty('format',REQUEST)

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.getLinkList: 
  #
  #  Returns list of URLs of links.
  # ----------------------------------------------------------------------------
  def getLinkList(self, REQUEST=None, allow_none=0):
    print "[getLinkList]: @deprecated: use own implementation!"
    
    #-- [ReqBuff]: Fetch buffered value from Http-Request.
    try:
      reqBuffId = 'getLinkList%i'%allow_none
      value = self.fetchReqBuff(reqBuffId,REQUEST)
      return value
    except:
      
      #-- Get value.
      value = []
      if self.meta_id == 'ZMSLinkElement' and self.getObjProperty('align',REQUEST) in ['','NONE']:
        if self.isEmbedded(REQUEST):
          if self.isPage():
            ref_obj = self.getRefObj()
            if ref_obj is not None:
              value.extend( ref_obj.getLinkList( REQUEST, allow_none))
        else:
          value.extend( getLinkList_ZMSLinkElement( self, REQUEST, allow_none))
      else:
        for ob in self.filteredChildNodes(REQUEST,['ZMSFile','ZMSLinkContainer','ZMSLinkElement']):
          if ob.meta_id == 'ZMSLinkContainer':
            for sub_ob in ob.filteredChildNodes(REQUEST,['ZMSLinkElement']):
              value.extend( getLinkList_ZMSLinkElement( sub_ob, REQUEST, allow_none))
          elif ob.meta_id == 'ZMSFile' and ob.getObjProperty('align',REQUEST) in ['','NONE']:
            f = ob.getFile(REQUEST)
            if f:
              dct = {}
              dct['dst'] = ob
              dct['url'] = f.getHref(REQUEST)
              dct['title'] = ob.getTitle(REQUEST)
              dct['description'] = _globals.nvl(ob.getObjProperty('attr_dc_description',REQUEST),'')
              dct['internal'] = 1
              value.append(dct)
          elif ob.meta_id == 'ZMSLinkElement' and ob.getObjProperty('align',REQUEST) in ['','NONE']:
            if not ob.isEmbedded(REQUEST):
              value.extend( getLinkList_ZMSLinkElement( ob, REQUEST, allow_none))
      
      #-- [ReqBuff]: Returns value and stores it in buffer of Http-Request.
      return self.storeReqBuff(reqBuffId,value,REQUEST)

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.meta_id_or_type:
  # ----------------------------------------------------------------------------
  def meta_id_or_type(self):
    print "[meta_id_or_type]: @deprecated: use meta_id!"
    return self.meta_id

  # ----------------------------------------------------------------------------
  #  DeprecatedAPI.absolute_obj_path:
  # ----------------------------------------------------------------------------
  def absolute_obj_path(self):
    print "[absolute_obj_path]: @deprecated!"
    ob = self.getDocumentElement()
    return '%s/%s/'%(ob.aq_parent.id,self.absolute_url()[len(ob.aq_parent.absolute_url())+1:])

  # ----------------------------------------------------------------------------
  # DeprecatedAPI.manage_adZMS*
  # ----------------------------------------------------------------------------
  def manage_addZMSFolder(self, values={}, REQUEST=None):
    print "[manage_addZMSFolder]: @deprecated!"
    return self.manage_addZMSCustom('ZMSFolder',values,REQUEST)
  def manage_addZMSDocument(self, values={}, REQUEST=None):
    print "[manage_addZMSDocument]: @deprecated!"
    return self.manage_addZMSCustom('ZMSDocument',values,REQUEST)
  def manage_addZMSFile(self, values={}, REQUEST=None):
    print "[manage_addZMSFile]: @deprecated!"
    return self.manage_addZMSCustom('ZMSFile',values,REQUEST)
  def manage_addZMSGraphic(self, values={}, REQUEST=None):
    print "[manage_addZMSGraphic]: @deprecated!"
    return self.manage_addZMSCustom('ZMSGraphic',values,REQUEST)
  def manage_addZMSNote(self, values={}, REQUEST=None):
    print "[manage_addZMSNote]: @deprecated!"
    return self.manage_addZMSCustom('ZMSNote',values,REQUEST)
  def manage_addZMSLinkContainer(self, values={}, REQUEST=None):
    print "[manage_addZMSLinkContainer]: @deprecated!"
    return self.manage_addZMSCustom('ZMSLinkContainer',values,REQUEST)
  def manage_addZMSLinkElement(self, values={}, REQUEST=None):
    print "[manage_addZMSLinkElement]: @deprecated!"
    return self.manage_addZMSCustom('ZMSLinkElement',values,REQUEST)
  def manage_addZMSSqlDb(self, values={}, REQUEST=None):
    print "[manage_addZMSSqlDb]: @deprecated!"
    return self.manage_addZMSCustom('ZMSSqlDb',values,REQUEST)
  def manage_addZMSSysFolder(self, values={}, REQUEST=None):
    print "[manage_addZMSSysFolder]: @deprecated!"
    return self.manage_addZMSCustom('ZMSSysFolder',values,REQUEST)
  def manage_addZMSTable(self, values={}, REQUEST=None):
    print "[manage_addZMSTable]: @deprecated!"
    return self.manage_addZMSCustom('ZMSTable',values,REQUEST)
  def manage_addZMSTeaserContainer(self, values={}, REQUEST=None):
    print "[manage_addZMSTeaserContainer]: @deprecated!"
    return self.manage_addZMSCustom('ZMSTeaserContainer',values,REQUEST)
  def manage_addZMSTeaserElement(self, values={}, REQUEST=None):
    print "[manage_addZMSTeaserElement]: @deprecated!"
    return self.manage_addZMSCustom('ZMSTeaserElement',values,REQUEST)
  def manage_addZMSTextarea(self, values={}, REQUEST=None):
    print "[manage_addZMSTextarea]: @deprecated!"
    return self.manage_addZMSCustom('ZMSTextarea',values,REQUEST)

  # --------------------------------------------------------------------------
  #  DeprecatedAPI.pil_img_*:
  # --------------------------------------------------------------------------
  def createThumbnail( self, img, maxdim=100, qual=75):
    """
    Creates thumbnail of given image.
    @param img: Image
    @type img: C{MyImage}
    @param qual: JPEG quality (default: 75)
    @type qual: C{int}
    @return: Thumbnail
    @rtype: C{MyImage}
    """
    warnings.warn('Using <%s @ %s>.createThumbnail(...) is deprecated.'
                 ' Use pilutil().thumbnail(...) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.pilutil().thumbnail( img, maxdim, qual)

  def pil_img_resize( self, img, size, mode='resize', sffx='_thumbnail', qual=75):
    """
    Returns a resized copy of an image. The size argument gives the requested
    size in pixels, as a 2-tuple: (width, height).
    @param img: Image
    @type img: C{MyImage}
    @param size: Size 2-tuple: (width, height)
    @type size: C{tuple}
    @param mode: Mode
    @type mode: C{string}
    @param qual: JPEG quality (default: 75)
    @type qual: C{int}
    @return: Resized image
    @rtype: C{MyImage}
    """
    warnings.warn('Using <%s @ %s>.pil_img_resize(...) is deprecated.'
                 ' Use pilutil().resize(...) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.pilutil().resize( img, size, mode, sffx, qual)

  def pil_img_crop( self, img, box, qual=75):
    """
    Returns a rectangular region from the current image. The box is a 4-tuple 
    defining the left, upper, right, and lower pixel coordinate.
    @param img: Image
    @type img: C{MyImage}
    @param box Box 4-tuple: (left, upper, right, bottom)
    @param qual: JPEG quality (default: 75)      
    @type box: C{tuple}
    @return: Cropped image
    @rtype: C{MyImage}
    """
    warnings.warn('Using <%s @ %s>.pil_img_crop(...) is deprecated.'
                 ' Use pilutil().crop(...) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.pilutil().crop( img, box, qual)

  def pil_img_rotate( self, img, direction, qual=75):
    """
    Returns rotated version of the current image. Direction is a simple string 
    defining either left (=90 degree rotation clockwise), right (-90 degree) or 180.
    @param img: Image
    @type img: C{MyImage}
    @param direction string: left, right, 180
    @param qual: JPEG quality (default: 75)
    @type box: C{string}
    @return: Rotated image
    @rtype: C{MyImage}
    """
    warnings.warn('Using <%s @ %s>.pil_img_rotate(...) is deprecated.'
                 ' Use pilutil().rotate(...) instead.'%(self.meta_id,self.absolute_url()),
                   DeprecationWarning, 
                   stacklevel=2)
    return self.pilutil().rotate( img, direction, qual)

################################################################################
