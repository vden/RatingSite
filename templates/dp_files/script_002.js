/*
# ------------------------------------------------------------------------
# JA Teline III - Stable - Version 1.4 - Licence Owner JA49652
# ------------------------------------------------------------------------
# Copyright (C) 2004-2009 J.O.O.M Solutions Co., Ltd. All Rights Reserved.
# @license - Copyrighted Commercial Software
# Author: J.O.O.M Solutions Co., Ltd
# Websites:  http://www.joomlart.com -  http://www.joomlancers.com
# This file may not be redistributed in whole or significant part.
# ------------------------------------------------------------------------
*/ 

JAUserSetting = new Class({		
						  
	initialize:function( defaults ){
		this.options = Object.extend({
			ajxURL: '',
			quees: [],
			blocks:[],
			containerClass: 'ja-usersetting-options'
		}, defaults || {});
		this.idsReload = new Array();	
	},
	/**
	 * show user setting form.
	 */
	showForm:function(a, parent, idReload){
		
		var action = 'loadform';
		parent.idReload = idReload;
		// looking for container which contain setting form.
		var container = parent.getElement( '.'+this.options.containerClass );
		if(container == null){ ;
			new Ajax( a.href, { method:'get', 
						 	    postBody:"action="+action+"&tmpl=component&rand="+(Math.random()*Math.random()), 
								onComplete:function(data){
									this._renderForm( data, parent, a ); 
									
									//begin: thanhnv
									//excute javascript
									newobj = new Element ('DIV');
									newobj.innerHTML = data;
									newobj.getElements ('script').each(function(script){
										//alert(script.innerHTML);
										if (script.src) {
											new Element('script', {'type':'text/javascript','src':script.src}).inject($E('head'));
										} else {
											eval (script.innerHTML);
										}
									});
									
									//excute callback function
									if(this.callBack) {
										this.callBack(idReload);
									}
									//end:thanhnv
													
								}.bind(this),  
								onFailure: function(){ alert('fail request');} }
				).request();

		} else {
			if ( container.getStyle('height').toInt() <= 0 ) {	
				this.showElement( container, container.maxHeight );	
			} else {
				this.hideElement( container );
			}
		}	
		return false;
	},
	/**
	 * building and render html.
	 */
	_renderForm:function( text, obj, a ){
		if( obj.getElement( '.'+this.options.containerClass ) != null ) return ;
		var divcontainer = new Element( 'div' );
		 		 	divcontainer.addClass( this.options.containerClass );
					divcontainer.setStyles({'overflow':'hidden'	});
			divcontainer.innerHTML = text;	
			obj.adopt(divcontainer);
			// store height using for last 
			divcontainer.maxHeight = divcontainer.offsetHeight;
			divcontainer.storeURL = a.href;
			// binding and processing event of form
			this._bindingAndprocessingEventForm( divcontainer, obj );
	},
	/**
	 * binding event and proccess even which happen with each element of form.
	 */
	_bindingAndprocessingEventForm:function( containter, obj ){
		var form = obj.getElement('form');
		// catch exeption
		if( $defined(form) == false){
			alert("Could not found the form setting for this module, please try to check again");
			return ;
		}
			
		// checkbox: click chooise all
		if( form.checkall != null ) {
			$(form.checkall).addEvent( 'click', function() {
				var doCheck = this.checked;
				form.getElements('input.checkbox').each(function(elm){ 
					elm.checked = doCheck;
				}.bind(this));
			});
		}
		// if click button cancel.
		form.getElement('input.ja-cancel').addEvent( 'click', function() {
			this.hideElement( containter );
		}.bind(this));	
		// if click button submit.
		form.getElement('input.ja-submit').addEvent( 'click', function() {			
		var action = obj.idReload !="" && (obj.idReload != null)
					&& ( $(obj.idReload) != null ) ? 'save_reload_module':'save_setting';
						   
		new Ajax( containter.storeURL+"&action="+action+"&tmpl=component&rand="+(Math.random()*Math.random()), { method:'post', 
					 								postBody:form.toQueryString(),
													onComplete:function(data){ 
													this.hideElement( containter );
													// reload module
													if( action == 'save_reload_module' ){
														newobj = new Element ('DIV');
														newobj.innerHTML = data;
														//alert(newobj.getElement ('#'+obj.idReload).innerHTML);
														if (newobj.getElement ('#'+obj.idReload)) $(obj.idReload).innerHTML = newobj.getElement ('#'+obj.idReload).innerHTML;
														else $(obj.idReload).innerHTML = data;
														//parse js
														//alert(newobj.getElements ('script'));
														newobj.getElements ('script').each(function(script){
															//alert(script.innerHTML);
															if (script.src) {
																new Element('script', {'type':'text/javascript','src':script.src}).inject($E('head'));
															} else {
																eval (script.innerHTML);
															}
														});
														
													}
												}.bind(this) , 
											onFailure: function(){ alert('fail request');} }
			).request();														   
		}.bind(this));
		
	},
	
	/**
	 *  Show or hide element
	 */
	showElement: function(obj, height ) {
		if(!obj.fx ){
			obj.fx = new Fx.Style(obj,'height');
		}
		obj.fx.start(height);	
	},
	hideElement: function(obj){
		obj.maxHeight = obj.offsetHeight;
		if(!obj.fx ){
			obj.fx = new Fx.Style(obj,'height');
		}
		obj.fx.start(0);
	}
	
});

