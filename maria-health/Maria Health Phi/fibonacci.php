<?php
    function fibonacci($num) {
        $x = 0;
        $y = 1;

        for ($i = 1; $i <= $num; $i++) {
            $z = $x + $y;
            $x = $y;
            $y = $z;

            if ($z % 3 == 0 and $z % 5 == 0) {
                $z = "Maria Health";
            } elseif ($z % 3 == 0) {
                $z = "Maria";
            } elseif ($z % 5 == 0) {
                $z = "Health";
            }

            echo $z . "<br/>";
        }
    }

    fibonacci(10);
?>