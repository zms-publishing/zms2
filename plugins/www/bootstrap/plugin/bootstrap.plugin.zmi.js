/*
 * Defaults
 */

String.prototype.removeWhiteSpaces = function() {return(this.replace(/\s+/g,""));};
String.prototype.leftTrim = function() {return(this.replace(/^\s+/,""));};
String.prototype.rightTrim = function() {return(this.replace(/\s+$/,""));};
String.prototype.basicTrim = function() {return(this.replace(/\s+$/,"").replace(/^\s+/,""));};
String.prototype.superTrim = function() {return(this.replace(/\s+/g," ").replace(/\s+$/,"").replace(/^\s+/,""));};
String.prototype.startsWith = function(str) {return (this.match("^"+str)==str)};
String.prototype.endsWith = function(str) {return (this.match(str+"$")==str)};
Array.prototype.indexOf = function(obj) {var i,idx=-1;for(i=0;i<this.length;i++){if(this[i]==obj){idx=i;break;}}return idx;};
Array.prototype.lastIndexOf = function(obj) {this.reverse();var i,idx=-1;for(i=0;i<this.length;i++){if(this[i]==obj){idx=(this.length-1-i);break;}}this.reverse();return idx;};
Array.prototype.contains = function(obj) {var i,listed=false;for(i=0;i<this.length;i++){if(this[i]==obj){listed=true;break;}}return listed;};
var zmiParams = {};

$(function(){
	var href = self.location.href;
	// Parse params (?) and pseudo-params (#).
	var delimiter_list = ['?','#'];
	for (var h = 0; h < delimiter_list.length; h++) {
		var delimiter = delimiter_list[h];
		var i = href.indexOf(delimiter);
		if (i > 0) {
			var query_string = href.substr(i+1);
			if (h < delimiter_list.length-1) {
				i = query_string.indexOf(delimiter_list[h+1]);
				if (i > 0) {
					query_string = query_string.substr(0,i);
				}
			}
			var l = query_string.split('&');
			for ( var j = 0; j < l.length; j++) {
				i = l[j].indexOf('=');
				if (i < 0) {
					break;
				}
				if (typeof zmiParams[l[j].substr(0,i)] == "undefined") {
					zmiParams[l[j].substr(0,i)] = unescape(l[j].substr(i+1));
				}
			}
		}
	}
	// Content-Editable ////////////////////////////////////////////////////////
	if (self.location.href.indexOf('/manage')>0 || self.location.href.indexOf('preview=preview')>0) {
		$('.contentEditable,.zmiRenderShort')
			.mouseover( function(evt) {
				$(this).addClass('preview').addClass('highlight'); 
			})
			.mouseout( function(evt) {
				$(this).removeClass('preview').removeClass('highlight'); 
			})
			.dblclick( function(evt) {
				evt.stopPropagation();
				var href = ""+self.location.href;
				if (href.indexOf('?')>0) {
					href = href.substr(0,href.indexOf('?'));
				}
				if (href.lastIndexOf('/')>0) {
					href = href.substr(0,href.lastIndexOf('/'));
				}
				var lang = null;
				var parents = $(this).parents('.contentEditable');
				for ( var i = 0; i <= parents.length; i++) {
					var pid;
					if ( i==parents.length) {
						pid = $(this).attr('id');
					}
					else {
						pid = $(parents[parents.length-i-1]).attr('id');
					}
					if (pid.length > 0) {
						if (lang == null) {
							lang = pid.substr(pid.lastIndexOf('_')+1);
						}
						pid = pid.substr(pid.indexOf('_')+1);
						if(pid.substr(pid.length-('_'+lang).length)==('_'+lang)) {
							pid = pid.substr(0,pid.length-('_'+lang).length);
						}
						if (!href.endsWith('/'+pid)) {
							href += '/'+pid;
						}
					}
				}
				if (self.location.href.indexOf(href+'/manage_main')==0) {
					href += '/manage_properties';
				}
				else {
					href += '/manage_main';
				}
				if (self.location.href.indexOf('/manage_translate')>0) {
					href += '_iframe';
					href += '?lang='+lang;
					href += '&ZMS_NO_BODY=1';
					zmiIframe(href,{},{});
				}
				else if (self.location.href.indexOf('/manage')>0) {
					href += '?lang='+lang;
					self.location.href = href;
				}
				else {
					href += '_iframe';
					href += '?lang='+lang;
					showFancybox({
						'autoDimensions':false,
						'hideOnOverlayClick':false,
						'href':href,
						'transitionIn':'fade',
						'transitionOut':'fade',
						'type':'iframe',
						'width':819
					});
				}
			})
		.attr( "title", "Double-click to edit!");
	}
	// ZMS plugins
	if (typeof zmiParams['ZMS_HIGHLIGHT'] != 'undefined' && typeof zmiParams[zmiParams['ZMS_HIGHLIGHT']] != 'undefined') {
		$.plugin('zmi_highlight',{
			files: ['/++resource++zms_/jquery/plugin/jquery.plugin.zmi_highlight.js']
			});
		$.plugin('zmi_highlight').get('body',function(){});
	}
	// Form
	$("form.form-horizontal").each(function() {
			if ($("div.zmi-richtext",this).length > 0) {
				$(this).submit(function() {
						zmiRichtextOnSubmitEventHandler();
					});
			}
		});
	// Action-Lists
	$("div.btn-group.zmi-action")
		.focus( function(evt) { zmiActionOver(this,"focus"); })
		.mouseover( function(evt) { zmiActionOver(this,"mouseover"); })
		.mouseout( function(evt) { zmiActionOut(this,"mouseout"); })
		;
	// Inputs
	$(".zmi-image-preview img")
			.attr({title:getZMILangStr('ATTR_IMAGE')+': '+getZMILangStr('BTN_EDIT')})
			.click(function() {
					var html = '<img src="' + $(this).attr("src") + '"/>';
					zmiIframe(html,{},{title:$(this).attr("title")});
				})
			;
});

function zmiWriteDebug(s) {
	var $div = $("div#zmi-debug");
	if ($div.css("display")!="none") {
		$div.html("["+(new Date())+"] "+s+'<br/>'+$div.html());
	}
}

function zmiRelativateUrls(s,page_url) {
	var splitTags = ['<a href="','<img src="'];
	for ( var h = 0; h < splitTags.length; h++) {
	var splitTag = splitTags[h];
		var vSplit = s.split(splitTag);
		var v = vSplit[0];
		for ( var i = 1; i < vSplit.length; i++) {
			var j = vSplit[i].indexOf('"');
			var url = vSplit[i].substring(0,j);
			if (url.indexOf('./')<0) {
				url = zmiRelativateUrl(page_url,url);
			}
			v += splitTag + url + vSplit[i].substring(j);
		}
		s = v;
	}
	return s;
}

function zmiIframe(href, data, opt) {
	if ($("#myModal").length==0) {
		var html = ''
			+ '<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'
				+ '<div class="modal-header">'
					+ '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'
					+ '<h3 id="myModalLabel"></h3>'
				+ '</div>'
				+ '<div class="modal-body">'
				+ '</div>'
				+ '<div class="modal-footer">'
					+ '<button class="btn" data-dismiss="modal" aria-hidden="true">' + getZMILangStr('BTN_CLOSE') + '</button>'
					+ '<button class="btn btn-primary">' + getZMILangStr('BTN_SAVE') + '</button>'
				+ '</div>'
			+ '</div>';
		$('body').append(html);
	}
	if (typeof opt["title"] != "undefined") {
		$("#myModal #myModalLabel").html(opt["title"]);
	}
	if (href.indexOf("<")==0) {
		$("#myModal .modal-body").html(href);
		$("#myModal").modal();
	}
	else {
		$.get( href, data, function(result) {
				var $result = $(result);
				if ($("div#system_msg",$result).length>0) {
					var manage_tabs_message = $("div#system_msg",$result).text();
					manage_tabs_message = manage_tabs_message.substr(0,manage_tabs_message.lastIndexOf("("));
					var href = self.location.href;
					href = href.substr(0,href.indexOf("?"))+"?lang="+getZMILang()+"&manage_tabs_message="+manage_tabs_message;
					self.location.href = href;
				}
				else {
					$("#myModal .modal-body").html(result);
					$("#myModal").modal();
				}
			});
	}
}

// #############################################################################
// ### ZMI Action-Lists
// #############################################################################

/**
 * Populate action-list.
 *
 * @param el
 */
function zmiActionOver(el, evt) {
	$(".split-left",el).css({visibility:"visible"});
	// Populate action-list.
	if($("ul.dropdown-menu",el).length==0) {
		// Set wait-cursor.
		$(document.body).css( "cursor", "wait");
		// Edit action
		$("button.split-left",el).click(function() {
				var btn_group = $(this).parents("div.btn-group.zmi-action");
				var dropdown_menu = $("ul.dropdown-menu",btn_group);
				self.location.href = $("li:first a",dropdown_menu).attr("href");
			});
		// Build action and params.
		var action = self.location.href;
		action = action.substr(0,action.lastIndexOf("/"));
		action += "/manage_ajaxZMIActions";
		var params = {};
		params['lang'] = getZMILang();
		params['context_id'] = typeof $(el).attr("id") == "undefined"?"":$(el).attr("id");
		// JQuery.AJAX.get
		$.get( action, params, function(data) {
			// Reset wait-cursor.
			$(document.body).css( "cursor", "auto");
			// Get object-id.
			var value = eval('('+data+')');
			var id = value['id'].replace(/\./,"_");
			var actions = value['actions'];
			$(el).append('<ul class="dropdown-menu"></ul>');
			for (var i = 1; i < actions.length; i++) {
				var optlabel = actions[i][0];
				var optvalue = actions[i][1];
				$("ul.dropdown-menu",el).append('<li><a href="javascript:zmiActionExecute(\'' + id + '\',\'' + optlabel + '\',\'' + optvalue + '\')">' + optlabel + '</a></li>');
			}
		});
	}
}

function zmiActionOut(el, evt) {
	$(".split-left",el).css({visibility:"hidden"});
}

function zmiActionExecute(id, label, target) {
	if (target.toLowerCase().indexOf('manage_addproduct/')==0 && target.toLowerCase().indexOf('form')>0) {
		// Parameters
		var $el = $(".zmi-action" + (id==''?":first":"#"+id));
		var $fm = $el.parents("form");
		var inputs = $("input:hidden",$fm);
		var data = {custom:label,_sort_id:$(".zmi-sort-id",$el).text()};
		for ( var i = 0; i < inputs.length; i++) {
			var $input = $(inputs[i]);
			var id = $input.attr("id");
			if (jQuery.inArray(id,['form_id','id_prefix','_sort_id','custom','lang','preview'])>=0) {
				data[$input.attr('name')] = $input.val();
			}
		}
		// Show add-dialog.
		zmiIframe(target,data,{
				title:getZMILangStr('BTN_INSERT'),
				close:function(event,ui) {
					$('tr#tr_manage_addProduct').remove();
				}
		});
	}
	else {
		self.location.href = target;
	}
}