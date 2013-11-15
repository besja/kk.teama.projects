

		jq(function() { 
    	    
    		jq("a.read_more").click(function(e) {
    			
    			var href = jq(this).attr("href");
    			var view = jq(this).parents('.tileItem').find('.view');
    			var preview = jq(this).parents('.tileItem').find('.preview');
    			jq(preview).hide();
    			if (!jq(view).hasClass('proccesed')) {
    			
    				jq.get(href, {ajax_load: "1"}, function(data){
    					var content = jq(data).find("#content-core");
    				    var header = jq(preview).find("h2.tileHeadline").clone();   				    
    					jq(view).prepend(content);
    					jq(view).find(".carousel").after(header);
    					jq(view).show();
    					setup_carousel(jq(view));
    					jq(view).addClass('proccesed');    				
    				});
    			}else {
    				jq(view).show();
    			}
    			return false;
    		});
    		jq("a.hide").click(function(e) {
    			
    			var view = jq(this).parents('.tileItem').find('.view');
    			var preview = jq(this).parents('.tileItem').find('.preview');
    			jq(view).hide();
                jq(preview).show();

    			return false;
    	 	});
    	});
