/* Author: 

*/
var map = L.map('map');
var layer = new L.StamenTileLayer("toner-lite");
var layerGroups = {};
var myScroll;
var hoverTitle;
var layercache = [];
map.addLayer(layer);
map.locate({setView: true, maxZoom: 18});

var customIcon = L.Icon.extend({
	options: {
	            shadowUrl: '/static/img/shadow.png',
	            iconSize:     [41, 38],
	            shadowSize:   [41, 38],
	            iconAnchor:   [21, 38],
	            shadowAnchor: [21, 38],
	            popupAnchor:  [-10, -40]
	        }
});

var startupIcon = new customIcon({iconUrl: '/static/img/company.png'});
var investorIcon = new customIcon({iconUrl: '/static/img/financial-organization.png'});
var serviceIcon = new customIcon({iconUrl: '/static/img/service-provider.png'});

function iscroll_init(options) {
	if(typeof options == 'undefined') { return false; }	
	if(options.action == 'init') {
		options.v = new iScroll(options.el);
		return true;
	} else if(options.action == 'refresh') {
		options.v.refresh();
		return true;
	}
}

$(function(){
	_.each(types, function(obj){
		layerGroups[obj.name] = new L.MarkerClusterGroup({maxClusterRadius:100});
	});
	//Load markers from sample data
	_.each(locations, function(location){
		var icon;
		switch(_.intersection(location.fields.type, _.keys(layerGroups))[0]) {
			case 'financial-organization':
				icon = investorIcon;
				break;
			case 'service-provider':
				icon = serviceIcon;
				break;
			default:
				icon = startupIcon;
		}
		var popup = "<h1>"+location.fields.name+"</h1><div style='max-height:100px;overflow:auto'>"+location.fields.desc+"</div>";
		var marker = L.marker( 	new L.LatLng(location.fields.lat, location.fields.lng), {icon: icon} ).bindPopup(popup)
				.on('click', function(){
					this.openPopup();
					hoverTitle.remove();
				})
				.on('mouseover', function(){
					x = $(this._icon).offset();
					hoverTitle = $('<h3 class="hover-title">')	.appendTo('#map')
											.css(	{	'position':'absolute',
														'left':x.left,
														'top':x.top-41})
											.text(location.fields.name);
				})
				.on('mouseout', function(){
					hoverTitle.remove();
				});
		location['marker'] = marker;
		});
		
		_.each(locations, function(obj){
			_.each(_.intersection(obj.fields.type, _.keys(layerGroups) ), function(name){
				layerGroups[name].addLayer(obj.marker);
			});
		});
		
		_.each(layerGroups, function(obj){
			obj.addTo(map);
		});
		
		//Hide layers if user unchecks box. Refactor the fuck out of this.
		$('#main-menu input[type="checkbox"]').change(function() {
			var name = $(this).attr('name');
			var parent = $(this).data('parent');
			if(typeof layercache[name] == 'undefined') {
				layercache[name] = _.filter(locations, function(obj) { return _.include(obj.fields.type, name); });
			}
			if($(this).is('checked')) {
				_.each(layercache[name], function(layer){ 
						layerGroups[parent].removeLayer(layer.marker);
				});
			} else {
				_.each(layercache[name], function(layer){ 
						layerGroups[parent].addLayer(layer.marker);
				});
			}
		});
			/*var parent_li = $(this).parent().parent().parent();
			var sub_lis = parent_li.find('ul>li');

			if ($(this).is(':checked')) {
				parent_li.removeClass('inactive');
				map.addLayer(layerGroups[parent_li.attr('id')]['layer']);
				sub_lis.each(function(i, el) {
					$(this).removeClass('inactive').find('input[type="checkbox"]').attr('checked',true);
					map.addLayer(layerGroups[parent_li.attr('id')]['sublayers'][$(this).attr('id')]['layer']);
				})
			} else {
				parent_li.addClass('inactive');
				map.removeLayer(layerGroups[parent_li.attr('id')]['layer']);
				sub_lis.each(function() {
					$(this).addClass('inactive').find('input[type="checkbox"]').attr('checked',false);;
					map.removeLayer(layerGroups[parent_li.attr('id')]['sublayers'][$(this).attr('id')]['layer']);
				})
			}
		});*/
		
		//Make the whole LI into a button (good for mobile!!)
		$('header li div label').toggle(
			function(){
				li = $(this).parent().parent();
				li.find('ul').slideDown();
			},
			function() {
				li = $(this).parent().parent();
				li.find('ul').slideUp();
			}
		);
		//SHOW ALL THE THINGS!
		$.each(layerGroups, function(key, value){
			map.addLayer(value['layer']);
			if(value['sublayers'] != {}) {
				$.each(value['sublayers'], function(key, value) {
					map.addLayer(value['layer']);
				});
			}
		});
		
		//We're all done here, refresh scrolling
		//REFACTOR
		if(Modernizr.touch) {
			setTimeout(function () {
					iscroll_init({action:"refresh",v:myScroll});
			}, 0);
		}
	//REFACTOR
	if(Modernizr.touch) {
		$(window).load(function(){
			iscroll_init({action:"init", v:myScroll, el:"main-menu"});
		});
		$(window).resize(function(){
			iscroll_init({action:"refresh", v:myScroll});
		});
	}
	$("#close").toggle(
		function(){
			$("header").animate({ top: (-$("header").height()-20), bottom: ($(window).height()-20) });
			$(this).html("open menu &darr;");
		},
		function(){
			$("header").animate({ bottom: 20, top:0 });
			$(this).html('hide menu &uarr;');
		}
	);
});

/* fullscreen crap */
function make_fullscreen() {
	var page = document.getElementById('container'),
	    ua = navigator.userAgent,
	    iphone = ~ua.indexOf('iPhone') || ~ua.indexOf('iPod'),
	    ipad = ~ua.indexOf('iPad'),
	    ios = iphone || ipad,
	    // Detect if this is running as a fullscreen app from the homescreen
	    fullscreen = window.navigator.standalone,
	    android = ~ua.indexOf('Android'),
	    lastWidth = 0;

	if (android) {
	  // Android's browser adds the scroll position to the innerHeight, just to
	  // make this really fucking difficult. Thus, once we are scrolled, the
	  // page height value needs to be corrected in case the page is loaded
	  // when already scrolled down. The pageYOffset is of no use, since it always
	  // returns 0 while the address bar is displayed.
	  window.onscroll = function() {
	    page.style.height = window.innerHeight + 'px'
	  } 
	}
	var setupScroll = window.onload = function() {
	  // Start out by adding the height of the location bar to the width, so that
	  // we can scroll past it
	  if (ios) {
	    // iOS reliably returns the innerWindow size for documentElement.clientHeight
	    // but window.innerHeight is sometimes the wrong value after rotating
	    // the orientation
	    var height = document.documentElement.clientHeight;
	    // Only add extra padding to the height on iphone / ipod, since the ipad
	    // browser doesn't scroll off the location bar.
	    if (iphone && !fullscreen) height += 60;
	    page.style.height = height + 'px';
	  } else if (android) {
	    // The stock Android browser has a location bar height of 56 pixels, but
	    // this very likely could be broken in other Android browsers.
	    page.style.height = (window.innerHeight + 56) + 'px'
	  }
	  // Scroll after a timeout, since iOS will scroll to the top of the page
	  // after it fires the onload event
	  setTimeout(scrollTo, 0, 0, 1);
	};
	(window.onresize = function() {
	  var pageWidth = page.offsetWidth;
	  // Android doesn't support orientation change, so check for when the width
	  // changes to figure out when the orientation changes
	  if (lastWidth == pageWidth) return;
	  lastWidth = pageWidth;
	  setupScroll();
	})();
}