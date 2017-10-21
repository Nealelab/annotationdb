// when getJSON promise is fulfilled, use the data to fill in Handlebars templates
$.when(
	$.ajax({
		dataType: 'json',
		method: 'GET',
		url: 'https://storage.googleapis.com/annotationdb-submit/tree.json',
		cache: false
	})
).done(function(data) {

	// add levels; e.g. va.cadd => level 0, va.cadd.PHRED => level 1; used to format the padding on the left nav
	add_levels(data, 0);

	load_partial('templates/leftNavPartial.hbs', 'leftNavPartial');
	load_partial('templates/leftNavContentPartial.hbs', 'leftNavContentPartial');
	load_partial('templates/leftNavPartialAdd.hbs', 'leftNavPartialAdd');

	// compile Handlebars templates, insert data, add to DOM
	load_template(path='templates/leftNav.hbs', data=data, target='#left-nav', method='html');
	load_template(path='templates/leftNavContent.hbs', data=data, target='#left-nav-content', method='html');

	($(document)

	.on('click', '.nav-tab', function() {

		var target = $('.tab[annotation="{0}"]'.format($(this).attr('annotation')));
		
		$('.nav-tab').removeClass('show');
		$('.tab').removeClass('show');
		$(this).addClass('show');
		target.addClass('show');

		target.find('textarea').each(function(_, value) {
			autosize_textarea(value);
		});

	})

	.on('click', '.breadcrumb-link', function() {
		$('.nav-tab[annotation="{0}"]'.format($(this).attr('annotation'))).trigger('click');
	})

	.on('click', '.button.edit:not([field="table"])', function() {
		($(this).removeClass('is-warning')
				.removeClass('edit')
				.addClass('is-success')
				.addClass('save')
				.text('Save'));
		($('textarea[annotation="{0}"][field="{1}"]'.format($(this).attr('annotation'), $(this).attr('field'))).removeAttr('readonly')
																											   .removeClass('locked')
																											   .trigger('focus'));
	})

	.on('click', '.button.save:not([field="table"])', function() {

		var annotation = $(this).attr('annotation');
		var field = $(this).attr('field');
		var id = '[annotation="{0}"][field="{1}"]'.format(annotation, field);
		var textarea = $('textarea{0}'.format(id));

		($(this).removeClass('is-success')
				.removeClass('save')
				.addClass('is-warning')
				.addClass('edit')
				.text('Edit'));


		$('.button.discard{0}'.format(id)).attr('disabled', true);
		
		(textarea.attr('readonly', true)
		 		 .addClass('locked'));

		if (get_value(data, annotation, field, '') != textarea.val()) {
			change_value(data, annotation, field, textarea.val());
			textarea.attr('original', textarea.val());
			post_data(data);
		}

	})

	.on('change input paste keyup', 'textarea', function() {
		var btn = $('.button.discard[annotation="{0}"][field="{1}"]'.format($(this).attr('annotation'), $(this).attr('field')));
		if ($(this).val() != $(this).attr('original')) {
			btn.removeAttr('disabled');
		} else {
			btn.attr('disabled', true);
		}
	})

	.on('change input paste keyup', 'textarea[field="title"]', function() {
		var tab = $('.nav-tab[annotation="{0}"]'.format($(this).attr('annotation')));
		if (tab.text() != $(this).val()) {
			tab.text($(this).val());
		}
	})

	.on('click', '.button.discard:not([field="table"])', function() {
		var id = '[annotation="{0}"][field="{1}"]'.format($(this).attr('annotation'), $(this).attr('field'));
		($('textarea{0}'.format(id)).val($('textarea{0}'.format(id)).attr('original'))
								    .trigger('change'));
		$('.button.save{0}'.format(id)).trigger('click');
	})

	.on('click', '.button.edit[field="table"]', function() {

		($(this).removeClass('is-warning')
				.removeClass('edit')
				.addClass('is-success')
				.addClass('save')
				.text('Save'));

		var target = $('table[annotation="{0}"][field="table"]'.format($(this).attr('annotation')));
		target.find('td:not(:last-child)').attr('contenteditable', 'true');
		target.find('tbody tr:first-child td:first-child').trigger('focus');
		target.find('.add-element').removeAttr('disabled');
		target.find('.delete-element').removeAttr('disabled');
	})

	.on('click', '.button.save[field="table"]', function() {

		($(this).removeClass('is-success')
				.removeClass('save')
				.addClass('is-warning')
				.addClass('edit')
				.text('Edit'));

		var annotation = $(this).attr('annotation');
		var id = '[annotation="{0}"][field="table"]'.format(annotation);

		$('.button.discard{0}'.format(id)).attr('disabled', true);
		$('table{0} td'.format(id)).each(function(_, value) {
			change_value(data, $(this).attr('annotation'), $(this).attr('field'), $(this).text());
			$(this).attr('original', $(this).text());
		});
		$('table{0} .add-element'.format(id)).attr('disabled', true);
		$('table{0} .delete-element'.format(id)).attr('disabled', true);
		post_data(data);

	})

	.on('click', '.add-element', function() {
		$('table[annotation="' + $(this).attr('annotation') + '"][field="table"] tbody').append([
			'<tr>',
			'<td contenteditable="true" annotation="" field="annotation" original=""></td>',
			'<td contenteditable="true" annotation="" field="type" original=""></td>',
			'<td contenteditable="true" annotation="" field="description" original=""></td>',
			'<td>', '<a class="button delete-element" annotation=""><i class="fa fa-minus"></i></a>', '</td>',
			'</tr>'
		].join(''));
		$('table[annotation="' + $(this).attr('annotation') + '"][field="table"] tbody tr:last-child td:first-child').trigger('focus');
	})

	.on('click', '.delete-element', function() {
		$(this).parent().parent().remove();
	})

	.on('change input paste keyup', 'table[field="table"] td', function() {
		var btn = $('.button.discard[annotation="' + $(this).attr('annotation').split('.').slice(0,-1).join('.') + '"][field="table"]');
		if ($(this).text() != $(this).attr('original')) {
			btn.removeAttr('disabled');
		} else {
			btn.attr('disabled', true);
		}
	})

	.on('click', '.button.discard[field="table"]', function() {
		var id = '[annotation="{0}"][field="table"]'.format($(this).attr('annotation'));
		$('table{0} td:not(:has(a))'.format(id)).each(function(_, value) {
			$(this).text($(this).attr('original'));
			$(this).trigger('change');
		});
		$(this).attr('disabled', true);
		$('.button.save{0}'.format(id)).trigger('click');
	})

	.on('click', '.doc-jump', function() {
		$('.nav-tab[annotation="' + $(this).attr('annotation') + '"]').click();
	})

	.on('change input paste keyup', 'textarea[field="annotation"]', function() {
		$('[annotation="{0}"]'.format($(this).attr('annotation'))).attr('annotation', $(this).val());
	})

	.on('change input paste keyup', 'td[field="annotation"]', function() {
		$('.nav-tab[annotation="{0}"]'.format($(this).attr('annotation'))).attr('annotation', $(this).text());
		$(this).parent().find('td:not(:last-child)').attr('annotation', $(this).text());
	})

	.on('click', '#add-annotation', function() {
		$('#add-modal').addClass('is-active');
	})

	.on('change input paste keyup', 'input.add-field', function() {
		var fields = $('input.add-field');
		if ($(fields[0]).val() != '' && $(fields[1]).val().startsWith('va.')) {
			$('#confirm-add').removeAttr('disabled');
		} else {
			$('#confirm-add').attr('disabled', true);
		}
	})

	.on('click', '#confirm-add', function() {
		
		var title = $('#add-title-input').val();
		var path = $('#add-annotation-input').val();
		
		var new_annotation = [{
			'level': 0,
			'title': title,
			'annotation': path,
			'db_file': '',
			'db_key': '',
			'db_element': '',
			'publication': '',
			'publication_link': '',
			'data_source': '',
			'description': '',
			'nodes': ['']
		}];

		load_template(path='templates/leftNav.hbs', data=new_annotation, target='#left-nav', method='prepend');
		load_template(path='templates/leftNavContent.hbs', data=new_annotation, target='#left-nav-content', method='prepend');

		data.push(new_annotation[0]);
		post_data(data);

		$('.nav-tab:first-child').click();
		$('#add-modal').removeClass('is-active');
	})

	.on('click', '#cancel-add', function() {
		$('#add-modal').removeClass('is-active');
	})

	.on('click', '#delete-annotation', function() {
		load_template(path='templates/deleteModal.hbs', data={'selected': $('.nav-tab.show').attr('annotation')}, target='#delete-modal', method='append');
		$('#delete-modal').addClass('is-active');
	})

	.on('click', '#cancel-delete', function() {
		($('#delete-modal').removeClass('is-active')
						   .empty());
	})

	.on('click', '#confirm-delete', function() {
		var annotation = $(this).attr('annotation');
		$('.nav-tab[annotation="' + annotation + '"]').remove();
		$('.tab[annotation="' + annotation + '"]').remove();
		$('.nav-tab:first-child').trigger('click');
		($('#delete-modal').removeClass('is-active')
						   .empty());
		data = data.filter(function(x) {
			return x.annotation != annotation;
		});
		post_data(data);
	}))

	// trigger the first annotation tab
	$('.nav-tab:first-child').trigger('click');

});
