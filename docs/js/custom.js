// promise to load annotation data from Google storage
var committed_promise = $.ajax({
	dataType: 'json',
	method: 'GET',
	url: 'https://api.github.com/repos/Nealelab/annotationdb/git/blobs/e6d5b1025d986ca0cde6959fb8d8a4dbdce088a4',
	cache: false
})

// register Handlebars helpers
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
			'</tr>'
		);
	});
	return out.join('');
});

function load_partial(path, name) {
	$.ajax({
		url: path,
		cache: false,
		async: false,
		success: function(template) {
			Handlebars.registerPartial(name, template);
		}
	});
}

function load_template(path, data, target) {
	$.ajax({
		url: path,
		cache: false,
		async: false,
		success: function(template) {
			compiled = Handlebars.compile(template);
			rendered = compiled(data);
			$(target).html(rendered);
		}
	});
}

load_partial('templates/leftNavPartial.hbs', 'leftNavPartial');
load_partial('templates/leftNavContentPartial.hbs', 'leftNavContentPartial');
load_partial('templates/leftNavPartialAdd.hbs', 'leftNavPartialAdd');

// custom string formatting function
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a;
}

function autosize_textarea(element) {
	$(element).css('height', 'auto');
	var diff = $(element).prop('scrollHeight') - $(element).prop('clientHeight');
	if (diff > 0) {
		$(element).height($(element).height() + diff);
	}
}

function add_levels(data, current_level) {
	$.each(data, function(index, value) {
		value['level'] = current_level;
		if (value.hasOwnProperty('nodes')) {
			add_levels(value['nodes'], current_level + 1);
		}
	});
}

function change_value(data, annotation, field, new_value) {
	$.each(data, function(_, value) {
		if (value.annotation == annotation) {
			value[field] = new_value;
		} else {
			if (value.hasOwnProperty('nodes')) {
				change_value(value.nodes, annotation, field, new_value);
			}
		}
	});
}

function get_value(data, annotation, field, out) {
	$.each(data, function(_, value) {
		if (value.annotation == annotation) {
			out = value[field];
			return false;
		} else {
			if (value.hasOwnProperty('nodes')) {
				get_value(value.nodes, annotation, field, out);
			}
		}
	});
	return out;
}

function post_data(data) {
	$.ajax({
		type: 'POST',
		async: true,
		url: 'https://api.github.com/repos/Nealelab/annotationdb/git/blobs',
		//url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb-submit/o?name=tree.json',
		data: JSON.stringify(data),
		contentType: 'application/json',
		dataType: 'json'
	});
	$.ajax({
		type: 'POST',
		async: true,
		url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb-submit/o?name=tree.json.bak',
		data: JSON.stringify(data),
		contentType: 'application/json',
		dataType: 'json'
	});
}

// when getJSON promise is fulfilled, use the data to fill in Handlebars templates
//$.when(committed_promise, pending_promise).done(function(committed_data, pending_data) {
$.when(committed_promise).done(function(data) {

	data = JSON.parse(atob(data.content));
	console.log(data);
	// add levels; e.g. va.cadd => level 0, va.cadd.PHRED => level 1; used to format the padding on the left nav
	add_levels(data, 0);

	// compile Handlebars templates, insert data, add to DOM
	load_template(path='templates/leftNav.hbs', data=data, target='#left-nav');
	load_template(path='templates/leftNavContent.hbs', data=data, target='#left-nav-content');

	$(document).on('click', '.nav-tab', function() {

		$('.nav-tab').removeClass('show');
		$(this).addClass('show');
		$('.tab').removeClass('show');

		var target = $('.tab[annotation="' + $(this).attr('annotation') + '"]');
		target.addClass('show');
		target.find('textarea').each(function(_, value) {
			autosize_textarea(value);
		});
	});

	$(document).on('click', '.breadcrumb-link', function() {
		$('.nav-tab[annotation="' + $(this).attr('annotation') + '"]').trigger('click');
	});

		$(document).on('click', '.button.edit:not([field="table"])', function() {
		($(this).removeClass('is-warning')
				.removeClass('edit')
				.addClass('is-success')
				.addClass('save')
				.text('Save'));
		($('textarea[annotation="' + $(this).attr('annotation') + '"][field="' + $(this).attr('field') + '"]').removeAttr('readonly')
																											  .removeClass('locked')
																											  .trigger('focus'));
	});

	$(document).on('click', '.button.save:not([field="table"])', function() {
		($(this).removeClass('is-success')
				.removeClass('save')
				.addClass('is-warning')
				.addClass('edit')
				.text('Edit'));
		$('.button.discard[annotation="' + $(this).attr('annotation') + '"][field="' + $(this).attr('field') + '"]').attr('disabled', true);

		var txt = $('textarea[annotation="' + $(this).attr('annotation') + '"][field="' + $(this).attr('field') + '"]');
		
		(txt.attr('readonly', true)
			.addClass('locked'));

		if (get_value(data, $(this).attr('annotation'), $(this).attr('field'), '') != txt.val()) {
			change_value(data, $(this).attr('annotation'), $(this).attr('field'), txt.val());
			post_data(data);
			txt.attr('original', txt.val());
		}

	});

	$(document).on('change input paste keyup', 'textarea', function() {
		var btn = $('.button.discard[annotation="' + $(this).attr('annotation') + '"][field="' + $(this).attr('field') + '"]');
		if ($(this).val() != $(this).attr('original')) {
			btn.removeAttr('disabled');
		} else {
			btn.attr('disabled', true);
		}
	});

	$(document).on('change input paste keyup', 'textarea[field="title"]', function() {
		var tab = $('.nav-tab[annotation="' + $(this).attr('annotation') + '"]');
		if (tab.text() != $(this).val()) {
			tab.text($(this).val());
		}
	});

	$(document).on('click', '.button.discard:not([field="table"])', function() {
		var select = '[annotation="' + $(this).attr('annotation') + '"][field="' + $(this).attr('field') + '"]';
		$('textarea' + select).val($('textarea' + select).attr('original')).trigger('change');
		$('.button.save' + select).trigger('click');
	});

	$(document).on('click', '.button.edit[field="table"]', function() {
		($(this).removeClass('is-warning')
				.removeClass('edit')
				.addClass('is-success')
				.addClass('save')
				.text('Save'));

		var target = $('table[annotation="' + $(this).attr('annotation') + '"][field="table"]');
		target.find('td').attr('contenteditable', 'true');
		target.find('tbody tr:first-child td:first-child').trigger('focus');
	});

	$(document).on('click', '.button.save[field="table"]', function() {
		($(this).removeClass('is-success')
				.removeClass('save')
				.addClass('is-warning')
				.addClass('edit')
				.text('Edit'));
		$('.button.discard[annotation="' + $(this).attr('annotation') + '"][field="table"]').attr('disabled', true);
		$('table[annotation="' + $(this).attr('annotation') + '"][field="table"]').find('td').each(function(_, value) {
			change_value(data, $(this).attr('annotation'), $(this).attr('field'), $(this).text());
			$(this).attr('original', $(this).text());
		});
		post_data(data);
	});

	$(document).on('change input paste keyup', 'table[field="table"] td', function() {
		var btn = $('.button.discard[annotation="' + $(this).attr('annotation').split('.').slice(0,-1).join('.') + '"][field="table"]');
		if ($(this).text() != $(this).attr('original')) {
			btn.removeAttr('disabled');
		} else {
			btn.attr('disabled', true);
		}
	});

	$(document).on('click', '.button.discard[field="table"]', function() {
		var select = '[annotation="' + $(this).attr('annotation') + '"][field="table"]';
		$('table' + select).find('td').each(function(_, value) {
			$(this).text($(this).attr('original'));
		});
		$(this).attr('disabled', true);
		$('.button.save' + select).click();
	});

	$(document).on('click', '.doc-jump', function() {
		$('.nav-tab[annotation="' + $(this).attr('annotation') + '"]').click();
	});

	$(document).on('click', '#add-annotation', function() {
		
		var new_annotation = [{
			'level': 0,
			'title': '<New annotation>',
			'annotation': 'va.',
			'db_file': '',
			'db_key': '',
			'db_element': '',
			'publication': '',
			'publication_link': '',
			'data_source': '',
			'description': '',
			'nodes': ['']
		}];

		$.ajax({
			url: 'templates/leftNav.hbs',
			cache: false,
			async: false,
			success: function(template) {
				compiled = Handlebars.compile(template);
				rendered = compiled(new_annotation);
				$('#left-nav').prepend(rendered);
			}
		});

		$.ajax({
			url: 'templates/leftNavContent.hbs',
			cache: false,
			async: false,
			success: function(template) {
				compiled = Handlebars.compile(template);
				rendered = compiled(new_annotation);
				$('#left-nav-content').prepend(rendered);
			}
		});

		$('.nav-tab:first-child').click();

	});

	$(document).on('click', '#delete-annotation', function() {
		$('#delete-modal').addClass('is-active');

	});

	$(document).on('click', '#cancel-delete', function() {
		$('#delete-modal').removeClass('is-active');
	});

	// trigger the first annotation tab
	$('.nav-tab:first-child').click();

	/*
	// add a new annotation
	$(document).on('click', '#btn-trigger-add', function() {

		var name = $($(this).attr('href')).val();*/
	//	var annotation = 'va.' + name.replace(/\b\S*/g, function(word) {
	/*		return word.charAt(0).toUpperCase() + word.substr(1);
		}).replace(/\s/g, '');

		var context = [{
			'title': name,
			'annotation': 'va.',
			'db_file': '',
			'db_key': '',
			'db_element': '',
			'publication': '',
			'publication_link',
			'data_source': '',
			'description': '',
			'nodes': []
		}];

		$.ajax({
			url: 'templates/leftNav.hbs',
			cache: false,
			async: false,
			success: function(template) {
				compiled = Handlebars.compile(template);
				rendered = compiled(context);
				$('#left-nav').prepend(rendered);
			}
		});

		$.ajax({
			url: 'templates/leftNavContent.hbs',
			cache: true,
			async: false,
			success: function(template) {
				compiled = Handlebars.compile(template);
				rendered = compiled(context);
				$('#left-nav-content').prepend(rendered);
			}
		});

		$('#left-nav>div:first-child').tab('show');	

	});*/

});
