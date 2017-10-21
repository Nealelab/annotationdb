Handlebars.registerHelper('paddingLevel', function(x) {
	return (5 + (5 * x)).toString() + '%';
});

Handlebars.registerHelper('makeID', function(annotation) {
	return annotation.replace('va.', '').replace('.', '-');
});

Handlebars.registerHelper('stripRoot', function(annotation) {
	return annotation.split('.').pop();
});

Handlebars.registerHelper('splitPath', function(annotation) {
	var split = annotation.split('.');
	return split.map(function(element, index) {
		if (element == 'va') {
			return '<li style="padding-right: 0.75em">' + element + '</li>';
		} else {
			return '<li><a class="breadcrumb-link" annotation="' + split.slice(0, index+1).join('.') + '">' + element + '</a></li>';
		}
	}).join('');
});

Handlebars.registerHelper('dbList', function(node) {
	var files = [].concat(node.db_file);
	var keys = (node.hasOwnProperty('db_key') ? [].concat(node.db_key) : false);
	var elements = (node.hasOwnProperty('db_element') ? [].concat(node.db_element) : false);
	var out = [];
	for (i=0; i<files.length; i++) {
		var key = (keys ? keys[i] : '');
		var element = (elements ? elements[i] : '');
		out.push(
			'<tr>',
			'<td>', files[i], '</td>',
			'<td>', key, '</td>',
			'<td>', element, '</td>',
			'</tr>'
		); 
	}
	return out.join('');
});

Handlebars.registerHelper('annotationList', function(node) {
	var out = [];
	$.each(node.nodes, function(index, value) {
		if (value.type == 'Struct') {
			var description = '<a class="doc-jump" annotation="' + value.annotation + '">Description</a>';
			var original = 'Description';
		} else {
			var description = value.description;
			var original = value.description;
		}
		out.push(
			'<tr>',
			'<td annotation="' + value.annotation + '" field="annotation" original="' + value.annotation + '">', value.annotation, '</td>',
			'<td annotation="' + value.annotation + '" field="type" original="' + value.type + '">', value.type, '</td>',
			'<td annotation="' + value.annotation + '" field="description" original="' + original + '">', description, '</td>',
			'<td>', '<a class="button delete-element" disabled annotation="' + value.annotation + '"><i class="fa fa-minus"></i></a>', '</td>',
			'</tr>'
		);
	});
	return out.join('');
});
