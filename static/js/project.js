(function() {
	var app = angular.module('querocomergostoso', []);

	app.service('ActionsServices', function ($http) {
		this.getActions = function () {
			return $http.get('/api/meta/action')
		}

		this.getTodos = function () {
			return $http.get('/api/meta/todo')
		}
	});

	app.controller('projectMetadataCtrl', function ($scope, ActionsServices) {
		$scope.actionList = {}
		$scope.todoList = {}
		$scope.team = {}

		ActionsServices.getActions()
			.success(function (data) {
				console.log("Getting changelog...")
				$scope.actionList = data;
			})
			.error(function () {
				console.log("Something went wrong while trying to get changelog.")
			});

		ActionsServices.getTodos()
			.success(function (data) {
				console.log("Getting to-dos...")
				$scope.todoList = data;
			})
			.error(function () {
				console.log("Something went wrong while trying to get to-dos.")
			})


	});





})();