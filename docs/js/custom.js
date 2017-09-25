$.getJSON('data/tree.json', function(data) {
	data = $.map(data, function(element, index) {
		element['isFirst'] = false;
		return element;
	});
	data[0]['isFirst'] = true;
	render_left_nav(data);
	render_left_nav_content(data);
});

function render_left_nav(data) {
	var template = $('#script-left-nav').html();
	var compiled = Handlebars.compile(template);
	var rendered = compiled(data);
	$('#left-nav').html(rendered);
	$('#left-nav>a:first-child').addClass('active');
}

function render_left_nav_content(data) {
	var template = $('#script-left-nav-content').html();
	var compiled = Handlebars.compile(template);
	var rendered = compiled(data);
	$('#left-nav-content').html(rendered);
	$('#left-nav-content>div:first-child').addClass('show active');
	/*$('.text-button.edit').on('click', function() {
		$(this).removeClass('edit');
		$(this).addClass('save');
		$(this).removeClass('btn-warning');
		$(this).addClass('btn-success');
		var target = $(this).attr('href');
		$(target).removeClass('form-control-plaintext');
		$(target).addClass('form-control');
		$(target).removeAttr('readonly');
	});
	$('.text-button.save').on('click', function() {
		$(this).removeClass('save');
		$(this).addClass('edit');
		$(this).removeClass('btn-success');
		$(this).addClass('btn-warning');
		var target = $(this).attr('href');
		$(target).removeClass('form-control');
		$(target).addClass('form-control-plaintext');
		$(target).attr('readonly');
	});*/
}

Handlebars.registerHelper('makeID', function(annotation) {
	return annotation.replace('va.', '').replace('.', '-');
});

$(document).on('click', '.text-button.edit', function() {
	$(this).removeClass('edit');
	$(this).addClass('save');
	$(this).removeClass('btn-warning');
	$(this).addClass('btn-success');
	var target = $(this).attr('href');
	$(target).removeClass('locked');
	$(target).removeAttr('readonly');
	$(this).find('i').removeClass('fa-pencil');
	$(this).find('i').addClass('fa-floppy-o');
	$(this).find('span').html('&nbsp; Save');
});

$(document).on('click', '.text-button.save', function() {
	$(this).removeClass('save');
	$(this).addClass('edit');
	$(this).removeClass('btn-success');
	$(this).addClass('btn-warning');
	var target = $(this).attr('href');
	$(target).addClass('locked');
	$(target).attr('readonly', true);
	$(this).find('i').removeClass('fa-floppy-o');
	$(this).find('i').addClass('fa-pencil');
	$(this).find('span').html('&nbsp; Edit');
});

