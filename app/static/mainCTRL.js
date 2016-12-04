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
          session['exists'] = false
          session['username'] = null
        }
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
      function(response) {
        session['exists'] = false
        session['username'] = null
      });
  }

  $scope.search = function(e, input) {
    var url = 'https://info3103.cs.unb.ca:39348/courses'; //get all reviews
    var charCode = (e.which) ? e.which : e.keyCode //not used
    var results = [] //array of coursesparseInt(reviews[review].avg)
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
        postedBy: session['username'],
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
         if (response.status == 201) {}
       },
       function(response) { //error
         if (response.status == 401) {}
       });
   }

  //list the reviews
  $scope.getReviews = function(id) {
    var url = "https://info3103.cs.unb.ca:39348/reviews/" + id;

    $http.get(url).success( function(response) {
      reviews = response
      $scope.reviews = reviews
      //console.log(reviews)
      for (review in reviews) {
        reviews[review].avg = ((scaleAvg(reviews[review].courseload_rating) + scaleAvg(reviews[review].tough_rating) + reviews[review].usefulness_rating)/3).toFixed(1)
        reviews[review].avg_alert = getAverageColor(reviews[review].avg)
        reviews[review].courseload_alert = getAverageColor(scaleAvg(reviews[review].courseload_rating))
        reviews[review].usefulness_alert = getAverageColor(reviews[review].tough_rating)
        reviews[review].tough_alert = getAverageColor(scaleAvg(reviews[review].tough_rating))

        if(reviews[review].exam_bool == 1)
          reviews[review].exam = "Examination"
        if(reviews[review].exam_bool == 0)
          reviews[review].exam = "No Examination"
      }
      $scope.courseAverages = getCourseAverages(reviews)
    });
  }

  function scaleAvg(num){
      if(num==1)
        return 5
      if(num==2)
        return 4
      if(num==3)
        return 3
      if(num==4)
        return 2
      if(num==5)
        return 1
  }

  function getAverageColor(avg) {
    if (avg>=4)
      return "alert alert-success"
    else if (avg>2 && avg<4)
      return "alert alert-warning"
    else if (avg<=2)
      return "alert alert-danger"
  }

  function getCourseAverages(reviews) {
    courseAverages = {courseId: null, avg: 0, courseload_rating: 0, tough_rating: 0, usefulness_rating: 0} //average of all reviews for course
    for (review in reviews) {
      courseAverages['avg'] += parseFloat(reviews[review].avg)
      courseAverages['courseload_rating'] += reviews[review].courseload_rating
      courseAverages['tough_rating'] += reviews[review].tough_rating
      courseAverages['usefulness_rating'] += reviews[review].usefulness_rating
    }
    courseAverages['courseId'] = reviews[0].courseId
    courseAverages['avg'] = (courseAverages['avg']/reviews.length).toFixed(1) //calculate total avg
    courseAverages['avg_alert'] = getAverageColor(courseAverages['avg'])

    courseAverages['courseload_rating'] = (courseAverages['courseload_rating']/reviews.length).toFixed(1) //calculate courseload_rating
    courseAverages['courseload_alert'] = getAverageColor(courseAverages['courseload_rating'])

    courseAverages['tough_rating'] = (courseAverages['tough_rating']/reviews.length).toFixed(1) //calculate tough_rating
    courseAverages['tough_alert'] = getAverageColor(courseAverages['tough_rating'])

    courseAverages['usefulness_rating'] = (courseAverages['usefulness_rating']/reviews.length).toFixed(1) //calculate usefulness_rating
    courseAverages['usefulness_alert'] = getAverageColor(courseAverages['usefulness_rating'])

    console.log(courseAverages)
    return (courseAverages)
  }

  //delete a specific review
  $scope.deleteReview = function(id) {
    var url = "https://info3103.cs.unb.ca:39348/reviews/" + id

    $http({ method: 'DELETE', url: url }).then(
      function(response) { //success
        if (response.status == 200){}
      },
      function(response) { //error
        if (response.status == 401){}
    });
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
