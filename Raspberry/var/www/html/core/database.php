<?php
	class DBcon {
		private	$dbserver = 'localhost';
		private $dbusername = "postgres";
		private	$dbpassword = "97237445";
		private	$dbname = "SmartFridge";
		public	$con = null;

		public function __construct() {
	        $this->con = pg_connect('host='. $this->dbserver .' port=5432 dbname='. $this->dbname .' user='. $this->dbusername .' password='. $this->dbpassword);
		}

		public function __destruct() {
			pg_close($this->con);
  		}

		public function get_con() {
			return $this->con;
		}

	}
?>
