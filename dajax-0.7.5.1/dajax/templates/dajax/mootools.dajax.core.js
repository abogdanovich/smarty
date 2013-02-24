var Dajax = {
	
{% for f in dajax_js_functions %}
	{{f.0.0}}_{{f.1}}: function(argv){
		this.dajax_call('{{f.0.1}}','{{f.1}}',argv);
	},
{% endfor %}
	
	dajax_call: function(app,fun,argv)
	{
		var jsonRequest = new Request.JSON({url: '/{{DAJAX_URL_PREFIX}}/'+app+'.'+fun+'/', method: "post", onSuccess: function(data){
		
			data.each(function(elem)
			{
				switch(elem.cmd)
				{
					case 'alert':
						alert(elem.val)
					break;
			
					case 'data':
						eval( elem.fun+"(elem.val);" );
					break;

					case 'as':
						$$(elem.id).each(function(e){ e[elem.prop] = elem.val; });
					break;

					case 'addcc':
						elem.val.each(function(cssclass){
					 		$$(elem.id).each(function(e){ e.addClass(cssclass);});
						});
					break;

					case 'remcc':
						elem.val.each(function(cssclass){
							$$(elem.id).each(function(e){ e.removeClass(cssclass);});
						});
					break;

					case 'ap':
						$$(elem.id).each(function(e){ e[elem.prop] += elem.val; });
					break;

					case 'pp':
						$$(elem.id).each(function(e){ e[elem.prop] = elem.val + e[elem.prop]; });
					break;

					case 'clr':
						$$(elem.id).each(function(e){ e[elem.prop]=""; });
					break;

					case 'red':
						window.setTimeout('window.location="'+elem.url+'";',elem.delay);
					break;

					case 'js':
						eval(elem.val);
					break;

					case 'rm':
						$$(elem.id).each(function(e){ e.destroy(); });
					break;

					default:
						alert('Unknown action!');
				}
			},this);
			
		}}).post(argv);
	}
};