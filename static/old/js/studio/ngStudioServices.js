var studioServices = angular.module('StudioServices', ['ngResource']);

var base = "http://" + location.host + "/";

studioServices.factory('User', ['$resource',
  function($resource){
    return $resource(base + 'services/studio/users/', {});
  }]);