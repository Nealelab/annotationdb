load_partial('tableRow', 'templates/tableRow.hbs', 'tableRow');

Handlebars.registerHelper('paddingLevel', function(annotation) {
	return 5 *(annotation.split('.').length - 1) + '%';
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

Handlebars.registerHelper('ifstruct', function(_, options) {
	if (this.type == 'Struct') {
		return options.fn(this);
	} else {
		return options.inverse(this);
	}
});

Handlebars.registerHelper('listRows', function(parent, data) {
	var context = data.filter(function(x) {
		return (x.annotation.startsWith(parent + '.') && 
				x.annotation.split('.').length == parent.split('.').length + 1);
	});
	var template = Handlebars.partials['tableRow'];
	var compiled = Handlebars.compile(template);
	return compiled(context);
});
