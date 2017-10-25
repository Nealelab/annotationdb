Handlebars.registerHelper('paddingLevel', function(x) {
	return (5 + (5 * x)).toString() + '%';
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

Handlebars.registerHelper('makeDescription', function() {
	if (this.type == 'Struct') {
		return '<a class="doc-jump" annotation="{0}">Documentation</a>'.format(this.annotation);
	} else if (this.hasOwnProperty('description')) {
		return this.description;
	} else {
		return '';
	}
});