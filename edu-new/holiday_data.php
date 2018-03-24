<?php
header("Content-type: text/html; charset=utf-8");
//Init
if(isset($_GET['role']) && isset($_GET['hash']) && isset($_GET['sid']) && isset($_GET['password']) && $_GET['sid'] != '' && $_GET['password'] != ''){
    $role     = $_GET['role'];
    $hash     = $_GET['hash'];
    $sid      = $_GET['sid'];
    $password = $_GET['password'];
}
else{
    exit('{"code":65535,"msg":"缺失参数"}');
}
//Verify Hash
include '../lib/VerifyHash.class.php';
$verify = new VerifyHash($role,$hash);
if(!$verify->checkRole()){
    exit('{"code":-1,"msg":"接口调用身份验证失败"}');
}

//Get Data and decode from unicode to utf-8
$data = shell_exec("python ./lib/holiday_date.py $sid $password");
class Helper_Tool   //unicode to utf-8
{
  static function unicodeDecode($data)
  {  
    function replace_unicode_escape_sequence($match) {
      return mb_convert_encoding(pack('H*', $match[1]), 'UTF-8', 'UCS-2BE');
    }  
    $rs = preg_replace_callback('/\\\\u([0-9a-f]{4})/i', 'replace_unicode_escape_sequence', $data);
    return $rs;
  }  
}
$data = Helper_Tool::unicodeDecode($data);
echo "$data";
?>