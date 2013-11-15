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
     		jq(view).find(".carousel #carousel").jCarouselLite({
        			btnNext: ".next",
       		 		btnPrev: ".prev", 
					visible:7, 
					circular:false

    		});

				
			var viewer_id = jq(view).find(".viewer").attr("id");
			jq(view).find(".jCarouselLite a").click(function(e){
					show_in_viewer(jq(this), viewer_id);
					return false;
			}).filter(":first").click();

    		// .filter(":first").click()
    	}
