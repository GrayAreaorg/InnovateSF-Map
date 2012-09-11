/* Author: 

*/
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


var map = L.map('map',{maxZoom: 19});
var layer = new L.StamenTileLayer("toner-lite");
var layerGroups = new L.MarkerClusterGroup({maxClusterRadius:50, showCoverageOnHover: false});
var myScroll;
var hoverTitle;
var companyNames = [];
map.addLayer(layer).setView(new L.LatLng(37.7810841,-122.4105332), 15);
//map.locate({setView: true, maxZoom: 16});

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

//REFACTOR THIS, YOU ALREADY HAVE THE PARENT NAME
function get_type(location, higher) {
  var i = -1;
  var type_obj = {};
  _.each(location.fields.type, function(obj){
    x = _.values(obj)[0]
    if(higher == true) { 
      if (x > i) {
        x = i;
        type_obj = _.keys(obj)[0]; 
      }
    } else {
      if (x == 0) {
        type_obj = _.keys(obj)[0]; 
      }
    }
  });
	returnType = _.find(types, function(obj){ return obj.fields.name == type_obj  });
	if (!returnType) {
  	console.log(location);
	} else {
		return returnType;
	}
}

function getMarker(name) {
	return _.find(locations, function(loc){return loc.fields.name == name}).marker;
}

function focusMapAndPopup(name) {
	var m = getMarker(name);
	layerGroups.zoomToShowLayer(m, function () {
		map.panTo(m._latlng);
		m.openPopup();
	});
	/*window.setTimeout(function() {
	    if (m._icon) {
					map.panTo(m._latlng);
	        m.openPopup();
	    } else {
	        foundOne.spiderfy();
	        window.setTimeout(function() {
							map.panTo(m._latlng);
							m.openPopup();
	         }, 250)
	    }
	}, 250);*/
}

function removeFromClusterGroup(type) {
  _.each(type.layerGroup._layers, function(obj){ layerGroups.removeLayer(obj) })
}

function addToClusterGroup(type) {
  _.each(type.layerGroup._layers, function(obj){ layerGroups.addLayer(obj) })
}

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

function edit_link(theLink, theName){
	var hackNext = theName;
	$('.edit_link').bind('click', function(event){
		event.preventDefault();
		if(loggedIn) {
			var popupBox = $(this).parent();
			var oldHtml = popupBox.html();
			$.get($(this).attr('href'),function(response){
				popupBox.html(response);
				$('<a>').attr('href','#').text('cancel').appendTo(popupBox).bind('click',function(event){
					event.preventDefault();
					popupBox.html(oldHtml);
					console.log(oldHtml);
					edit_link(theLink);
				});
			});
		} else {
			$.get($(this).attr('href'), function(response){
				var loggedInMessage = "<h1>You have to be logged in to do that!</h1>";
				$('<div>').appendTo('#container').addClass('modal clearfix').html("<a id='modal_close' href=''>Close</a>" + loggedInMessage + response).fadeIn('fast').find('input[name=next]').val('/'+hackNext);
			});
		}
	});
}

function submit_form(form, container){
	$(form).bind('submit', function(event){
		event.preventDefault();
		$.post($(form).attr('action'),form.serialize(),function(response){
			container.html(response);
		});
	});
}

$(function(){
  _.each(types, function(obj){
    obj['layerGroup'] = new L.LayerGroup();
    button = $("#main-menu li input[name="+obj.fields.name+"]");
    sub = button.parent().parent().parent().find('ul li');
    button.data('type',obj).data('sub',sub);
    button.change(
      function(){
        sub = $(this).data('sub')
        if($(this).is(':checked')) {
          layerGroups.addLayer($(this).data('type').layerGroup);
          if(sub.length) {
            sub.each( function(){
              $(this).find('input[type=checkbox]').attr('checked', true).change();
            });
          }
        } else {
          removeFromClusterGroup($(this).data('type'));
          if(sub.length) {
            sub.each( function(){
              $(this).find('input[type=checkbox]').attr('checked', false).change();
            });
          }
        }
      }
    );
  })

  _.each(locations, function(location){
  	var icon;
  	switch(get_type(location, false).fields.name) {
  		case 'financial-organization':
  			icon = investorIcon;
  			break;
  		case 'service-provider':
  			icon = serviceIcon;
  			break;
  		default:
  			icon = startupIcon;
  	}
		var theLink = "<a class='edit_link' href='/locations/edit/"+location.pk+"'>Edit</a>";
  	var popup = "<h1>"+location.fields.name+"</h1>"+theLink+"<div style='max-height:100px;overflow:auto'>"+location.fields.desc+"</div>";
  	var marker = L.marker( 	new L.LatLng(location.fields.lat, location.fields.lng), {icon: icon} ).bindPopup(popup)
  			.on('click', function(){
					this.openPopup();
					console.log(this);
					hoverTitle.remove();
					edit_link(theLink, this['name']);
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
		location['marker']['name'] = location.fields.name;
  	get_type(location, true).layerGroup.addLayer(location.marker);
  });

    _.each(types, function(type) {
      try {
        layerGroups.addLayer(type.layerGroup);
      } catch(error) {
        console.log(error);
      }
    })
  
	  layerGroups.addTo(map);
		
		
		$("#menu_close").toggle(
			function(){
				$("header").addClass('hidemenu');
				$(this).html("open menu");
			},
			function(){
				$("header").removeClass('hidemenu');
				$(this).html('hide menu');
			}
		);
		
		//Make the whole LI into a button (good for mobile!!)
		$('li div label').toggle(
			function(){
				li = $(this).parent().parent();
				li.find('>ul').show();
			},
			function() {
				li = $(this).parent().parent();
				li.find('>ul').hide();
			}
		);
		
		//We're all done here, refresh scrolling
		//REFACTOR
		/*if(Modernizr.touch) {
			setTimeout(function () {
					iscroll_init({action:"refresh",v:myScroll});
			}, 0);
		}*/
	//REFACTOR
	/*if(Modernizr.touch) {
		$(window).load(function(){
			iscroll_init({action:"init", v:myScroll, el:"main-menu"});
		});
		$(window).resize(function(){
			iscroll_init({action:"refresh", v:myScroll});
		});
	}*/
	
	$("#main-menu a").click(function(event){
	  event.preventDefault();
	  focusMapAndPopup($(this).attr('href').substring(1));
	})
	
	_.each(locations, function(obj){ companyNames[companyNames.length] = obj.fields.name;  });
	$("#search_field").autocomplete(companyNames).result(function(){ focusMapAndPopup($(this).val()); });
	$("#search_form").submit(function(event){event.preventDefault(); focusMapAndPopup($('#search_field').val()); });
	
	$("#mailchimp_link").click(
		function(event){
			event.preventDefault();
			$("#mailchimp_close").bind('click', function(event){ event.preventDefault(); $(this).parent().parent().fadeOut('fast'); });
			$('#mailchimp').fadeIn('fast');
		}
	)
	
	$("#modal_close").live('click', function(event){ event.preventDefault(); $('.modal').remove(); });
	//and finally,
	if(typeof mapFocus != "undefined") {
		try {
			focusMapAndPopup(mapFocus);
		} catch(e) {
			//silence is golden
		}
	}
	
	$("#login_button").click(function(){
		$.get("/locations/create",{}, function(response){
			var loggedInMessage = "";
			if(!loggedIn) { loggedInMessage = "<h1>You have to be logged in to do that!</h1>";  }
			$('<div>').appendTo('#container').addClass('modal clearfix').html("<a id='modal_close' href=''>Close</a>" + loggedInMessage + response).fadeIn('fast');
		});
	});
	
	var learn = "<a id='modal_close' href=''>Close</a><p>More than any other city, San Francisco is uniquely poised to innovate and invent the future right here, right now, by capitalizing on our greatest resource – our people.</p><p>With your help, we hope to use this map as a platform to show how much funding is coming in to SF startups, where jobs are and much much more. Add your company details and be a part of the story of San Francisco as the best place to live, work and play.</p>";

	$("#learn_button").click(function(){
		$('<div>').appendTo('#container').addClass('modal').html(learn).fadeIn('fast');
	});
	
	$(window).load(function(){ make_fullscreen(); });
});