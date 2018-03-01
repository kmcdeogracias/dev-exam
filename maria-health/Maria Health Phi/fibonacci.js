function fibonacci(num) {
	var x = 0, y = 1;

	for (var i=0; i <= num; i++) {
		var z = x + y;
        x = y;
        y = z;

        if (z % 3 == 0 && z % 5 == 0) {
            z = "Maria Health";
        } else if (z % 3 == 0) {
            z = "Maria";
        } else if (z % 5 == 0) {
            z = "Health";
        }

        console.log(z)
	}


}

fibonacci(100)