<?php
    require_once './Router.php';

    if(isset($_GET['action'])){
        $action=$_GET['action'];
    }
    else{
        $action="_no_action";
    }

    $router=new Router();
    $router->register('getValues', 'Value', 'getValues');

    $response=$router->run($action);

    echo json_encode($response);
