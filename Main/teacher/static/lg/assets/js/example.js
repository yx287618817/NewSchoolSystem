// Run the script on DOM ready:
$(function(){
 $('table').visualize({type: 'pie', height: '500px', width: '900px'});
	$('table').visualize({type: 'bar', width: '900px', height: '500px'});
	$('table').visualize({type: 'area', width: '900px', height: '500px'});
	$('table').visualize({type: 'line', width: '900px', height: '500px'});
});