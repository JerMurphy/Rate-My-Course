function mainCTRL($scope,$http) {
  var session = {};
  $scope.session = session
  session['exists'] = false //call ng-if="getLogin()" instead?? (more secure)
  session['username'] = null

  //login user
  $scope.login = function(user) {
    var url = 'https://info3103.cs.unb.ca:39348/signin'
    credentials = JSON.stringify({"username": user.username, "password": user.password});

    $http({ method: 'POST', url: url, data: credentials }).then(
      function(response) { //success
        if (response.status == 201) {
          $scope.message = null
          session['exists'] = true
          session['username'] = response.data.username
        }
      }, 
      function(response) { //error
        $scope.message = "Login Failed"
      }
    );
  }

  //logout user
  $scope.logout = function() {
    var url = 'https://info3103.cs.unb.ca:39348/signin'

    $http({ method: 'DELETE', url: url }).then(
      function(response) { //success
        if (response.status == 200) {
          session['working'] = true
        }
      }, 
      function(response) { //error
        session['exists'] = false //TEMPORARILY HERE - to be moved to success response
        session['username'] = null //TEMPORARILY HERE - to be moved to success response
      }
    );
  }

  //check for session
  $scope.getLogin = function() {
    var url = 'https://info3103.cs.unb.ca:39348/signin';

    $http.get(url).success( function(response) { //success
      session['exists'] = true
      session['username'] = response.data.username
    },
    function(response) { //error
      session['exists'] = false
      session['username'] = null
    });
  }

  $scope.search = function(e, input) {
    var url = 'https://info3103.cs.unb.ca:39348/courses'; //get all reviews
    var charCode = (e.which) ? e.which : e.keyCode //not used
    var results = [] //array of courses
    input = input.toUpperCase()

    $http.get(url).success( function(response) { //success
      var course;
      for (course in response) {
        if (input == "")
          continue
        else if (input == (response[course].id).substring(0,input.length))
          results.push(response[course].id)
        else if (input == (response[course].num).substring(0,input.length))
          results.push(response[course].id)
      }
      $scope.search_results = results;
    })
  }

 // post a review
   $scope.postReview = function() {
     var url = 'https://info3103.cs.unb.ca:39348/reviews';
     var dat = {
        postedBy: "jmurphy1",
        review: $('#review').val(),
        tough_rating:$('#tough').val(),
        courseload_rating: $('#courseload').val(),
        usefulness_rating: $('#use').val(),
        courseId: $('#courseid').val(),
        exam_bool: $('#exam').val()
     }
     var data = JSON.stringify(dat);
     console.log(data); 

     $http({ method: 'POST', url: url, data: data }).then(
       function(response) { //success
         if (response.status == 201) {
           //successfully posted
           

         }
       },
       function(response) { //error
         if (response.status == 401) {
           //access denied

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