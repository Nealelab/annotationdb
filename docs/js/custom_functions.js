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

function load_template(path, data, target, method) {
	$.ajax({
		url: path,
		cache: false,
		async: false,
		success: function(template) {
			compiled = Handlebars.compile(template);
			rendered = compiled(data);
			if (method == 'html') {
				$(target).html(rendered);
			} else if (method == 'prepend') {
				$(target).prepend(rendered);
			} else if (method == 'append') {
				$(target).append(rendered);
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
		url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb-submit/o?name=tree.json',
		data: JSON.stringify(data),
		contentType: 'application/json',
		dataType: 'json'
	});
	$.ajax({
		type: 'POST',
		url: 'https://www.googleapis.com/upload/storage/v1/b/annotationdb-submit/o?name=tree.json.bak',
		data: JSON.stringify(data),
		contentType: 'application/json',
		dataType: 'json'
	});
}
