var studioServices = angular.module('StudioServices', ['ngResource']);

var base = "http://" + location.host + "/";

studioServices.factory('User', ['$resource',
    function ($resource) {
        return $resource(base + 'services/studio/users/', {});
    }]);

studioServices.factory('MrrFiles', ['$resource',
    function ($resource) {
        return $resource(base + 'api/mrrfiles/?format=json', null,
            {
                'delete': {method: 'DELETE', url: base + 'api/mrrfiles/:mrrId'},
                'select': {method: 'POST', url: base + 'api/mrrfiles/:mrrId/select'},
                'selected': {method: 'GET', url: base + 'api/mrrfiles/selected/'}
            }
        );
    }]);

studioServices.factory('Devices', ['$resource',
    function ($resource) {
        return $resource(base + 'api/devices/?format=json', null,
            {
                'delete': {method: 'DELETE', url: base + 'api/devices/:deviceId'},
                'manualregister': {method: 'GET', url: base + 'api/devices/manualregister'}
            }
        );
    }]);