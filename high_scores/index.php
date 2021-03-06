<?php
/* This file handles the high scores storing on the webserver.
 * 
 * --------------------------------------------------------------------------------
 * "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
 * Phyks (webmaster@phyks.me) wrote or updated these files for hackEns. As long
 * as you retain this notice you can do whatever you want with this stuff 
 * (and you can also do whatever you want with this stuff without retaining it, 
 * but that's not cool...).
 *
 * If we meet some day, and you think this stuff is worth it, you can buy us a 
 * <del>beer</del> soda in return.
 *                                                              Phyks for hackEns
 * ---------------------------------------------------------------------------------
 */

$api_key = "API_KEY";
//===================

function sort_array(&$array, $key) {
    $sort_keys = array();

    foreach ($array as $key2 => $entry) {
        $sort_keys[$key2] = $entry[$key];
    }


    return array_multisort($sort_keys, SORT_DESC, $array);
}

if(empty($_GET['do']) || ($_GET['do'] != 'add' && $_GET['do'] != 'get')) {
    exit('ERROR : Invalid request.');
}

// Sending API
if($_GET['do'] == 'add' && !empty($_GET['api_key']) && !empty($_GET['nick']) && isset($_GET['score'])) {
    if($_GET['api_key'] == $api_key) {
        // Send a 403 HTTP response (access forbidden) if api_key not valid
        header('HTTP/1.1 403 Forbidden');
        exit('ERROR : Wrong api key.');
    }

    $data = array();
    if(is_file('data/scores.dat')) {
        $data = json_decode(gzinflate(file_get_contents('data/scores.dat')), true);
    }

    $data[] = array(
        'nick' => $_GET['nick'],
        'score' => intval($_GET['score']),
    );

    sort_array($data, 'score');

    file_put_contents('data/score.dat', gzdeflate(json_encode($data)));
    exit('Success');
}

// Getting API
if($_GET['do'] == 'get') {
    // Fetch data
    $data = array();
    if(is_file('data/scores.dat')) {
        $data = json_decode(gzinflate(file_get_contents('data/scores.dat')), true);
    }

    echo(json_encode($data));
    exit();
}
