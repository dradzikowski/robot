angular.module('main', [])

    .config(function () {
    })
    .controller('MainController', ['$scope', '$filter', 'MainService', '$routeParams',
        function ($scope, $filter, mainService, $routeParams) {
            $scope.getstatistics = function () {
                //key = $scope.key;
                //value = $scope.value;
                data = {"key": "keywords", "value": $scope.value};
                mainService.getstatistics(data, function (res) {
                    $scope.result = res.data;
                    console.log(res );
                }, function (res) {
                    console.log(res);
                })
            }
        }])
    .service('MainService', ['$http', function ($http) {
        var baseUrl = "http://localhost:8001";

        return {
            getstatistics: function (data, success, error) {
                //$http.post(baseUrl + '/find').then(success, error);
                $http({
                    method: 'POST',
                    url: baseUrl + '/find/',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(success, error);
            }
        };
    }]);