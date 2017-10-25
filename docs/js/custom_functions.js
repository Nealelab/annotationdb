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

function add_levels(data, current_level) {
	$.each(data, function(index, value) {
		value['_level'] = current_level;
		if (value.hasOwnProperty('nodes')) {
			add_levels(value['nodes'], current_level + 1);
		}
	});
}

function change_value(data_object, annotation, field, new_value) {
	$.each(data_object, function(_, value) {
		if (value.annotation == annotation) {
			value[field] = new_value;
			return false
		} else {
			if (value.hasOwnProperty('nodes')) {
				change_value(value.nodes, annotation, field, new_value);
			}
		}
	});
}

function get_value(data_object, match_annotation, field) {
	var out;
	for (var i=0; i<data_object.length; i++) {
		if (data_object[i].annotation == match_annotation) {
			return data_object[i][field];
		} else {
			if (data_object[i].hasOwnProperty('nodes')) {
				out = get_value(data_object[i].nodes, match_annotation, field);
				if (out) {
					return out;
				}
			}
		}
	}
	return out;
}

function add_annotation(data_object, parent, new_annotation) {
	if (parent == 'va') {
		data_object.push(new_annotation);
	} else {
		$.each(data_object, function(_, value) {
			if (value.annotation == parent) {
				value.nodes.push(new_annotation);
				return false;
			} else {
				if (value.hasOwnProperty('nodes')) {
					add_annotation(value.nodes, parent, new_annotation);
				}
			}
		});
	}
}

function delete_annotation(data_object, annotation) {
	$.each(data_object, function(i, value) {
		if (value.annotation == annotation) {
			data_object.splice(i, 1);
			return false;
		} else if (value.hasOwnProperty('nodes')) {
			delete_annotation(value.nodes, annotation);
		}
	});
}

function post_data(data) {
	$.ajax({
		type: 'POST',
		url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb-submit/o?name=tree.json',
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

function sort_data(data_object) {
	$.each(data_object)
}
