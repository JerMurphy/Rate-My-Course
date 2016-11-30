function mainCTRL($scope,$http) {
  //log user in
  $scope.logIn = function(user){
    credentials = JSON.stringify({"username": user.username, "password": user.password});
    // Submit the credentials
    $http.post('https://info3103.cs.unb.ca:39348/signin', credentials).then(function(data) {
      // Success here means the transmission was successful - not necessarily the login.
      // The data.status determines login success
      $scope.message = ""
      if(data.status == 201) {
        //you're in!!
        $scope.message = "Login Successful"
      }
      else{
        $scope.message = "Login Unsucessful"
      }
    });
  }

  //list the reviews
  $scope.getReviews = function(id) {
 		var url = "https://info3103.cs.unb.ca:39348/reviews/" + id;

		$http.get(url).success( function(response) {
		  $scope.reviews = response;
      for (review in $scope.reviews){
        var avg = Math.ceil((scaleAvg($scope.reviews[review].courseload_rating) + scaleAvg($scope.reviews[review].tough_rating) + $scope.reviews[review].usefulness_rating)/3)
        console.log(avg)
        if( avg > 3)
          $scope.reviews[review].panel = "panel panel-success"
        if(avg < 3)
          $scope.reviews[review].panel = "panel panel-danger"
        if(avg == 3)
          $scope.reviews[review].panel = "panel panel-warning"
        if($scope.reviews[review].exam_bool == 1)
          $scope.reviews[review].exam = "Yes"
        if($scope.reviews[review].exam_bool == 0)
          $scope.reviews[review].exam = "No"
      }
		});
    
  }

  function scaleAvg(num){
      console.log(num)
      if(num == 1){
        return 5
      }
      if(num==2){
        return 4
      }
      if(num==3){
        return 3
      }
      if(num==4){
        return 2
      }
      if(num==5){
        return 1
      }
  }

  //get the CS courses
  $scope.getCS = function() {
  	var url = "https://info3103.cs.unb.ca:39348/courses/CS";

 		$http.get(url).success( function(response) {
    	$scope.courses = response;
 		});
	}
	//get the INFO courses
	$scope.getINFO = function() {
  	var url = "https://info3103.cs.unb.ca:39348/courses/INFO";

 		$http.get(url).success( function(response) {
    	$scope.courses = response;
 		});
	}
	//get the MATH courses
	$scope.getMATH = function() {
  	var url = "https://info3103.cs.unb.ca:39348/courses/MATH";

 		$http.get(url).success( function(response) {
    	$scope.courses = response;
 		});
	}
	//get the STAT courses
	$scope.getSTAT = function() {
  	var url = "https://info3103.cs.unb.ca:39348/courses/STAT";

 		$http.get(url).success( function(response) {
    	$scope.courses = response;
 		});
	}
	//get the MAAC courses
	$scope.getMAAC = function() {
  	var url = "https://info3103.cs.unb.ca:39348/courses/MAAC";

 		$http.get(url).success( function(response) {
    	$scope.courses = response;
 		});
	}
}