var Dajax = {
{% for f in dajax_js_functions %}
	{{f.0.0}}_{{f.1}}: function(argv){
		this.dajax_call('{{f.0.1}}','{{f.1}}',argv);
	},
{% endfor %}
	
	dajax_call: function(app,fun,argv)
	{
		dojo.xhrPost({url: '/{{DAJAX_URL_PREFIX}}/'+app+'.'+fun+'/',
					handleAs: "json",
					load: function(data, ioArgs){
						
						dojo.forEach(data, function(elem,i){ 
							switch(elem.cmd)
							{
								case 'alert':
									alert(elem.val)
								break;
								
								case 'data':
									eval( elem.fun+"(elem.val);" );
								break;
								
								case 'as':
									dojo.forEach(dojo.query(elem.id),function(e){ e[elem.prop] = elem.val; });
								break;

								case 'addcc':
									dojo.forEach(elem.val,function(e){
										dojo.query(elem.id).addClass(e);
									});
								break;

								case 'remcc':
									dojo.forEach(elem.val,function(e){
										dojo.query(elem.id).removeClass(e);
									});
								break; 

								case 'ap':
									dojo.forEach(dojo.query(elem.id),function(e){ e[elem.prop] += elem.val;});
								break;

								case 'pp':
									dojo.forEach(dojo.query(elem.id),function(e){ e[elem.prop] = elem.val + e[elem.prop] ;});
								break;

								case 'clr':
									dojo.forEach(dojo.query(elem.id),function(e){ e[elem.prop] = ""; });
								break;

								case 'red':
									window.setTimeout('window.location="'+elem.url+'";',elem.delay);
								break;

								case 'js':
									eval(elem.val);
								break;

								case 'rm':
									dojo.forEach(dojo.query(elem.id), "dojo.query(item).orphan();");
								break;

								default:
									alert('Unknown action!');
							}
						});
						
					},
					error: function(data, ioArgs){
						alert('Something went wrong...');
					},
					content: argv
		});

	}
};