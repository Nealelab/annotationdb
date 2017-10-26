var committed_promise = $.ajax({
	dataType: 'json',
	method: 'GET',
	url: 'https://storage.googleapis.com/annotationdb/annotationdb.json',
	cache: false
});

$.when(committed_promise).done(function(data) {

	var sorted = data.sort(function(a, b) {
		if (a.annotation < b.annotation) {
			return -1;
		} else {
			return 1;
		}
	});

	load_template(path='templates/leftNav.hbs', data_object=data, target='#left-nav', method='html');
	load_template(path='templates/leftNavContent.hbs', data_object=data, target='#left-nav-content', method='html');

	($(document)

	.on('click', '.nav-tab', function() {

		var annotation = $(this).attr('annotation');
		var tab = get_el('.tab', annotation);

		$('.nav-tab').removeClass('show');
		$(this).addClass('show');
		
		$('.tab').removeClass('show');
		tab.addClass('show').find('textarea').each(function(_, value) {
			autosize_textarea(value);
		});

	})

	.on('click', '.breadcrumb-link', function() {
		get_el('.nav-tab', $(this).attr('annotation')).trigger('click');
	})

	.on('click', '.button.edit:not([field="table"]):not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var textarea = get_el('textarea', annotation, field);
		var edit = '.button.edit[annotation="{0}"][field="{1}"]'.format(annotation, field);
		var data_obj = {
			'annotation': annotation,
			'field': field
		};

		load_template(path='templates/discardButton.hbs', data_object=data_obj, target=edit, method='before');
		textarea.removeAttr('readonly').removeClass('locked').trigger('focus');

		($(this).removeClass('is-warning')
				.removeClass('edit')
				.addClass('is-success')
				.addClass('save')
				.text('Save'));

	})

	.on('click', '.button.save:not([field="table"]):not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var textarea = get_el('textarea', annotation, field);
		var val = textarea.val();

		get_el('.button.discard', annotation, field).remove();

		($(this).removeClass('is-success')
				.removeClass('save')
				.addClass('is-warning')
				.addClass('edit')
				.text('Edit'));
		
		if (field == 'annotation') {

			get_el('', annotation).attr('annotation', val);
			get_el('table', val).find('td').each(function(_, value) {
				var new_annotation = val + '.' + $(value).attr('annotation').split('.').slice(-1).pop();
				change_value(data, $(value).attr('annotation'), 'annotation', new_annotation);
				$(value).attr('annotation', new_annotation);
				if ($(value).attr('field') == 'annotation') {
				    $(value).attr('original', new_annotation).text(new_annotation);
				}
			});

		}

		textarea.attr('readonly', true).addClass('locked').attr('original', val);

		change_value(data, annotation, field, val);
		post_data(data);

	})

	.on('click', '.button.discard:not([field="table"]):not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var button = get_el('.button.save', annotation, field);
		var textarea = get_el('textarea', annotation, field);
		var original = textarea.attr('original');

		textarea.val(original).trigger('change');
		button.trigger('click');

	})

	.on('change input paste keyup', 'textarea[annotation][field]', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var val = $(this).val();
		var original = $(this).attr('original');
		var button = get_el('.button.discard', annotation, field);

		autosize_textarea($(this));

		if (val != original) {
			button.removeAttr('disabled');
		} else {
			button.attr('disabled');
		}

	})

	.on('change input paste keyup', 'textarea[field="title"]', function() {

		var annotation = $(this).attr('annotation');
		var val = $(this).val();
		var tab = get_el('.nav-tab', annotation);

		tab.text(val);

	})

	.on('click', '.button.edit[field="table"]:not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		var table = get_el('table', annotation);
		var edit = '.button.edit[annotation="{0}"][field="table"]'.format(annotation);
		var data_obj = {
			'annotation': annotation,
			'field': 'table'
		};

		load_template('templates/discardButton.hbs', data_obj, edit, 'before');

		table.find('td:not(:last-child)').attr('contenteditable', 'true');
		table.find('tbody tr:first-child td:first-child').trigger('focus');
		table.find('.add-element').removeAttr('disabled');
		table.find('.delete-element').removeAttr('disabled');

		($(this).removeClass('is-warning')
				.removeClass('edit')
				.addClass('is-success')
				.addClass('save')
				.text('Save'));

	})

	.on('click', '.button.save[field="table"]:not([disabled])', function() {

		var parent = $(this).attr('annotation');
		var table = get_el('table', parent, 'table');
		var discard = get_el('.button.discard', parent, 'table');	
		var level = get_value(data, parent, '_level');

		get_el('.button.discard', parent, 'table').remove();		

		($(this).removeClass('is-success')
				.removeClass('save')
				.addClass('is-warning')
				.addClass('edit')
				.text('Edit'));

		table.find('tbody').find('tr').each(function(_, row) {

			var row_annotation = $(row).find('td[field="annotation"]').text();
			var row_type = $(row).find('td[field="type"]').text();
			var row_description = $(row).find('td[field="description"]').text();

			var row_annotation_original = $(row).find('td[field="annotation"]').attr('original');
			var row_type_original = $(row).find('td[field="type"]').attr('original');
			var row_description_original = $(row).find('td[field="description"]').attr('original');

			if (row_annotation != row_annotation_original) {
				change_value(data, row_annotation_original, 'annotation', row_annotation);
			}

			if (row_type != row_type_original) {

				change_value(data, row_annotation, 'type', row_type);

				if (row_type == 'Struct') {

					var nav = '.nav-tab[annotation="{0}"]'.format(annotation);
					var tab = '.tab[annotation="{0}"]'.format(annotation);
					var new_struct = [{
						'_level': level + 1,
						'title': row_annotation,
						'annotation': row_annotation,
						'type': 'Struct',
						'description': row_description,
						'nodes': ['']
					}];

					load_template('templates/leftNav.hbs', new_struct, nav, 'after');
					load_template('templates/leftNavContent.hbs', new_struct, tab, 'after');

					delete_annotation(data, row_annotation);
					add_annotation(data, parent, new_struct);

				}
			}

			if (row_description != row_description_original) {
				change_value(data, row_annotation, 'description', row_description);
			}

		});

		table.find('td:not(:last-child)').removeAttr('contenteditable');
		table.find('.add-element').attr('disabled', true);
		table.find('.delete-element').attr('disabled', true);

		post_data(data);

	})

	.on('click', '.button.discard[field="table"]:not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		var table = get_el('table', annotation, 'table');
		var save = get_el('.button.save', annotation, 'table');

		table.find('td').each(function(_, value) {
			$(value).text($(value).attr('original'));
		});

		$(this).attr('disabled', true);
		save.trigger('click');

	})

	.on('change input paste keyup', 'td[annotation][field]', function() {

		var parent = $(this).attr('annotation').split('.').slice(0, -1).join('.');
		var field = $(this).attr('field');
		var val = $(this).text();
		var original = $(this).attr('original');
		var save = get_el('.button.save', parent, 'table');
		var discard = get_el('.button.discard', parent, 'table');

		if (val != original) {
			discard.removeAttr('disabled');
		} else {
			discard.attr('disabled', true);
		}

		if (field == 'annotation' && !val.startsWith(parent + '.')) {
			save.attr('disabled', true);
		} else {
			save.removeAttr('disabled');
		}

	})

	.on('click', '.add-element:not([disabled])', function() {

		var parent = $(this).attr('annotation');
		var table = get_el('table', parent, 'table');
		var body = 'table[annotation="{0}"] tbody'.format(parent);
		var last = table.find('tr').last().find('td').first().attr('annotation');
		var level = get_value(data_object=data, annotation=parent, field='_level');

		if (last === undefined) {
			var new_id = parent + '.added_0';
		} else {
			if (last.split('.').slice(-1)[0].startsWith('added_')) {
				var new_id = parent + '.added_' + (parseInt(last.split('.').slice(-1)[0].split('_')[1]) + 1).toString();
			} else {
				var new_id = parent + '.added_0';
			}
		}

		var new_obj = [{
			'title': new_id,
			'annotation': new_id,
			'type': '',
			'description': ''
		}];

		add_annotation(data, new_obj[0]);
		load_template('templates/tableRow.hbs', new_obj, body, 'append');

		get_el('td', new_id).attr('contenteditable', 'true').first().trigger('focus');
		get_el('td', new_id).last().find('a').removeAttr('disabled');

	})

	.on('click', '.delete-element:not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		load_template('templates/deleteModal.hbs', {'annotation': annotation}, '#delete-modal', 'append'); 
		$('#delete-modal').addClass('is-active');

	})

	.on('click', '.doc-jump', function() {
		get_el('.nav-tab', $(this).attr('annotation')).trigger('click');
	})

	.on('click', '#add-annotation', function() {
		$('#add-modal').addClass('is-active');
	})

	.on('change input paste keyup', 'input.add-field', function() {
		var fields = $('input.add-field');
		if ($(fields[0]).val() != '' && 
			$(fields[1]).val().startsWith('va.') && 
			$(fields[2]).val().startsWith('gs://annotationdb/') &&
			($(fields[2]).val().endsWith('.vds') ||
			 $(fields[2]).val().endsWith('.kt'))) {
			$('#confirm-add').removeAttr('disabled');
		} else {
			$('#confirm-add').attr('disabled', true);
		}
	})

	.on('click', '#confirm-add:not([disabled])', function() {

		var title = $('#add-title-input').val();
		var path = $('#add-annotation-input').val();
		var db_file = $('#add-dbfile-input').val();
		var parent = path.split('.').slice(0, -1).join('.');

		var new_annotation = [{
			'title': title,
			'annotation': path,
			'type': 'Struct',
			'db_file': db_file,
			'publication': '',
			'description': ''
		}];

		var match = $('.nav-tab').map(function() {
			return $(this).attr('annotation');
		}).filter(function() {
			return path.startsWith(this + '.');
		}).sort(function(a, b) {
			return b.length - a.length;
		})[0];

		if (match !== undefined) {
			load_template('templates/leftNav.hbs', new_annotation, get_el('.nav-tab', match), 'after');
			load_template('templates/leftNavContent.hbs', new_annotation, get_el('.tab', match), 'after');
		} else {
			load_template('templates/leftNav.hbs', new_annotation, '#left-nav', 'prepend');
			load_template('templates/leftNavContent.hbs', new_annotation, '#left-nav-content', 'prepend');
		}

		add_annotation(data, new_annotation[0]);
		post_data(data);

		$('#add-modal').removeClass('is-active');
		get_el('.nav-tab', path).trigger('click');

	})

	.on('click', '#cancel-add', function() {
		$('#add-modal').removeClass('is-active');
	})

	.on('click', '.delete-annotation', function() {
		var annotation = $(this).attr('annotation');
		load_template('templates/deleteModal.hbs', {'annotation': annotation}, '#delete-modal', 'append');
		$('#delete-modal').addClass('is-active');
	})

	.on('click', '#cancel-delete', function() {
		($('#delete-modal').removeClass('is-active')
						   .empty());
	})

	.on('click', '#confirm-delete:not([disabled])', function() {

		var annotation = $(this).attr('annotation');
		var nav = get_el('.nav-tab', annotation);
		var tab = get_el('.tab', annotation);

		if (nav.length) {
			nav.remove();
			tab.remove();
			$('.nav-tab:first-child').trigger('click');
		} else {
			get_el('.delete-element', annotation).parent().parent().remove();
		}
		delete_annotation(data, annotation);
		($('#delete-modal').removeClass('is-active')
						   .empty());
		post_data(data);
	}));

	$('.nav-tab:first-child').trigger('click');

});
