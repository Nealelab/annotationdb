function load_partial(name, path) {
	$.ajax({
		url: path,
		cache: false,
		async: false,
		success: function(template) {
			Handlebars.registerPartial(name, template);
		}
	});
}

function load_template(path, data_object, target, method) {
	$.ajax({
		url: path,
		cache: false,
		async: false,
		success: function(template) {
			compiled = Handlebars.compile(template, {preventIndent: true});
			rendered = compiled(data_object);
			if (method == 'html') {
				$(target).html(rendered);
			} else if (method == 'prepend') {
				$(target).prepend(rendered);
			} else if (method == 'append') {
				$(target).append(rendered);
			} else if (method == 'after') {
				$(target).after(rendered);
			} else if (method == 'before') {
				$(target).before(rendered);
			}
		}
	});
}

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

function change_value(data_object, annotation, field, new_value) {
	for (var i=0; i<data_object.length; i++) {
		if (data_object[i].annotation == annotation) {
			data_object[i][field] = new_value;
			break;
		}
	}
}

function get_value(data_object, annotation, field) {
	for (var i=0; i<data_object.length; i++) {
		if (data_object[i].annotation == annotation) {
			return data_object[i][field];
		}
	}
}

function add_annotation(data_object, annotation_object) {
	var parent = annotation_object.annotation.split('.').slice(0,-1).join('.');
	if (parent == 'va') {
		data_object.splice(0, 0, annotation_object)
	} else {
		for (var i=0; i<data_object.length; i++) {
			if (data_object[i].annotation == parent) {
				data_object.splice(i+1, 0, annotation_object);
				break;
			}
		}
	}
}

function delete_annotation(data_object, annotation) {
	for (var i=0; i<data_object.length; i++) {
		if (data_object[i].annotation == annotation) {
			data_object.splice(i, 1);
			break;
		}
	}
}

function post_data(data) {
	$.ajax({
		type: 'POST',
		url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb/o?name=tree.json',
		data: JSON.stringify(data),
		contentType: 'application/json',
		dataType: 'json'
	});
}

function get_el(custom, annotation='', field='') {
	var out = custom;
	if (annotation != '') {
		out = out + '[annotation="' + annotation + '"]';
	}
	if (field != '') {
		out = out + '[field="' + field + '"]';
	}
	return $(out);
}
