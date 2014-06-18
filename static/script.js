
function CollapseDemoCtrl($scope) {
  $scope.isCollapsedGet = true;
  $scope.isCollapsedPost = true;
  $scope.isCollapsedPut = true;
  $scope.isCollapsedDelete = true;
}

function CollapseDemoCtrl1($scope) {
  $scope.isCollapsedPortGet = true;
  $scope.isCollapsedPortGetName = true;
  $scope.isCollapsedPortPost = true;
  $scope.isCollapsedPortDelete = true;
}

// define angular module/app
var stocksFormApp = angular.module('stocksFormApp', []);

// create angular controller and pass in $scope and $http
function stocksFormController($scope, $http) {
	// create a blank object to hold our form information
	// $scope will allow this to pass between controller and view
	$scope.formData = {};
	
	//TODO: Keep bringing in stuff based on referenceFormController function
}

var portfolioFormApp = angular.module('portfolioFormApp', []);

function portfolioFormApp($scope, $http) {
	//TODO: Keep bringing in stuff based on referenceFormController function
	$scope.formData = {};
	
}

// define angular module/app
var referenceFormApp = angular.module('referenceFormApp', []);

// create angular controller and pass in $scope and $http
function referenceFormController($scope, $http) {

	// create a blank object to hold our form information
	// $scope will allow this to pass between controller and view
	$scope.formData = {};

	// process the form
	
	$scope.processForm = function() {
	//console.log($scope.formData.name);
		$http({
			method  : 'GET',
			url     : '/stock/price/'+$scope.formData.name,
			//data    : $.param($scope.formData),  // pass in data as strings
			//headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
		})
			.success(function(data) {
				console.log(data);
				
				$scope.pricemessage = data;

			//    if (!data.success) {
					// if not successful, bind errors to error variables
			//        $scope.errorName = data.errors.name;
			//        $scope.errorSuperhero = data.errors.superheroAlias;
			//    } else {
					// if successful, bind success message to message
			//        $scope.message = data.message;
			//    }
			});

	};

}

// create the module and name it scotchApp
var scotchApp = angular.module('scotchApp', ['ngRoute','ui.bootstrap']);

// configure our routes
scotchApp.config(function($routeProvider) {
$routeProvider

	// route for the home page
	.when('/', {
		templateUrl : 'home.html',
		controller  : 'mainController'
	})

	// route for the about page
	.when('/about', {
		templateUrl : 'about.html',
		controller  : 'aboutController'
	})

	// route for the contact page
	.when('/contact', {
		templateUrl : 'contact.html',
		controller  : 'contactController'
	});
});

// create the controller and inject Angular's $scope
scotchApp.controller('mainController', function($scope) {
// create a message to display in our view
$scope.message = 'Scroll down for AJAX forms';
});

scotchApp.controller('aboutController', function($scope) {
$scope.message = 'Look! I am an about page.';
});

scotchApp.controller('contactController', function($scope) {
$scope.message = 'Contact us! JK. This is just a lab.';
});