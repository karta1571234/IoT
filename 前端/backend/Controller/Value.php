<?php
  require_once __DIR__ . './mysql.php';
  require_once __DIR__ . './Controller.php';

  class Value extends Controller {
    public function getValues(){
      $response = openDB();
      if ($response['status']==200){
        $conn=$response['result'];
        $sql="SELECT  *  FROM  `rpi_sensor`";
        $stmt=$conn->prepare($sql);
        $result=$stmt->execute();

        if ($result) {
          $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
          return $this->response(200, "查詢成功", $rows);
        } 
        else {
          return $this->response(400, "SQL錯誤"); //Bad Request
        }
      }
    }
  }

?>