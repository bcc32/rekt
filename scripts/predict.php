<?php
function mismatches($a, $b) {
    $num = 0;
    $la = strlen($a);
    $lb = strlen($b);
    for ($i = 0; $i < $la and $i < $lb; $i++) {
        if ($a[$i] != $b[$i]) {
            $num++;
        }
    }
    return $num;
}

function cmp($a, $b) {
    $ca = strlen($a);
    $ma = mismatches($a, $GLOBALS['word']);
    $cb = strlen($b);
    $mb = mismatches($b, $GLOBALS['word']);
    if ($ma < $mb) {
        return -1;
    } else if ($ma > $mb) {
        return 1;
    } else if ($ca < $cb) {
        return -1;
    } else if ($ca > $cb) {
        return 1;
    } else {
        return 0;
    }
}

require dirname(__FILE__) . '/errors.php';
header('Access-Control-Allow-Origin: http://web.mit.edu');
$file_name = dirname(__FILE__) . '/../../www/rekt/data/cleaned_up.txt';
$dict = fopen($file_name, 'r');
$orig = $_REQUEST["word"];
$word = strtolower($orig);
$word = preg_replace('/[^a-z]/', '', $word);
if (strlen($word) > 0) {
    $pattern = '/^';
    foreach (str_split($word) as $ch) {
        $pattern .= '[' . $ch . $errors[$ch] . ']';
    }
    if (array_key_exists('strict', $_REQUEST) && $_REQUEST['strict']) {
        $pattern .= '$';
    }
    $pattern .= '/';

    $matches = [];

    while (!feof($dict)) {
        $try_this = chop(fgets($dict));
        if (preg_match($pattern, $try_this)) {
            array_push($matches, $try_this);
        }
    }
    $ans = 'teapot';
    usort($matches, 'cmp');
    if (count($matches) == 0) {
        header($_SERVER['SERVER_PROTOCOL'] . ' 418 I\'m a teapot');
    } else {
        $ans = $matches[0];
    }

    if (strtoupper($orig) == $orig) {
        $ans = strtoupper($ans);
    } else if (ucwords($orig) == $orig) {
        $ans = ucwords($ans);
    }

    $ans = str_ireplace($word, $ans, $orig);

    $response = ['orig' => $orig, 'word' => $word, 'comp' => $ans ];
    print json_encode($response);
} else {
    header($_SERVER['SERVER_PROTOCOL'] . ' 204 No Content');
}
fclose($dict);
?>
