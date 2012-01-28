<?php 

// escaping and slashing all POST and GET variables. you may add $_COOKIE and $_REQUEST if you want them sanitized. 
array_walk_recursive($_POST, 'sanitizeVariables'); 
array_walk_recursive($_GET, 'sanitizeVariables'); 

// sanitization 
function sanitizeVariables(&$item, $key) 
{ 
    if (!is_array($item)) 
    { 
        // undoing 'magic_quotes_gpc = On' directive 
        if (get_magic_quotes_gpc()) 
            $item = stripcslashes($item); 
        
        $item = sanitizeText($item); 
    } 
} 

// does the actual 'html' and 'sql' sanitization. customize if you want. 
function sanitizeText($text) 
{ 
    $text = str_replace("<", "&lt;", $text); 
    $text = str_replace(">", "&gt;", $text); 
    $text = str_replace("\"", "&quot;", $text); 
    $text = str_replace("'", "&#039;", $text); 
    
    // it is recommended to replace 'addslashes' with 'mysql_real_escape_string' or whatever db specific fucntion used for escaping. However 'mysql_real_escape_string' is slower because it has to connect to mysql. 
    $text = addslashes($text); 

    return $text; 
} 

// export POST variables as GLOBALS. remove if you want 
foreach (array_keys($_POST) as $ehsanKey) 
    $GLOBALS[$ehsanKey] = $_POST[$ehsanKey]; 

// export GET variables as GLOBALS. remove if you want 
foreach (array_keys($_GET) as $ehsanKey) 
{ 
    $GLOBALS[$ehsanKey] = $_GET[$ehsanKey]; 
} 

// preventing the key used above for iteration from getting into globals (in case  'register_globals = On') 
unset($ehsanKey); 

// the reverse function of 'sanitizeText'. you may use it in pages which need the original data (e.g. for an HTML editor) 
function unsanitizeText($text) 
{ 
    $text =  stripcslashes($text); 

    $text = str_replace("&#039;", "'", $text); 
    $text = str_replace("&gt;", ">", $text); 
    $text = str_replace("&quot;", "\"", $text);    
    $text = str_replace("&lt;", "<", $text); 
    
    return $text; 
} 
?>