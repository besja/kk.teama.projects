
		function show_in_viewer(elem, viewer_id) {
   			var src = jq(elem).attr("href");
    	    var is_video = jq(elem).hasClass("video");
    	    jq("#"+viewer_id).parent().find(".active").removeClass('active');
    	    jq(elem).addClass('active');
			if (is_video) {
				player = flowplayer(viewer_id, "http://releases.flowplayer.org/swf/flowplayer-3.2.7.swf");
				player.play(src);
			} else {
				jq("#"+viewer_id).html("<img src ='"+src+"' />");
			} 
			return false;	
		}    
    	function setup_carousel(view) {
    	
        	jq(view).find(".carousel #carousel").jcarousel({});  
        	  	
			jq(view).find(".jCarouselLite a").click(function(e){
			        var total = jq(view).find('.jcarousel').jcarousel('items').length;
					var viewer_id = jq(view).find(".viewer").attr("id");
			        var this_index = jq(view).find("li").index(jq(this).parent());				
					var active_index = jq(view).find("li").index(jq(view).find("a.active").parent());
					var offset = this_index - active_index;
					if (offset > 0) {
						//вперед
						if (this_index > 3) {
							//двигаемся c третьего
							var items_to_move = this_index - Math.max(3, active_index);
							// если active_index < 3, то двигаемся так 
							jq(view).find('.jcarousel').jcarousel('scroll', "+="+items_to_move);
						}
					} 
					if (offset < 0 ) {
						//назад
						if (this_index < total - 4) {
						 	var items_to_move = Math.min(active_index, total - 4) - this_index;
						 	jq(view).find('.jcarousel').jcarousel('scroll', "-="+items_to_move);
						}						
					}
					show_in_viewer(jq(this), viewer_id);
					return false;
			}).filter(":first").click();
			
			jq(view).parent().find(".next").click(function(e) {

	            var viewer_id = jq(view).find(".viewer").attr("id");
				var active = jq(view).find("a.active");
				var next = active.parent().next();
				var next_index = jq(view).find("li").index(next);
				if (next.length) {
					next.find("a").addClass("active");
					active.removeClass('active');
					show_in_viewer(next.find("a"), viewer_id);
					if (next_index>3)
					jq(view).find('.jcarousel').jcarousel('scroll', "+=1");
				}
				
			})
			jq(view).parent().find(".prev").click(function(e) {
			    var total = jq(view).find('.jcarousel').jcarousel('items').length;
	            var viewer_id = jq(view).find(".viewer").attr("id");    
				var active = jq(view).find("a.active");
				var prev = active.parent().prev();
				var prev_index = jq(view).find("li").index(prev);
				if (prev.length) {
					prev.find("a").addClass("active");
					active.removeClass('active');
					show_in_viewer(prev.find("a"), viewer_id);
					if (prev_index < total - 4)
					jq(view).find('.jcarousel').jcarousel('scroll', "-=1");				
				}				
			})
	}