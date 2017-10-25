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

/*Handlebars.registerHelper('listFields', function(fields) {

	$(document).ready(function() {

		var tab = '.tab[annotation="{0}"]'.format(fields.annotation);
		var field_obj = {
			'annotation': fields.annotation,
			'other': []
		};

		if (fields.hasOwnProperty('title')) {
			field_obj['title'] = {
				'field': 'title',
				'value': fields.title
			}
		}

		if (fields.hasOwnProperty('nodes')) {
			field_obj['nodes'] = [];
			$.each(fields.nodes, function(index, value) {
				var annotation = value.annotation;
				if (value.hasOwnProperty('type')) {
					var type = value.type;
				} else {
					var type = '';
				}
				var element = {
					'annotation': annotation,
					'type': type
				}
				if (type != 'Struct') {
					if (value.hasOwnProperty('description')) {
						element['description'] = value.description;
					} else {
						element['description'] = '';
					}
				}
				field_obj['nodes'].push(element);
			});
		}

		$.each(fields, function(key, value) {
			if (key == 'annotation' || key == 'title' || key == 'nodes') {
				return true;
			} else {
				field_obj['other'].push({'field': key, 'value': value});
			}
		});

		load_template(path='templates/fields.hbs', data_object=field_obj, target=tab, method='append');

	});

});*/
