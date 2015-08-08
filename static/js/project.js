(function() {
	var app = angular.module('querocomergostoso', []);

	app.service('ActionsServices', function ($http) {
		this.getActions = function () {
			return $http.get('/api/meta/l33t/action')
		}

		this.getTodos = function () {
			return $http.get('/api/meta/todo')
		}
	});

	app.controller('projectMetadataCtrl', function ($scope, ActionsServices) {
		$scope.actionList = {}
		$scope.todoList = [{"desc":"put the team to work!"}, {"desc":"grab a beer"}]
		$scope.team = {}

		ActionsServices.getActions()
			.success(function (data) {
				console.log("Getting changelog...")
				$scope.actionList = data;
			})
			.error(function () {
				console.log("Dummy content!")
				$scope.actionList = [
					{"desc": "new metadata page!!",
					"author": "clenimar"},
				]
			})
	});





})();