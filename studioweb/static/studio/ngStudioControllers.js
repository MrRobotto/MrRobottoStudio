'use strict';

var studioControllers = angular.module('StudioControllers', []);

studioControllers.controller('BlendFilesController', ['$scope', 'MrrFiles', function ($scope, MrrFiles) {

    $scope.mrrs = MrrFiles.query();

    $scope.selected_mrr = MrrFiles.selected();

    $scope.onSelect = function (mrr) {
        MrrFiles.select({mrrId: mrr.id}, function () {
            $scope.mrrs = MrrFiles.query();
            $scope.selected_mrr = MrrFiles.selected();
        });
    };

    $scope.onDelete = function (mrr) {
        MrrFiles.delete({mrrId: mrr.id}, function () {
            $scope.mrrs = MrrFiles.query();
            $scope.selected_mrr = MrrFiles.selected();
        });
    }
}]);

studioControllers.controller('DevicesController', ['$scope', '$interval', 'Devices', function ($scope, $interval, Devices) {
    $scope.devices = Devices.query();
    /*$interval(function() {
     var devs = Devices.query(function() {
     if (devs.length != $scope.devices.length) {
     $scope.devices = devs;
     }
     });
     }, 1000);*/

    var base_url = Devices.manualregister(function () {
        $scope.base_url = base_url["base_url"];
    });

    $scope.onDelete = function (device) {
        Devices.delete({deviceId: device.id}, function () {
            $scope.devices = Devices.query();
        });
    }
}]);

studioControllers.controller('LoginCtrl', ['$scope', '$location', 'User', function ($scope, $location, User) {

    $scope.regUsername = "";
    $scope.regPass1 = "";
    $scope.regPass2 = "";
    $scope.passMatch = false;

    $scope.register = function () {
        if (!$scope.passMatch) {
            return;
        }
        var userName = $scope.regUsername;
        var pass = $scope.regPass1;
        var user = new User({'username': userName, 'password': pass});
        user.$save(function (value, headers) {
            alert(value);
        }, function (resp) {
            alert(resp.status);
        });
    };

    $scope.checkRegister = function () {
        if ($scope.regUsername == "") {
            $scope.passMatch = false;
            return false;
        }
        if ($scope.regPass1 == $scope.regPass2) {
            $scope.matchColor = {'background-color': 'white'};
            $scope.passMatch = true;
        } else {
            $scope.matchColor = {'background-color': '#d9534f'};
            $scope.passMatch = false;
        }
        return $scope.passMatch;
    };
}]);