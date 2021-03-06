################################################################################
# Initialisation file for the ZMS Product for Zope
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
#
################################################################################

"""ZMS Product"""

# Documentation string.
__doc__ = """initialization module."""
# Version string.
__version__ = '0.1'

# Imports.
from zope.component import provideAdapter
from App.Common import package_home
from App.ImageFile import ImageFile
from DateTime.DateTime import DateTime
import ConfigParser
import OFS.misc_
import os
import re
import stat
# Product Imports.
import _globals
import zms
import zmscustom
import zmssqldb
import zmslinkcontainer
import zmslinkelement
import _confmanager
import _multilangmanager
import _mediadb
import _sequence
import _zmsattributecontainer


################################################################################
# Define the initialize() function.
################################################################################

def initialize(context): 
    """Initialize the product."""
    
    try: 
        """Try to register the product."""
        
        context.registerClass(
            zms.ZMS,
            permission = 'Add ZMSs',
            constructors = ( zms.manage_addZMSForm, zms.manage_addZMS),
            container_filter = zms.containerFilter,
            )
        context.registerClass(
            zmscustom.ZMSCustom,
            permission = 'Add ZMSs',
            constructors = (zmscustom.manage_addZMSCustomForm, zmscustom.manage_addZMSCustom),
            container_filter = zmscustom.containerFilter,
            )
        context.registerClass(
            zmssqldb.ZMSSqlDb,
            permission = 'Add ZMSs',
            constructors = (zmssqldb.manage_addZMSSqlDbForm, zmssqldb.manage_addZMSSqlDb),
            container_filter = zmscustom.containerFilter,
            )
        context.registerClass(
            zmslinkcontainer.ZMSLinkContainer,
            permission = 'Add ZMSs',
            constructors = (zmslinkcontainer.manage_addZMSLinkContainer, zmslinkcontainer.manage_addZMSLinkContainer),
            container_filter = zmscustom.containerFilter,
            )
        context.registerClass(
            zmslinkelement.ZMSLinkElement,
            permission = 'Add ZMSs',
            constructors = (zmslinkelement.manage_addZMSLinkElementForm, zmslinkelement.manage_addZMSLinkElement),
            container_filter = zmscustom.containerFilter,
            )
        context.registerClass(
            _mediadb.MediaDb,
            permission = 'Add ZMSs',
            constructors = (_mediadb.manage_addMediaDb, _mediadb.manage_addMediaDb),
            icon = 'www/acl_mediadb.gif',
            container_filter = _mediadb.containerFilter,
            )
        context.registerClass(
            _zmsattributecontainer.ZMSAttributeContainer,
            permission = 'Add ZMSs',
            constructors = (_zmsattributecontainer.manage_addZMSAttributeContainer, _zmsattributecontainer.manage_addZMSAttributeContainer),
            container_filter = _zmsattributecontainer.containerFilter,
            )
        
        # register deprecated classes
        dummy_constructors = (zmscustom.manage_addZMSCustomForm, zmscustom.manage_addZMSCustom,)
        dummy_permission = 'Add ZMSs'
        zms.NoETagAdapter.register()
        
        # automated registration for util
        OFS.misc_.misc_.zms['initutil']=_globals.initutil()
        
        # automated registration of language-dictionary
        OFS.misc_.misc_.zms['langdict']=_multilangmanager.langdict()
        
        # automated registration of configuration
        confdict = _confmanager.ConfDict.get()
        OFS.misc_.misc_.zms['confdict']=confdict
        
        # automated registration for other resources
        for img_path in ['www/']:
          path = package_home(globals()) + os.sep + img_path
          for file in os.listdir(path):
            filepath = path + os.sep + file 
            mode = os.stat(filepath)[stat.ST_MODE]
            if not stat.S_ISDIR(mode):
              registerImage(filepath,file)
        
        # automated combination of external CSS
        gen = confdict.get('zmi.css.gen','').split(',')
        if gen[0] != '':
          print "automated combination of external CSS:",gen
          fileobj = open(translate_path(confdict.get('zmi.all')),'w')
          for key in gen:
            fn = translate_path(confdict.get('zmi.%s'%key))
            fh = open(fn,'r')
            fc = fh.read()
            fh.close()
            s0 = len(fc)
            # Pack
            fc = fc.strip()
            fc = re.sub( '/\*((.|\n|\r|\t)*?)\*/', '', fc)
            while True:
              done = False
              for k in ['=','+','{','}','(',';',',',':']:
                for sk in [' ','\n']:
                  while fc.find(sk+k)>=0:
                    fc=fc.replace(sk+k,k)
                    done = True
                  while k+sk not in [') ','}\n'] and fc.find(k+sk)>=0:
                    fc=fc.replace(k+sk,k)
                    done = True
              d = ['\t','','  ',' ','\n\n','\n',';}','}']
              for i in range(len(d)/2):
                k = d[i*2]
                v = d[i*2+1]
                while fc.find(k) >= 0:
                  fc = fc.replace(k,v)
                  done = True
              if not done:
                break
            s1 = len(fc)
            print "add",fn,"(Packed:",s0,"->",s1,"Bytes)"
            fileobj.write(fc)
          fileobj.close()
        
        # automated generation of language JavaScript
        from xml.dom import minidom
        filename = os.sep.join([package_home(globals())]+['import','_language.xml'])
        print "automated generation of language JavaScript:",filename
        xmldoc = minidom.parse(filename)
        langs = None
        d = {}
        for row in xmldoc.getElementsByTagName('Row'):
          cells = row.getElementsByTagName('Cell')
          if langs is None:
            langs = []
            for cell in cells:
              data = getData(cell)
              if data is not None:
                langs.append(data)
          else:
            l = []
            for cell in cells:
              data = getData(cell)
              if cell.attributes.get('ss:Index') is not None:
                while len(l) < int(cell.attributes['ss:Index'].value) - 1:
                  l.append(None)
              l.append(data)
            if len(l) > 1:
              k = l[0]
              d[k] = {}
              for i in range(len(l)-1):
                d[k][langs[i]] = l[i+1]
        for lang in langs:
          filename = os.sep.join([package_home(globals())]+['plugins','www','i18n','%s.js'%lang])
          print "generate:",filename
          fileobj = open(filename,'w')
          fileobj.write('var zmiLangStr={\'lang\':\'%s\''%lang)
          for k in d.keys():
            v = d[k].get(lang)
            if v is not None:
              v = v.replace('\'','\\\'').replace('\n','\\n')
              fileobj.write(',\'%s\':\''%k)
              fileobj.write(unicode(v).encode('utf-8'))
              fileobj.write('\'')
          fileobj.write('};')
          fileobj.close()
        
        # automated combination of external JavaScript
        for category in ['jquery','bootstrap']:
          gen = confdict.get('%s.libs.gen'%category,'').split(',')
          if gen[0] != '':
            print "%s automated combination of external JavaScript:"%category,gen
            fileobj = open(translate_path(confdict.get('%s.all'%category)),'w')
            for key in gen:
              fn = translate_path(confdict.get(key))
              fh = open(fn,'r')
              fc = fh.read()
              fh.close()
              s0 = len(fc)
              if fn.endswith('.min.js'):
                print "add",fn,"(",s0,"Bytes)"
              else:
                # Pack
                fc = fc.strip()
                fc = re.sub( '/\*(\!|\*|\s)((.|\n|\r|\t)*?)\*/', '', fc)
                fc = re.sub( '//( |-|\$)((.|\r|\t)*?)\n', '', fc)
                while True:
                  done = False
                  for k in ['=','+','-','(',')',';',',',':','&','|']:
                    for sk in [' ','\n']:
                      while fc.find(sk+k)>=0:
                        fc=fc.replace(sk+k,k)
                        done = True
                      while fc.find(k+sk)>=0:
                        fc=fc.replace(k+sk,k)
                        done = True
                  d = ['\t',' ','{ ','{','{\n','{',' }','}',';}','}',',\n',',','\n ','\n','  ',' ','\n\n','\n','}\n}\n','}}\n']
                  for i in range(len(d)/2):
                    k = d[i*2]
                    v = d[i*2+1]
                    while fc.find(k) >= 0:
                      fc = fc.replace(k,v)
                      done = True
                  if not done:
                    break
                s1 = len(fc)
                print "add",fn,"(Packed:",s0,"->",s1,"Bytes)"
              fileobj.write(fc)
            fileobj.close()
    
    except:
        """If you can't register the product, dump error. 
        
        Zope will sometimes provide you with access to "broken product" and
        a backtrace of what went wrong, but not always; I think that only 
        works for errors caught in your main product module. 
        
        This code provides traceback for anything that happened in 
        registerClass(), assuming you're running Zope in debug mode."""
        
        import sys, traceback, string
        type, val, tb = sys.exc_info()
        sys.stderr.write(string.join(traceback.format_exception(type, val, tb), ''))
        del type, val, tb

def getData(cell):
    rc = None
    datas = cell.getElementsByTagName('Data')
    if len(datas) > 0:
        data = datas[0]
        rc = getText(data.childNodes)
    return rc

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def translate_path(s):
  """
  translate path
  """
  ZMS_HOME = package_home(globals())
  if s.startswith('/++resource++zms_/'):
    l = ['plugins','www']+s.split('/')[2:]
  elif s.startswith('/misc_/zms/'):
    l = ['www']+s.split('/')[3:]
  return os.sep.join([ZMS_HOME]+l)

def registerImage(filepath,s):
  """
  manual icon registration
  """
  icon=ImageFile(filepath,globals())
  icon.__roles__ = None
  OFS.misc_.misc_.zms[s]=icon

################################################################################
