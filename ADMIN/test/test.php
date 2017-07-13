function get_data($url) {
    $ch = curl_init();
    $timeout = 5;
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    $data = curl_exec($ch);
    curl_close($ch);
    return $data;
}

function create_db($sql) {
    $db = new PDO('sqlite::memory:');
    $db->exec($sql);
    return $db;
}

$url = 'http://storage.googleapis.com/annotationdb/annotationdb.sql?ignoreCache=1';
$sql = get_data($url);
$db = create_db($sql);

$qry = <<<EOT
    SELECT annotation, "Struct" AS type
    FROM docs
    UNION ALL
    SELECT annotation, type
    FROM annotations
EOT;

$types = [];
foreach($db->query($qry) as $row) {
    $types[$row['annotation']] = $row['type'];
}

$qry = <<<EOT
    SELECT annotation, text, study_link, study_title, study_data, free_text, selectable
    FROM docs
EOT;

$docs = [];
foreach($db->query($qry) as $row) {
    $docs[$row['annotation']] = [
        'text' => $row['text'],
        'study_link' => $row['study_link'],
        'study_title' => $row['study_title'],
        'study_data' => $row['study_data'],
        'free_text' => $row['free_text'],
        'selectable' => $row['selectable']
    ];
}

$qry = <<<EOT
    SELECT annotation, type, description
    FROM annotations
EOT;

$annotations = [];
foreach($db->query($qry) as $row) {
    $annotations[$row['annotation']] = [
        'type' => $row['type'],
        'description' => $row['description']
    ];
}

$qry = <<<EOT
    WITH RECURSIVE doctree AS (
    
        WITH bridge_table AS (
            SELECT parent, annotation
            FROM docs
            UNION ALL
            SELECT parent, annotation
            FROM annotations
        )

        SELECT parent, annotation
        FROM bridge_table
        WHERE annotation = 'va'
        
        UNION ALL
        
        SELECT b.parent, b.annotation
        FROM bridge_table AS b INNER JOIN doctree AS t
            ON b.parent = t.annotation
    )

    SELECT DISTINCT parent, annotation
    FROM doctree
EOT;

$hierarchy = [];
foreach($db->query($qry) as $row) {
    $hierarchy[$row['parent']][] = $row['annotation'];
}

$nested = [];
$nested[] = ['annotation' => 'va'];

function build_tree(&$array) {
    global $docs;
    global $annotations;
    global $types;
    global $hierarchy;
    foreach ($array as $key => $value) {
        $a = $value['annotation'];
        if ($types[$a] != "Struct") {
            $array[$key]['type'] = $annotations[$a]['type'];
            $array[$key]['description'] = $annotations[$a]['description'];
            continue;
        }
        $new_nodes = [];
        foreach($hierarchy[$a] as $new_key => $new_value) {
            $new_nodes[] = ['annotation' => $new_value];
            unset($new_key);
            unset($new_value);
        }
        $array[$key]['text'] = $docs[$a]['text'];
        $array[$key]['study_link'] = $docs[$a]['study_link'];
        $array[$key]['study_data'] = $docs[$a]['study_data'];
        $array[$key]['study_title'] = $docs[$a]['study_title'];
        $array[$key]['free_text'] = $docs[$a]['free_text'];
        $array[$key]['selectable'] = $docs[$a]['selectable'];
        $array[$key]['nodes'] = $new_nodes;
        build_tree($array[$key]['nodes']);
    }
}

build_tree($nested);
print_r($nested);


$array[$key] = array_flip($hierarchy[$value]);

foreach($db->query($qry) as $row) {
    if ($row['is_struct'] === '0') {
        $nested[$row['parent']] = null;
    } else {
        $links[$row['parent']][] = $row['annotation'];
    }
}

/*$links[$row['parent']][] = $row['annotation'];*/

$new_array = [];
foreach($results as $key => $value) {
    $split = explode('.', preg_replace('/^va\./', '', $value['annotation']));
    foreach($split => $x) {
        $array = $array[$value['annotation']]
    }
}

function sort_depth($a, $b) {
    return ($a['depth'] < $b['depth'] ? 1 : -1);
}

usort($results, "sort_depth");

$qry = 'SELECT * FROM docs';
$docs = [];
foreach ($db->query($qry) as $row) {
    $docs[$row['annotation']] = array(
        'text' => $row['text'],
        'study_link' => $row['study_link'],
        'study_title' => $row['study_title'],
        'study_data' => $row['study_data'],
        'free_text' => $row['free_text'],
        'parent' => $row['parent']
    );
}

$qry = 'SELECT annotation, type, description FROM annotations';
$annotations = [];
foreach($db->query($qry) as $row) {
    $annotations[$row['annotation']] = array(
        'type' => $row['type'],
        'description' => $row['description']
    );
}

ksort($docs);
ksort($annotations);

$qry = 'SELECT * FROM docs AS a INNER JOIN docs AS b ON a.annotation = b.parent';
$results = $db->query($qry)->fetchAll();


function make_array($annotation, $array, $root) {
    $new_root = implode('.', array_slice(explode('.', $annotation), $length=$depth-1));
    if ($new_root === $root) {
        make_array($annotation=$annotation, $array=$array[$root], $root=$new_root);
    }
    return $array[] = [$annotation];
}

//function split_annotations(&$value, $key) {
//    $value = explode('.', $key);
//}

function split_annotations(&$value, $key) {
    $split = $explode('.', $key);
    if (count($split) > 1) {
        $new_value = implode('.', array_slice($split, $offset=1));
        $new_key = 
        split_annotations(implode('.', array_slice($split, $offset=1)), $split[0]);
    }
    $value = $split;
}

$levels = $docs;
array_walk($levels, "split_annotations");
print_r($levels);

$new_array = [];
foreach($levels as $key => $value) {
    foreach($value as $v) {
        if (array_key_exists($v)
}



$new_array = [];

$current_root = 'va';
$last_common_branch = '';
$previous = '';
foreach($docs as $k => $v) {
    //$root = preg_replace('/\.[A-Za-z0-9]+$/', '', preg_replace('/^va\./', '', $k));
    $k_split = explode('.', $k);
    $depth = count($k_split);
    $root = implode('.', array_slice($k_split, $length=$depth-1));
    if ($root === $current_root) {
        try {
            $new_array[$previous]['nodes'][] = array(
                'annotation' => $k
            );
        } catch (Exception $e) {
            echo "Exception: ", $e->getMessage(), "\n";
        }
    } elseif (substr($k, 0, strlen($current_root)) === $current_root) {
        echo "Yes", "\n";
        $previous = $k;
    } else {
        $new_array[$k] = array(
            'annotation' => $k
        );
        $previous = $k;
    }
    $current_root = $root;
}

$new_array = [];
foreach($docs as $k => $v) {
    
}

function build_array($annotation, $root, $new_array) {
    $new_root = 'va.' . preg_replace('/\.[A-Za-z0-9]+$/', '', preg_replace('/^va\./', '', $annotation));
    if ($new_root === $root) {

    }
    $new_array[$annotation] = $annotation;
    $root = $new_root;
}












$docs = $db->query($qry)->fetchAll();

function custom_sort($a, $b) {
    return strcmp($a['annotation'], $b['annotation']);
}
usort($docs, "custom_sort");

$qry = 'SELECT annotation FROM annotations';
$annotations = $db->query($qry).fetchAll();

$annotations = array_column($docs, 'annotation');

$nested_array = [];

function build_hierarchy($annotations, $previous_annotation) {
    foreach($annotations as $current) {
        $current_split = explode('.', $current);
        $previous_split = explode('.', $previous);
        $i = 0;
        while (true) {
            if ($current_split[$i] !== $previous_split[$i]) {
                break;
            }
            $i += 1;
        }
        $array = $nested_array;
        for ($x = 0; $x < i; $x++) {
            $array = $array[$current_split[$x]];
        }
        $array[$current] = $current_split;
    }
}

build_array($docs, $previous_root = 'va', $previous_annotation = '', $current_array = $nested_array);


$nested_array = [];

function build_array($doc_set, $previous_root, $previous_annotation, $current_array) {
    foreach($docs as $d) {
        $annotation = $d['annotation'];
        $text = $d['text'];
        $study_link = $d['study_link'];
        $study_title = $d['study_title'];
        $study_data = $d['study_data'];
        $free_text = $d['free_text'];
        $add = array(
            'annotation' => $annotation, 
            'text' => $text,
            'study_link' => $study_link,
            'study_title' => $study_title,
            'study_data' => $study_data,
            'free_text' => $free_text
        );
        $root = preg_replace('/.[A-Za-z0-9]+$/', '', $annotation);
        if ($root === $previous_annotation) {
            $new_array = $current_array[$previous_annotation]['nodes'];
            $new_array[$annotation] = $add;
        } elseif ($root === $previous_root) {}
        else {
            $new_array = $nested_array;
        }
    }
}
$previous = '';
foreach($docs as $d) {
    $annotation = $d['annotation'];
    $text = $d['text'];
    $study_link = $d['study_link'];
    $study_title = $d['study_title'];
    $study_data = $d['study_data'];
    $free_text = $d['free_text'];
    $add = array(
        'annotation' => $annotation, 
        'text' => $text,
        'study_link' => $study_link,
        'study_title' => $study_title,
        'study_data' => $study_data,
        'free_text' => $free_text
    );
    if (substr($annotation, 0, strlen($previous)) === $previous) {
        $nested_array[$previous][$nodes][] = 
    }
    $nested_array[$annotation] = $add;
}

$json_array = json_encode($nested_array);

