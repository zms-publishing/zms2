################################################################################
# _zmi_actions_util.py
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

# Product imports.
import _globals

def zmi_actions(container, context, attr_id='e'):
  """
  """
  actions = []
  
  REQUEST = container.REQUEST
  if container.meta_id == 'ZMSTrashcan':
    objAttr = {}
  else:
    objAttr = container.getMetaobjAttr( container.meta_id, attr_id)
  objChildren = len(container.getObjChildren(attr_id,REQUEST))
  objPath = ''
  if context is not None and context != container:
    objPath = context.id+'/'
  
  #-- Action: Separator.
  actions.append(('----- %s -----'%container.getZMILangStr('ACTION_SELECT')%container.getZMILangStr('ATTR_ACTION'),''))
  actions.extend(zmi_basic_actions(container, context, objAttr, objChildren, objPath))
  actions.extend(zmi_insert_actions(container, context, objAttr, objChildren, objPath))
  
  # Return action list.
  return actions


def zmi_basic_actions(container, context, objAttr, objChildren, objPath=''):
  """
  Returns sorted list of basic actions (undo, delete, cut, copy, paste, 
  move up/down) and custom commands.
  """
  actions = []
  
  REQUEST = container.REQUEST
  lang = REQUEST['lang']
  auth_user = REQUEST['AUTHENTICATED_USER']
  
  repetitive = objAttr.get('repetitive',0)==1
  mandatory = objAttr.get('mandatory',0)==1
  
  #-- Action: Edit.
  if context is not None:
    actions.append((container.getZMILangStr('BTN_EDIT'),objPath+'manage_main'))
    if context.getLevel() > 0:
      if repetitive or not mandatory:
        #-- Action: Undo.
        can_undo = context.inObjStates( [ 'STATE_NEW', 'STATE_MODIFIED', 'STATE_DELETED'], REQUEST)
        if can_undo:
          actions.append((container.getZMILangStr('BTN_UNDO'),'manage_undoObjs'))
        #-- Action: Delete.
        if context.getParentByLevel(1).meta_id == 'ZMSTrashcan':
          actions.append((container.getZMILangStr('BTN_DELETE'),'manage_eraseObjs'))
        else:
          can_delete = not context.inObjStates( [ 'STATE_DELETED'], REQUEST) and context.getAutocommit() or context.getDCCoverage(REQUEST).endswith('.'+lang)
          if can_delete:
            ob_access = context.getObjProperty('manage_access',REQUEST)
            can_delete = can_delete and ((not type(ob_access) is dict) or (ob_access.get( 'delete') is None) or (len( container.intersection_list( ob_access.get( 'delete'), context.getUserRoles(auth_user))) > 0))
            metaObj = container.getMetaobj( context.meta_id)
            can_delete = can_delete and ((metaObj.get( 'access') is None) or (metaObj.get( 'access', {}).get( 'delete') is None) or (len( container.intersection_list( metaObj.get( 'access').get( 'delete'), context.getUserRoles(auth_user))) > 0))
          if can_delete:
            actions.append((container.getZMILangStr('BTN_DELETE'),'manage_deleteObjs'))
        #-- Action: Cut.
        can_cut = not context.inObjStates( [ 'STATE_DELETED'], REQUEST) and context.getAutocommit() or context.getDCCoverage(REQUEST).endswith('.'+lang)
        if can_cut:
          actions.append((container.getZMILangStr('BTN_CUT'),'manage_cutObjects')) 
      #-- Action: Copy.
      actions.append((container.getZMILangStr('BTN_COPY'),'manage_copyObjects'))
      #-- Actions: Move.
      can_move = objChildren > 1
      if can_move:
        actions.append((container.getZMILangStr('ACTION_MOVEUP'),objPath+'manage_moveObjUp'))
        actions.append((container.getZMILangStr('ACTION_MOVEDOWN'),objPath+'manage_moveObjDown'))
  
  #-- Action: Paste.
  if repetitive or objChildren==0:
    if container.cb_dataValid():
      if objAttr['type']=='*':
        meta_ids = objAttr['keys']
      else:
        meta_ids = [objAttr['type']]
      append = True
      try:
        for ob in container.cp_get_obs( REQUEST):
          metaObj = ob.getMetaobj( ob.meta_id)
          append = append and (ob.meta_id in meta_ids or 'type(%s)'%metaObj['type'] in meta_ids)
      except:
        append = False
      if append:
        actions.append((container.getZMILangStr('BTN_PASTE'),'manage_pasteObjs'))
  
  #-- Custom Commands.
  actions.extend(zmi_command_actions(context, insert_actions=False, objPath=objPath))
  
  # Return action list.
  return actions


def zmi_insert_actions(container, context, objAttr, objChildren, objPath=''):
  """
  Returns sorted list of insert actions. 
  """
  actions = []
  if container.meta_id == 'ZMSTrashcan':
    return actions
  
  REQUEST = container.REQUEST
  auth_user = REQUEST['AUTHENTICATED_USER']
  absolute_url = '/'.join(list(container.getPhysicalPath())+[''])
  
  repetitive = objAttr.get('repetitive',0)==1
  mandatory = objAttr.get('mandatory',0)==1
  
  #-- Objects.
  if repetitive or len(container.getObjChildren(objAttr['id'],REQUEST))==0:
    metaObjIds = container.getMetaobjIds()
    meta_ids = []
    if objAttr['type']=='*':
      for meta_id in objAttr['keys']:
        if meta_id.startswith('type(') and meta_id.endswith(')'):
          for metaObjId in metaObjIds:
            metaObj = container.getMetaobj( metaObjId)
            if metaObj['type'] == meta_id[5:-1] and metaObj['enabled'] == 1:
              meta_ids.append( metaObj['id'])
        elif objAttr['id']=='e' and meta_id in metaObjIds:
          metaObj = container.getMetaobj( meta_id)
          if metaObj['enabled'] == 1:
            meta_ids.append( meta_id)
        elif meta_id in metaObjIds:
          meta_ids.append( meta_id)
        else:
          _globals.writeError( container, '[zmi_insert_actions]: %s.%s contains invalid meta_id \'%s\''%(container.meta_id,objAttr['id'],meta_id))
    else:
      meta_ids.append( objAttr['type'])
    for meta_id in meta_ids:
      metaObj = container.getMetaobj(meta_id)
      ob_access = True
      ob_manage_access = container.getMetaobjAttr(meta_id,'manage_access',syncTypes=['*'])
      if ob_manage_access is not None:
        try:
          ob_access = _globals.dt_html(container,ob_manage_access['custom'],REQUEST)
        except:
          _globals.writeError( container, '[zmi_insert_actions]: can\'t get manage_access from %s'%meta_id)
      can_insert = True
      if objAttr['type']=='*':
        can_insert = can_insert and ((type(ob_access) is not dict) or (ob_access.get( 'insert') is None) or (len( container.intersection_list( ob_access.get( 'insert'), container.getUserRoles(auth_user))) > 0))
        mo_access = metaObj.get( 'access')
        if type(mo_access) is dict:
          mo_access_insert_roles = mo_access.get('insert')
          if type(mo_access_insert_roles) is list:
            can_insert = can_insert and len( container.intersection_list( mo_access_insert_roles, container.getUserRoles(auth_user))) > 0
          mo_access_insert_nodes = container.string_list(mo_access.get('insert_custom','{$}'))
          sl = []
          sl.extend(map( lambda x: (container.getHome().id+'/content/'+x[2:-1]+'/').replace('//','/'),filter(lambda x: x.find('@')<0,mo_access_insert_nodes)))
          sl.extend(map( lambda x: (x[2:-1].replace('@','/content/')+'/').replace('//','/'),filter(lambda x: x.find('@')>0,mo_access_insert_nodes)))
          can_insert = can_insert and len( filter( lambda x: absolute_url.find(x)>=0, sl)) > 0
      if can_insert:
        if meta_id in container.dGlobalAttrs.keys() and container.dGlobalAttrs[meta_id].has_key('constructor'):
          value = 'manage_addProduct/zms/%s'%container.dGlobalAttrs[meta_id]['constructor']
        elif metaObj['type']=='ZMSModule':
          value = 'manage_addZMSModule'
        elif objAttr['type'] in meta_ids and repetitive and objAttr.get('custom'):
          value = 'manage_addZMSCustomDefault'
        else:
          value = 'manage_addProduct/zms/manage_addzmscustomform'
        action = (container.display_type(REQUEST,meta_id),value,container.display_icon(REQUEST,meta_id))
        if action not in actions:
          actions.append( action)
  
  #-- Insert Commands.
  actions.extend(zmi_command_actions(container, insert_actions=True))
  
  #-- Sort.
  actions.sort()
  
  #-- Headline.
  if len(actions) > 0:
    actions.insert(0,('----- %s -----'%container.getZMILangStr('ACTION_INSERT')%container.display_type(REQUEST),'','icon-plus-sign'))
  
  # Return action list.
  return actions


def zmi_command_actions(context, insert_actions=False, objPath=''):
  """
  Returns list of custom commands.
  """
  actions = []
  if context is None:
    return actions
  
  REQUEST = context.REQUEST
  auth_user = REQUEST['AUTHENTICATED_USER']
  absolute_url = '/'.join(list(context.getPhysicalPath())+[''])
  
  for metaCmdId in context.getMetaCmdIds():
    metaCmd = context.getMetaCmd(metaCmdId)
    if (insert_actions and metaCmd['id'].startswith('manage_add')) or \
       (not insert_actions and not metaCmd['id'].startswith('manage_add')):
      canExecute = True
      if canExecute:
        hasMetaType = context.meta_id in metaCmd['meta_types'] or 'type(%s)'%context.getType() in metaCmd['meta_types']
        canExecute = canExecute and hasMetaType
      if canExecute:
        hasRole = False
        hasRole = hasRole or len(context.intersection_list(context.getUserRoles(auth_user),metaCmd['roles'])) > 0
        hasRole = hasRole or auth_user.has_role('Manager')
        canExecute = canExecute and hasRole
      if canExecute:
        nodes = context.string_list(metaCmd.get('nodes','{$}'))
        sl = []
        sl.extend(map( lambda x: (context.getHome().id+'/content/'+x[2:-1]+'/').replace('//','/'),filter(lambda x: x.find('@')<0,nodes)))
        sl.extend(map( lambda x: (x[2:-1].replace('@','/content/')+'/').replace('//','/'),filter(lambda x: x.find('@')>0,nodes)))
        hasNode = len( filter( lambda x: absolute_url.find(x)>=0, sl)) > 0
        canExecute = canExecute and hasNode
      if canExecute:
        actions.append((metaCmd['name'],objPath+'manage_executeMetacmd'))
  
  # Return action list.
  return actions

################################################################################