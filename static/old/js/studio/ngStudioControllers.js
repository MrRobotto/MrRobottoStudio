'use strict';

var studioControllers = angular.module('StudioControllers', []);

studioControllers.controller('LoginCtrl', ['$scope', '$location', 'User', function ($scope, $location, User) {

    $scope.regUsername = "";
    $scope.regPass1 = "";
    $scope.regPass2 = "";
    $scope.passMatch = false;

    $scope.register = function() {
        if (!$scope.passMatch) {
            return;
        }
        var userName = $scope.regUsername;
        var pass = $scope.regPass1;
        var user = new User({'username': userName, 'password': pass});
        user.$save(function(value, headers) {
            alert(value);
        }, function(resp) {
            alert(resp.status);
        });
    };

    $scope.checkRegister = function() {
        if ($scope.regUsername == "") {
            $scope.passMatch = false;
            return false;
        }
        if ($scope.regPass1 == $scope.regPass2) {
            $scope.matchColor = {'background-color':'white'};
            $scope.passMatch = true;
        } else {
            $scope.matchColor = {'background-color':'#d9534f'};
            $scope.passMatch = false;
        }
        return $scope.passMatch;
    };
}]);