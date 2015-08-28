var studioServices = angular.module('StudioServices', ['ngResource']);

var base = "http://" + location.host + "/";

studioServices.factory('User', ['$resource',
  function($resource){
    return $resource(base + 'services/studio/users/', {});
  }]);

studioServices.factory('MrrFiles', ['$resource',
    function($resource){
        return $resource(base + 'api/v1/mrrfiles/?format=json', null,
            {'delete': {method: 'DELETE', url: base + 'api/v1/mrrfiles/:mrrId'},
             'select': {method: 'GET', url: base + 'api/v1/mrrfiles/:mrrId/select'},
             'selected': {method: 'GET', url: base + 'api/v1/mrrfiles/selected/'}
            }
        );
}]);

studioServices.factory('Devices', ['$resource',
    function($resource) {
        return $resource(base + 'api/v1/devices/?format=json', null,
            {
                'delete': {method: 'DELETE', url: base + 'api/v1/devices/:deviceId'}
            }
        );
}]);