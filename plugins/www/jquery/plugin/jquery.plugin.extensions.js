/*
 * @see http://nicolas.rudas.info/jQuery/getPlugin/
 */

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
	if (typeof zmiParams['zmi-debug'] != "undefined") {
		zmiToggleDebug(true);
	}

	zmiWriteDebug("BO jquery.plugin.extensions");

	// Content-Editable ////////////////////////////////////////////////////////
	if (self.location.href.indexOf('/manage')>0 || self.location.href.indexOf('preview=preview')>0) {
		$('.contentEditable,.zmiRenderShort')
			.mouseover( function(evt) {
				$(this).addClass('preview').addClass('highlight'); 
			})
			.mouseout( function(evt) {
				$(this).removeClass('preview').removeClass('highlight'); 
			})
			.click( function(evt) {
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
						var $el = $(parents[parents.length-i-1]);
						if ($el.hasClass("portalClient")) {
							if (href.lastIndexOf('/')>0) {
								href = href.substr(0,href.lastIndexOf('/'));
							}
						}
						pid = $el.attr('id');
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
		.attr( "title", "Click to edit!");
	}
	// ZMS plugins
	if (typeof zmiParams['ZMS_HIGHLIGHT'] != 'undefined' && typeof zmiParams[zmiParams['ZMS_HIGHLIGHT']] != 'undefined') {
		$.plugin('zmi_highlight',{
			files: ['/++resource++zms_/jquery/plugin/jquery.plugin.zmi_highlight.js']
			});
		$.plugin('zmi_highlight').get('body',function(){});
	}

	zmiWriteDebug("EO jquery.plugin.extensions");

});


/**
 * Debug
 */
function zmiToggleDebug(b) {
	var $div = $("div#zmi-debug");
	if ($div.length==0) {
		$("body").append('<div id="zmi-debug"></div>');
		$div = $("div#zmi-debug");
	}
	if (b) {
		$div.css("display","block");
	}
	else {
		$div.css("display","none");
	}
}
function zmiWriteDebug(s) {
	var $div = $("div#zmi-debug");
	if ($div.css("display")!="none") {
		var d = new Date();
		$div.html("<code>["+(d)+'...'+(d.getMilliseconds())+"] "+s+'</code><br/>'+$div.html());
	}
}

/**
 * jQuery UI
 * @see http://jqueryui.com
 */
$(function(){
	$('body.zmi').each(function(){
		initUI(this);
	});
});

function initUI(context) {
	// Icons:
	// hover states on the static widgets
	$('ul#icons li,ul.zmi-icons li,div.zmi-icon',context).hover(
		function() {
			if ($(this).hasClass('ui-state-default')) {
				$(this).addClass('ui-state-hover');
			}
		},
		function() {
			if ($(this).hasClass('ui-state-default')) {
				$(this).removeClass('ui-state-hover');
			}
		}
	);
  // Url-Picker
	$("input.url-input",context).each(function() {
			var enabled = true; // @TODO
			var fmName = $(this).parents("form").attr("name");
			var elName = $(this).attr("name");
			$(this).after(''
					+ '<div class="zmi-icon ui-widget ui-helper-clearfix ui-corner-all ui-state-default" style="float:left">'
						+ '<span class="ui-icon ui-icon-newwin" onclick="return zmiBrowseObjs(\'' + fmName + '\',\'' + elName + '\',getZMILang())"></span>'
					+ '</div>'
				);
		});
	pluginUIDatepicker('input.datepicker,input.datetimepicker',function(){
		// Date-Picker
		$.datepicker.setDefaults( $.datepicker.regional[ pluginLanguage()]);
		$('input.datepicker',context).datepicker({
				showWeek: true
			});
		$('input.datetimepicker',context).datepicker({
				constrainInput: false,
				showWeek: true,
				beforeShow: function(input, inst) {
						var e = '';
						var v = $(input).val();
						var i = v.indexOf(' ');
						if ( i > 0) {
							e = v.substr(i+1);
							v = v.substr(0,i);
						}
						$(inst).data("inputfield",input);
						$(inst).data("extra",e);
					},
				onClose: function(dateText, inst) {
						if (dateText) {
							var e = $(inst).data("extra");
							var input = $(inst).data("inputfield");
							var v = $(input).val();
							var i = v.indexOf(' ');
							if ( i < 0 && e) {
								$(input).val(v+' '+e);
							}
						}
					}
			});
	});
	return context;
}

function pluginLanguage() {
	return getZMILangStr('LOCALE',{'nocache':""+new Date()});
}

function pluginUIDatepicker(s, c) {
	var lang = pluginLanguage();
	$.plugin('ui_datepicker',{
		files: [
				'/++resource++zms_/jquery/ui/i18n/jquery.ui.datepicker-'+lang+'.js'
		]});
	$.plugin('ui_datepicker').get(s,c);
}

function zmiAutocompleteDefaultFormatter(l, q) {
	return $.map(l,function(x){
		var label = x;
		var value = x;
		if (typeof x == "object") {
			label = x.label;
			value = x.value;
		}
		var orig = label;
		return {label: label.replace(
								new RegExp(
										"(?![^&;]+;)(?!<[^<>]*)(" +
										$.ui.autocomplete.escapeRegex(q) +
										")(?![^<>]*>)(?![^&;]+;)", "gi"
										), "<strong>$1</strong>" ),
				value: value,
				orig: label};
			})
}

function zmiAutocomplete(s, o) {
	$(s).autocomplete(o)
	.data( "autocomplete" )._renderItem = function( ul, item ) {
			return $( "<li></li>" )
				.data( "item.autocomplete", item )
				.append( "<a>" + item.label + "</a>" )
				.appendTo( ul );
	};
}


/**
 * Fancybox
 * @see http://fancybox.net/
 */
var pluginFancyboxDefaultOptions = {
			'autoScale'		: false,
			'titleShow'		: false,
			'hideOnContentClick': true,
			'transitionIn'	: 'elastic',
			'transitionOut'	: 'elastic'
		};

$(function(){
	$('a.fancybox')
		.click(function() {
			pluginFancyboxDefaultOptions['href'] = $(this).attr('href');
			// Ensure that this link will be opened as an image!
			if ($("img.img",this).length==1) {
				pluginFancyboxDefaultOptions['type'] = 'image';
			}
			return showFancybox(pluginFancyboxDefaultOptions);
		});
});

function pluginFancybox(s, c) {
	$.plugin('fancybox',{
		files: ['/++resource++zms_/jquery/fancybox/jquery.easing-1.3.pack.js',
				'/++resource++zms_/jquery/fancybox/jquery.mousewheel-3.0.4.pack.js',
				'/++resource++zms_/jquery/fancybox/jquery.fancybox-1.3.4.pack.js',
				'/++resource++zms_/jquery/fancybox/jquery.fancybox-1.3.4.css']
		});
	$.plugin('fancybox').get(s,c);
}

function showFancybox(p) {
	pluginFancybox('body',function() {
		$.fancybox(p);
		try {
			$("#fancybox-wrap").draggable();
		}
		catch(e) {
		}
	});
	return false;
}


/**
 * Autocomplete
 * @see http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/
 * @deprecated
 */
function pluginAutocomplete(s, c) {
	$.plugin('autocomplete',{
		files: ['/++resource++zms_/jquery/autocomplete/jquery.bgiframe.min.js',
				'/++resource++zms_/jquery/autocomplete/jquery.autocomplete.min.js',
				'/++resource++zms_/jquery/autocomplete/jquery.autocomplete.css']
	});
	$.plugin('autocomplete').get(s,c);
}


/**
 * jQuery Editable Combobox (jEC)
 * @see http://code.google.com/p/jquery-jec/
 */
function pluginJEC(s, c) {
	$.plugin('jec',{
		files: ['/++resource++zms_/jquery/jec/jquery.jec.min-0.5.2.js']
	});
	$.plugin('jec').get(s,c);
}


/**
 * Jcrop - the jQuery Image Cropping Plugin
 * @see http://deepliquid.com/content/Jcrop.html
 */
function runPluginJcrop(c) {
	$.plugin('jcrop',{
		files: ['/++resource++zms_/jquery/jcrop/jquery.Jcrop.min.js?ts='+escape(new Date()),
				'/++resource++zms_/jquery/jcrop/jquery.Jcrop.css?ts='+escape(new Date())]
		});
	$.plugin('jcrop').get('body',c);
}

/**
 * jQuery Cookies
 * @see http://code.google.com/p/cookies
 */
function runPluginCookies(c) {
	$.plugin('cookies',{
		files: ['/++resource++zms_/jquery/jquery.cookies.2.2.0.min.js']
		});
	$.plugin('cookies').get('body',c);
}

/**
 * jQuery JSON
 */
function runPluginJSON(c) {
	$.plugin('json',{
		files: ['/++resource++zms_/jquery/jquery.json-2.2.min.js']
		});
	$.plugin('json').get('body',c);
}

/**
 * ZMS jQuery Testsuite
 */
function runPluginTestsuite() {
	$.plugin('testsuite',{
		files: ['/++resource++zms_/jquery/tests/jquery.plugin.testsuite.js?ts='+escape(new Date())]
		});
	$.plugin('testsuite').get('body',function(){zmiTestRun()});
}
