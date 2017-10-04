// promises to load data from local directory
var committed_promise = $.getJSON('data/tree.json')
var pending_promise = $.getJSON('data/tree.pending.json')

// register Handlebars helpers
Handlebars.registerHelper('echo', function(x) {
	console.log(x);
});
Handlebars.registerHelper('paddingLevel', function(x) {
	return (5 + (5 * x)).toString() + '%';
});
Handlebars.registerHelper('makeID', function(annotation) {
	return annotation.replace('va.', '').replace('.', '-');
});
Handlebars.registerHelper('stripRoot', function(annotation) {
	return annotation.split('.').pop();
})

// register Handlebars partial templates
Handlebars.registerPartial('leftNavPartial', $('#script-left-nav-partial').html());
Handlebars.registerPartial('leftNavContentPartial', $('#script-left-nav-content-partial').html());

// custom string formatting function
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a;
}

// when getJSON promise is fulfilled, use the data to fill in Handlebars templates
$.when(committed_promise, pending_promise).done(function(committed_data, pending_data) {

	// copy of the committed data, used to populate the page initially
	var data_committed = $.extend(true, [], committed_data[0]);

	// copy of the pending data, where changes have been suggested but not yet reviewed
	var data_pending = $.extend(true, [], pending_data[0]);

	// copy of the pending data to work with in the browser
	var data_current = $.extend(true, [], pending_data[0]);

	// add level to each annotation, beginning with level 0; e.g. va.cadd => level 0, va.cadd.PHRED => level 1;
	// used to format the padding on the left nav
	function add_levels(data, current_level) {
		$.each(data, function(index, value) {
			value['level'] = current_level;
			if (value.hasOwnProperty('nodes')) {
				add_levels(value['nodes'], current_level + 1);
			}
		});
	}
	add_levels(data_committed, 0);

	// compile left-nav Handlebars template, insert data, add to DOM
	var left_nav_compiled = Handlebars.compile($('#script-left-nav').html());
	var left_nav_rendered = left_nav_compiled(data_committed);
	$('#left-nav').html(left_nav_rendered);

	// compile left-nav-content Handlebars template, insert data, add to DOM
	var left_nav_content_compiled = Handlebars.compile($('#script-left-nav-content').html());
	var left_nav_content_rendered = left_nav_content_compiled(data_committed);
	$('#left-nav-content').html(left_nav_content_rendered);

	// function to retrieve an arbitrary value from one of the data tree objects, given the
	// annotation ("va.gnomAD.exomes") and the field ("study_title")
	function get_value(data_object, annotation, field, val) {
		$.each(data_object, function(index, value) {
			if (value['annotation'] == annotation) {
				val = value[field];
				return false;
			} else {
				if (value.hasOwnProperty('nodes')) {
					val = get_value(value['nodes'], annotation, field);
				}
			}
		});
		return val;
	}

	// function replace an arbitrary value from one of the data tree objects with a new value,
	// given the annotation ("va.gnomAD.exomes"), the field ("study_title"), and the new value
	function put_value(data_object, annotation, field, new_value) {
		$.each(data_object, function(index, value) {
			if (value['annotation'] == annotation) {
				value[field] = new_value;
			} else {
				if (value.hasOwnProperty('nodes')) {
					put_value(value['nodes'], annotation, field, new_value);
				}
			}
		});
	}

	// function to populate an array of "status" elements, where each element describes if an 
	// editable field in the data tree object is different in the "new" version compared to the "old"
	// version. element is uniquely identified by annotation and field
	function get_status(old_data, new_data, editables) {
		$.each(old_data, function(index, value) {
			$.each(['study_title', 'study_link', 'study_data', 'free_text'], function(_, field) {
				if (value.hasOwnProperty(field)) {
					if (value[field] == new_data[index][field]) {
						edited = false;
					} else {
						edited = true;
					}
					editables.push({'annotation': value['annotation'],
									'field': field,
									'edited': edited});
				}
			});
			if (value.hasOwnProperty('nodes')) {
				get_status(value['nodes'], new_data[index]['nodes'], editables);
			}
		});
	}

	// function to change the status of an element in the array described above
	function change_status(status_object, annotation, field, new_status) {
		$.each(status_object, function(index, value) {
			if (value['annotation'] == annotation && value['field'] == field) {
				value['edited'] = new_status;
				return false;
			}
		});
	}

	// populate status array object with any differences between committed data and pending data
	var status = [];
	get_status(data_committed, data_pending, status);

	// for each element with changes pending, disable editing for that textarea
	$.each(status, function(index, value) {
		if (value['edited']) {
			$('.text-button[annotation="{0}"][field="{1}"][position="{2}"]'.format(value['annotation'], value['field'], 'first')).addClass('disabled');
			$('.tooltip-wrapper[annotation="{0}"][field="{1}"][position="{2}"]'.format(value['annotation'], value['field'], 'first')).attr('data-original-title', 'Update pending');
			$('.tooltip-wrapper[annotation="{0}"][field="{1}"][position="{2}"]'.format(value['annotation'], value['field'], 'second')).attr('data-original-title', 'Update pending');
		}
	});

	// add background to textarea when its corresponding edit button is hovered over
	$('.text-button').hover(function() {
			$($(this).attr('href')).addClass('hover');
		}, function() {
			$($(this).attr('href')).removeClass('hover');
	});

	// behavior when an edit button is clicked
	$(document).on('click', '.text-button.edit', function() {

		($(this).removeClass('edit')
			    .addClass('save')
				.removeClass('btn-warning')
				.addClass('btn-success'));

		($($(this).attr('href')).removeClass('locked')
		  					    .removeAttr('readonly'));

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var position = $(this).attr('position');

		$('.tooltip-wrapper[annotation="{0}"][field="{1}"][position="{2}"]'.format(annotation, field, position)).attr('data-original-title', 'Save changes');
		$('.text-button[annotation="{0}"][field="{1}"][position="third"]'.format(annotation, field)).removeClass('disabled');
		

		($(this).find('i').removeClass('fa-pencil')
						  .addClass('fa-floppy-o'));
	});

	// behavior when a save button is clicked
	$(document).on('click', '.text-button.save', function() {

		($(this).removeClass('save')
		        .addClass('edit')
				.removeClass('btn-success')
				.addClass('btn-warning')
				.attr('data-original-title', 'Edit'));

		($($(this).attr('href')).addClass('locked')
		 					    .attr('readonly', true));

		($('.tooltip-wrapper[annotation="{0}"][field="{1}"][position="{2}"]'.format($(this).attr('annotation'), 
																				    $(this).attr('field'), 
																				    $(this).attr('position'))).attr('data-original-title', 'Edit'));

		($(this).find('i').removeClass('fa-floppy-o')
						  .addClass('fa-pencil'));

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');

		var original_value = get_value(data_committed, annotation, field);
		var new_value = $('textarea[annotation="{0}"][field="{1}"]'.format(annotation, field)).val();

		if (original_value != new_value) {

			change_status(status, annotation, field, true);
			put_value(data_current, annotation, field, new_value);
			$('.text-button[annotation="{0}"][field="{1}"][position="second"]'.format(annotation, field)).removeClass('disabled');

		} else {

			change_status(status, annotation, field, false);
			put_value(data_current, annotation, field, original_value);
			$('.text-button[annotation="{0}"][field="{1}"][position="second"]'.format(annotation, field)).addClass('disabled');
			$('.text-button[annotation="{0}"][field="{1}"][position="third"]'.format(annotation, field)).addClass('disabled');

		}
	});

	// behavior when an upload button is clicked
	$(document).on('click', '.text-button.upload', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var current_value = get_value(data_current, annotation, field);

		put_value(data_pending, annotation, field, current_value);


	});

	// behavior when a discard button is clicked; discard changes that have been made to data_current
	$(document).on('click', '.text-button.discard', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var original_value = get_value(data_committed, annotation, field);

		change_status(status, annotation, field, false);
		put_value(data_current, annotation, field, original_value);

		$('textarea[annotation="{0}"][field="{1}"]'.format(annotation, field)).val(original_value);
		$('.text-button[annotation="{0}"][field="{1}"][position="second"]'.format(annotation, field)).addClass('disabled');
		$(this).addClass('disabled');

	});

	// link to Struct page for Structs in tables
	$(document).on('click', '.description-jump-btn', function() {
		$($(this).attr('href')).trigger('click');
	});

	// autosize textareas
	$(document).on('shown.bs.tab', function(e) {
		$($(e.target).attr('href')).find('textarea.edit-text').each(function() {
			$(this).height($(this).prop('scrollHeight'));
		});
	});

	// trigger the first annotation tab
	$('#left-nav>div:first-child').tab('show');

	// activate tooltips
	$('[data-toggle="tooltip"]').tooltip();

});

