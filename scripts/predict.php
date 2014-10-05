<?php
function cmp($a, $b) {
    $ca = count($a);
    $cb = count($b);
    if ($ca == $cb) {
        return 0;
    } else if ($ca < $cb) {
        return -1;
    } else {
        return 1;
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
    } else if (array_search($word, $matches)) {
        $ans = $word;
    } else {
        $ans = $matches[0];
    }

    if (strtoupper($orig) == $orig) {
        $ans = strtoupper($ans);
    } else if (ucwords($orig) == $orig) {
        $ans = ucwords($ans);
    }

    $ans = preg_replace('/' . preg_quote($word, '/') . '/', $ans, $orig);

    $response = ['orig' => $orig, 'comp' => $ans ];
    print json_encode($response);
} else {
    header($_SERVER['SERVER_PROTOCOL'] . ' 204 No Content');
}
?>
