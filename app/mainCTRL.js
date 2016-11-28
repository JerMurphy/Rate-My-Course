function mainCTRL($scope,$http) {
   
    //list the reviews
    $scope.getReviews = function(id) {
    	
     		var url = "https://info3103.cs.unb.ca:43327/reviews/" + id;

   			$http.get(url).success( function(response) {
      		$scope.reviews = response;
   			});

	}

    //get the CS courses
    $scope.getCS = function() {
    	var url = "https://info3103.cs.unb.ca:43327/courses/CS";

   		$http.get(url).success( function(response) {
      		$scope.courses = response;
   		});
	}
	//get the INFO courses
	$scope.getINFO = function() {
    	var url = "https://info3103.cs.unb.ca:43327/courses/INFO";

   		$http.get(url).success( function(response) {
      		$scope.courses = response;
   		});
	}
	//get the MATH courses
	$scope.getMATH = function() {
    	var url = "https://info3103.cs.unb.ca:43327/courses/MATH";

   		$http.get(url).success( function(response) {
      		$scope.courses = response;
   		});
	}
	//get the STAT courses
	$scope.getSTAT = function() {
    	var url = "https://info3103.cs.unb.ca:43327/courses/STAT";

   		$http.get(url).success( function(response) {
      		$scope.courses = response;
   		});
	}
	//get the MAAC courses
	$scope.getMAAC = function() {
    	var url = "https://info3103.cs.unb.ca:43327/courses/MAAC";

   		$http.get(url).success( function(response) {
      		$scope.courses = response;
   		});
	}
}