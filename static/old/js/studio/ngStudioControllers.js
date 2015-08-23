'use strict';

var studioControllers = angular.module('StudioControllers', []);

studioControllers.controller('BlendFilesController', ['$scope', 'MrrFiles', function($scope, MrrFiles){

    $scope.mrrs = MrrFiles.query();

    $scope.selected_mrr = MrrFiles.selected();

    $scope.onSelect = function(mrr) {
        MrrFiles.select({mrrId: mrr.id}, function() {
            $scope.mrrs = MrrFiles.query();
            $scope.selected_mrr = MrrFiles.selected();
        });
    };

    $scope.onDelete = function(mrr) {
        MrrFiles.delete({mrrId: mrr.id}, function() {
            $scope.mrrs = MrrFiles.query();
            $scope.selected_mrr = MrrFiles.selected();
        });
    }
}]);

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