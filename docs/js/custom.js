// promises to load data from local directory
var committed_promise = $.ajax({
	dataType: 'json',
	method: 'GET',
	url: 'https://storage.googleapis.com/annotationdb/tree.json',
	cache: false,
	beforeSend: function(request) {
 		request.setRequestHeader('access-control-expose-headers', 'access-control-allow-origin');
 		request.setRequestHeader('access-control-allow-origin', '*');
 	}
})
var pending_promise = $.ajax({
	dataType: 'json',
	method: 'GET',
	url: 'https://storage.googleapis.com/annotationdb-submit/tree.pending.json',
	cache: false,
	beforeSend: function(request) {
 		request.setRequestHeader('access-control-expose-headers', 'access-control-allow-origin');
 		request.setRequestHeader('access-control-allow-origin', '*');
 	}
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

// function to populate an array of "status" elements, where each element describes if an 
// editable field in the data tree object is different in the "new" version compared to the "old"
// version. element is uniquely identified by annotation and field
function get_editables(old_data, new_data, editables) {
	$.each(old_data, function(index, value) {
		$.each(['text', 'study_title', 'study_link', 'study_data', 'free_text', 'description'], function(_, field) {
			if (value.hasOwnProperty(field)) {
				if (value[field] == new_data[index][field]) {
					edited = false;
				} else {
					edited = true;
				}
				editables.push({'annotation': value['annotation'],
								'field': field,
								'original_value': value[field],
								'pending_value': new_data[index][field],
								'current_value': value[field],
								'pending_edited': edited,
								'current_edited': false});
			}
		});
		if (value.hasOwnProperty('nodes')) {
			get_editables(value['nodes'], new_data[index]['nodes'], editables);
		}
	});
}

// autosize textareas
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

// when getJSON promise is fulfilled, use the data to fill in Handlebars templates
$.when(committed_promise, pending_promise).done(function(committed_data, pending_data) {

	// copy of the committed data, used to populate the page initially
	var data_committed = $.extend(true, [], committed_data[0]);

	// copy of the pending data, where changes have been suggested but not yet reviewed
	var data_pending = $.extend(true, [], pending_data[0]);

	// copy of pending data to work with in the browser
	var data_current = $.extend(true, [], pending_data[0]);

	// add level to each annotation, beginning with level 0; e.g. va.cadd => level 0, va.cadd.PHRED => level 1;
	// used to format the padding on the left nav
	add_levels(data_committed, 0);

	// compile left-nav Handlebars template, insert data, add to DOM
	var left_nav_compiled = Handlebars.compile($('#script-left-nav').html());
	var left_nav_rendered = left_nav_compiled(data_committed);
	$('#left-nav').html(left_nav_rendered);

	// compile left-nav-content Handlebars template, insert data, add to DOM
	var left_nav_content_compiled = Handlebars.compile($('#script-left-nav-content').html());
	var left_nav_content_rendered = left_nav_content_compiled(data_committed);
	$('#left-nav-content').html(left_nav_content_rendered);

	// populate status array object with any differences between committed data and pending data
	var editables = [];
	get_editables(data_committed, data_pending, editables);

	// for each element with changes pending, disable editing for that textarea
	$.each(editables, function(index, value) {
		if (value.pending_edited) {
			$('.custom-btn.edit[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).addClass('disabled');
			$('.tooltip-wrapper.edit[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).attr('data-original-title', 'Update pending');
			$('.tooltip-wrapper.discard[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).attr('data-original-title', 'Update pending');
		}
	});

	// add background to textarea when its corresponding edit button is hovered over
	$('.custom-btn').hover(function() {
			$($(this).attr('href')).addClass('hover');
		}, function() {
			$($(this).attr('href')).removeClass('hover');
	});

	// autosize textareas
	$(document).on('shown.bs.tab', function(e) {
		$($(e.target).attr('href')).find('textarea').each(function() {
			autosize_textarea(this);
		});
	});

	// trigger the first annotation tab
	$('#left-nav>div:first-child').tab('show');

	// activate tooltips
	$('.doc-row>b[data-toggle="tooltip"]').tooltip();

	// activate popovers
	$('#btn-upload-changes[data-toggle="tooltip"]').popover({
		placement: 'bottom',
		delay: {
			show: 0,
			hide: 100
		}
	});
	$(document).on('click', '#btn-upload-changes[data-toggle="tooltip"]', function() {
		setTimeout(function() { $('.popover').fadeOut(); }, 1000);
	});

	// behavior when an edit button is clicked
	$(document).on('click', '.custom-btn.edit', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');

		($(this).removeClass('edit')
			    .addClass('save')
				.removeClass('btn-warning')
				.addClass('btn-success'));

		($($(this).attr('href')).removeClass('locked')
		  					    .removeAttr('readonly'));

		($(this).find('i')
			    .removeClass('fa-pencil')
				.addClass('fa-floppy-o'));

		($('.tooltip-wrapper.edit[annotation="{0}"][field="{1}"]'.format(annotation, field)).attr('data-original-title', 'Save changes')
																						    .removeClass('edit')
																						    .addClass('save'));

		$('.custom-btn.discard[annotation="{0}"][field="{1}"]'.format(annotation, field)).removeClass('disabled');
		
	});

	// behavior when a save button is clicked
	$(document).on('click', '.custom-btn.save', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');

		autosize_textarea($(this).attr('href'));

		($(this).removeClass('save')
		        .addClass('edit')
				.removeClass('btn-success')
				.addClass('btn-warning')
				.attr('data-original-title', 'Edit'));

		($($(this).attr('href')).addClass('locked')
		 					    .attr('readonly', true));

		($(this).find('i')
			    .removeClass('fa-floppy-o')
				.addClass('fa-pencil'));

		($('.tooltip-wrapper.save[annotation="{0}"][field="{1}"]'.format(annotation, field)).attr('data-original-title', 'Edit')
																							.removeClass('save')
																							.addClass('edit'));

		var original_value = editables.filter(function(element) {
			return (element.annotation == annotation & element.field == field);
		})[0].original_value;

		var current_value = $('textarea[annotation="{0}"][field="{1}"]'.format(annotation, field)).val();

		if (original_value != current_value) {

			editables.filter(function(element) {
				return (element.annotation == annotation & element.field == field);
			})[0].current_value = current_value;

			editables.filter(function(element) {
				return (element.annotation == annotation & element.field == field);
			})[0].current_edited = true;

			$('.custom-btn.discard[annotation="{0}"][field="{1}"]'.format(annotation, field)).removeClass('disabled');

		} else {

			editables.filter(function(element) {
				return (element.annotation == annotation & element.field == field);
			})[0].current_value = original_value;

			editables.filter(function(element) {
				return (element.annotation == annotation & element.field == field);
			})[0].current_edited = false;

			$('.custom-btn.discard[annotation="{0}"][field="{1}"]'.format(annotation, field)).addClass('disabled');

		}

		var any_edited = editables.filter(function(element) {
			return (element.current_edited);
		}).length > 0;

		if (any_edited) {
			$('#btn-upload-changes').removeClass('disabled');
		} else {
			$('#btn-upload-changes').addClass('disabled');
		}

	});

	// behavior when a discard button is clicked; discard changes that have been made to data_current
	$(document).on('click', '.custom-btn.discard', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');

		var original_value = editables.filter(function(element) {
			return (element.annotation == annotation & element.field == field);
		})[0].original_value;

		editables.filter(function(element) {
			return (element.annotation == annotation & element.field == field);
		})[0].current_value = original_value;

		editables.filter(function(element) {
			return (element.annotation == annotation & element.field == field);
		})[0].current_edited = false;

		$('textarea[annotation="{0}"][field="{1}"]'.format(annotation, field)).val(original_value);
		$(this).addClass('disabled');

		var any_edited = editables.filter(function(element) {
			return (element.current_edited);
		}).length > 0;

		if (any_edited) {
			$('#btn-upload-changes').removeClass('disabled');
		} else {
			$('#btn-upload-changes').addClass('disabled');
		}

	});

	// link to Struct page for Structs in tables
	$(document).on('click', '.docs-jump-btn', function() {
		$($(this).attr('href')).trigger('click');
	});

	function change_value(data_object, annotation, field, new_value) {
		$.each(data_object, function(index, value) {
			if (value.annotation == annotation) {
				value[field] = new_value;
			} else {
				if (value.hasOwnProperty('nodes')) {
					change_value(value.nodes, annotation, field, new_value);
				}
			}
		});
	}

	// behavior when upload button is clicked
	$(document).on('click', '#btn-upload-changes', function() {

		$.each(editables, function(_, value) {
			if (value.current_edited) {
				change_value(data_pending, value.annotation, value.field, value.current_value);
				value.pending_value = value.current_value;
				value.pending_edited = true;
				value.current_edited = false;
				$('.tooltip-wrapper.edit[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).attr('data-original-title', 'Update submitted');
				$('.tooltip-wrapper.discard[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).attr('data-original-title', 'Update submitted');
				$('.custom-btn.edit[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).addClass('disabled');
				$('.custom-btn.discard[annotation="{0}"][field="{1}"]'.format(value.annotation, value.field)).addClass('disabled');
			}
		});

		$(this).addClass('disabled');

		$.ajax({
			type: 'POST',
			url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb-submit/o?name=tree.test.json',
			data: JSON.stringify(data_pending),
			contentType: 'application/json',
			dataType: 'json'
		});
	
	});

});
