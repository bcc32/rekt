<?php
require dirname(__FILE__) . '/errors.php';
header('Access-Control-Allow-Origin: http://web.mit.edu');
$file_name = dirname(__FILE__) . '/../../www/rekt/data/cleaned_up.txt';
$dict = fopen($file_name, 'r');
$orig = $_REQUEST["word"];
$word = strtolower($orig);
if (strlen($word) > 0) {
    $pattern = '/^';
    foreach (str_split($word) as $ch) {
        if ($ch >= 'a' and $ch <= 'z') {
            $pattern .= '[' . $ch . $errors[$ch] . ']';
        }
    }
    $pattern .= '/';
    $something_found = false;
    while (!feof($dict)) {
        $try_this = chop(fgets($dict));
        if (preg_match($pattern, $try_this)) {
            if (strtoupper($orig) == $orig) {
                $try_this = strtoupper($try_this);
            } else if (ucwords($orig) == $orig) {
                $try_this = ucwords($try_this);
            }
            $response = ['orig' => $orig, 'comp' => $try_this];
            print json_encode($response);
            $something_found = true;
            break;
        }
    }
    if (!$something_found) {
        header($_SERVER['SERVER_PROTOCOL'] . ' 418 I\'m a teapot');
        $response = ['orig' => $word];
        print json_encode($response);
    }
} else {
    header($_SERVER['SERVER_PROTOCOL'] . ' 204 No Content');
}
?>
