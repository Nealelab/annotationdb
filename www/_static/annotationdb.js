
function gen_command(selected_hail) {
	if (selected_hail.length) {
			
		$( 'span.hail-code.query ').empty();
		$( 'span.hail-code.query ').removeClass('placeholder');
		$( 'span.hail-code.query ').addClass('active-qry');
				
		var query = '<pre>' + 
				    'import_annotations_db(' + 
				    '<br>' +
					"    '" + selected_hail.join("',<br>    '") +
					"'<br>" +
					')' +
					'</pre>';

		$( 'span.hail-code.query ').html(query);
				
	} else {
			
		$( 'span.hail-code.query ').empty();
		$( 'span.hail-code.query ').removeClass('active-qry');
		$( 'span.hail-code.query ').addClass('placeholder');
		$( 'span.hail-code.query ').text('');
	}
}

function build_tree(data) {
	$('#tree').treeview({
		data: data,
		multiSelect: true,
		levels: 1,
		expandIcon: 'glyphicon-plus',
		collapseIcon: 'glyphicon-minus',
		onNodeSelected: function(node_event, node) {
			var selected_nodes = $('#tree').treeview('getSelected', node);
			var selected_hail = $.map(selected_nodes, function(value, index) {
				return value['hail'];
			});
			var parent = $('#tree').treeview('getParent', node);
			$('#tree').treeview('selectNode', node.nodeId);
			
			/* -- SELECT ALL CHILDREN WHEN PARENT SELECTED --
			$.each(node['nodes'], function(child_index, child) {
				$('#tree').treeview('selectNode', child.nodeId);
				selected_hail.push(child['hail']);
				if (child_index == 1) {
					var parent = $('#tree').treeview('getParent', child);
					selected_hail.splice( $.inArray(parent['hail'], selected_hail), 1);
				}
			});
			*/
			
			gen_command(selected_hail);
		},
		onNodeUnselected: function(event, node) {
			var selected_nodes = $('#tree').treeview('getSelected', node);
			var selected_hail = $.map(selected_nodes, function(value, index) {
				return value['hail'];
			});
			
			/* -- UNSELECT CHILDREN WHEN PARENT UNSELECTED --
			$.each(node['nodes'], function(child_event, child) {
				$('#tree').treeview('unselectNode', child.nodeId);
				selected_hail.splice( $.inArray(child['hail'], selected_hail), 1);
			});
			*/

			gen_command(selected_hail);
		}
	});
}

function build_doc_group(node, parent_id_string, parent_level) {
	var name = node['text'];
	var current_id = node['id'];
	var current_id_string = parent_id_string + '-' + current_id;
	var current_level = parent_level + 1;
	var margin = (current_level * 10).toString() + 'px';
	if (node.hasOwnProperty('nodes')) {
		var panel = '<div class="panel panel-default" style="margin-left: ' + margin + '; margin-right: ' + margin + '">' +
		       		    '<div class="panel-heading" id="' +  current_id_string + '-heading">' +
		           			'<a role="button" data-toggle="collapse" href="#' + current_id_string + '">' +
				       			'<span class="text-expand">' + name + '</span>' +
				   			'</a>' +
			   			'</div>' +
			   			'<div class="panel-collapse collapse" id="' + current_id_string + '">' +
			      			'<div class="panel-body">' +
							'</div>' +
				   		'</div>' +
			   		'</div>';
		$('#' + parent_id_string).append(panel);
		if (node['nodes'][0].hasOwnProperty('nodes')) {
			$.each(node['nodes'], function(new_index, new_node) {
				build_doc_group(node=new_node, parent_id_string=current_id_string, parent_level=current_level);
			});
		} else {
			
			var study_title = node['study_title'];
			var study_link = node['study_link']
			if (study_title && study_link) {
				$('#' + current_id_string + '>.panel-body').append(
					'<div class="panel-text">' + 
					   '<a href="' + study_link + '" target="_blank">' + study_title + '</a>' +
					'</div>'
				);
			}
			
			var study_data = node['study_data'];
			if (study_data) {
				$('#' + current_id_string + '>.panel-body').append(
					'<div class="panel-text">' +
					   '<a href="' + study_data + '" target="_blank">Raw data download</a>' +
					'</div>'
				);
			}

			var table_outline = '<table class="table table-hover">' +
								 	'<thead>' + 
										'<th>Variable</th>' +
										'<th>Type</th>' +
										'<th>Description</th>' +
									'</thead>' +
									'<tbody>' +
									'</tbody>' +
								'</table>'
			$('#' + current_id_string + '>.panel-body').append(table_outline);
			
			$.each(node['nodes'], function(index, val) {
				var variable = val['hail'];
				var type = val['type'];
				var description = val['description'];
				var row = '<tr>' +
						     '<td><span class="hail-code">' + variable + '</span></td>' +
							 '<td>' + type + '</td>' +
							 '<td>' + description + '</td>' +
						  '</tr>'
				$('#' + current_id_string + '>.panel-body tbody').append(row);
			});
		}
	} 

}

function build_docs(data) {
	id_string = 'panel-docs';
	level = -1;
	$.each(data, function(index, node) {
		build_doc_group(node, id_string, level);
	});
}
	
$.ajax({
	url: 'https://storage.googleapis.com/hail-annotation/annotationdb.json',
	method: 'GET',
	dataType: 'json',
	cache: false,
	beforeSend: function(request) {
		request.setRequestHeader('access-control-expose-headers', 'access-control-allow-origin');
		request.setRequestHeader('access-control-allow-origin', '*');
	},
	success: function(data) {
		build_tree(data);
		build_docs(data);
	},
	error: function() {
		window.alert('Error fetching tree file!');
	}
});

$('#annotations-clear').on('click', function() {
	var tree = $('#tree').treeview(true);
	tree.unselectNode(tree.getSelected());
});

var hail_copy_btn = document.getElementById('hail-copy-btn');
var clipboard = new Clipboard(hail_copy_btn);

clipboard.on( 'success', function(e) {
});

clipboard.on( 'error', function(e) {
});
