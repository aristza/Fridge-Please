<?php

require_once('core/database.php');

$c = new DBcon();
$con = $c->get_con();


$action = $_REQUEST["action"];
if ( $action == "listProductsInFridge" ) {
    $dbproducts = pg_query($con, "SELECT * FROM product where inFridge=true order by pID ASC;");
    $i = pg_num_rows($dbproducts);
    $jsonProduct = new stdClass();
    echo '{';
    while ($fetchedRow = pg_fetch_row($dbproducts)) {
        echo "\"" . $i . "\":";
        $jsonProduct->id = $fetchedRow[0];
		$jsonProduct->name = $fetchedRow[1];
		$jsonProduct->weight = $fetchedRow[3];
        $jsonProduct->inFridge = $fetchedRow[4];	
        $jsonProduct->expirationDate = $fetchedRow[2];
        echo json_encode($jsonProduct);
        $i--; if ($i>0) { print ","; }
    }
    echo '}';
}
elseif ( $action == "getUserPhoto" ) {
    $res = pg_query($con, "SELECT userPhoto FROM transaction order by timestamp ASC;");
    $raw = pg_fetch_result($res, 'userPhoto');

    header('Content-type: image/jpeg');
    echo pg_unescape_bytea($raw);
}
elseif ( $action == "listTransactions" ) {
    $transactions = pg_query($con, "SELECT tID, timestamp, gotIn, product, name FROM transaction join product on pID=product order by timestamp ASC;");
    $i = pg_num_rows($transactions);
    $jsonTransaction = new stdClass();
    echo '{';
    while ($fetchedRow = pg_fetch_row($transactions)) {
        echo "\"" . $i . "\":";
        $jsonTransaction->id = $fetchedRow[0];
		$jsonTransaction->timestamp = $fetchedRow[1];
        $jsonTransaction->gotin = $fetchedRow[2];
        $jsonTransaction->pid = $fetchedRow[3];
        $jsonTransaction->productName = $fetchedRow[4];
        echo json_encode($jsonTransaction);
        $i--; if ($i>0) { print ","; }
    }
    echo '}';
}
elseif ( $action == "setDesiredTemperature" ) {
    if (isset($_REQUEST["dt"])) {
        pg_query($con, "update fridge set desiredTemperature=".$_REQUEST["dt"]." where fID='0';");
        pg_query($con, 'COMMIT');
        echo 'OK';
    } else {
        echo 'E';
    }
}
elseif ( $action == "setProductName" ) {
    if (isset($_REQUEST["n"])) {
        if (isset($_REQUEST["id"])) {
            pg_query($con, "update product set name='".$_REQUEST["n"]."' where pID="."'".$_REQUEST["id"]."'".";");
            pg_query($con, 'COMMIT');
            echo 'OK';
        } else {
            echo 'E';
        }  
    } else {
        echo 'E';
    }
}
elseif ( $action == "getFridgeState" ) {
    $res = pg_query($con, "SELECT * FROM fridge;");
    $fridge = pg_fetch_row($res);
    $jsonFridge = new stdClass();
    $jsonFridge->id = $fridge[0];
    $jsonFridge->name = $fridge[1];
    $jsonFridge->actualTempereture = $fridge[2];
    $jsonFridge->desiredTempereture = $fridge[3];
    $jsonFridge->humidity = $fridge[4];
    echo json_encode($jsonFridge);
}
else {
    echo 'E';
}

?>
