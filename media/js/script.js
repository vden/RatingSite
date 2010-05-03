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

window.addEvent ('domready', function() {
	var sfEls = $$('ul.ja-megamenu li');
	sfEls.each (function(li){
		li.addEvent('mouseenter', function(e) {
			clearTimeout(this.timer);
			jaMegaHoverOutOther (this);
			if(this.className.indexOf(" over") == -1)
				this.className+=" over";
		});
		li.addEvent('mouseleave', function(e) {
			this.timer = setTimeout(jaMegaHoverOut.bind(this, e), 1000);
		});
	});
	function jaMegaHoverOut(e) {
		clearTimeout(this.timer);
		this.className=this.className.replace(new RegExp(" over\\b"), "");
	}
	function jaMegaHoverOutOther(el) {
		sfEls.each (function(li) {
			if (li != el)
				li.className = li.className.replace(new RegExp(
								" over\\b"), "");
				});
	}
});