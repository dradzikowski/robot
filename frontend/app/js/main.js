angular.module('main', ['ngTagsInput', 'chart.js'])

    .config(function () {
    })
    .controller('MainController', ['$scope', '$filter', 'MainService', '$routeParams',
        function ($scope, $filter, mainService, $routeParams) {

            $scope.getstatistics = function () {
                //key = $scope.key;
                //value = $scope.value;
                $scope.loading = true;
                data = {"key": "keywords", "value": $scope.value[0].value};
                mainService.getstatistics(data, function (res) {
                    $scope.result = res.data;
                    $scope.loading = false;
                    console.log(res);
                }, function (res) {
                    console.log(res);
                })
            };

            /*
            $scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
            $scope.series = ['Series A', 'Series B'];
            $scope.data = [
                [65, 59, 80, 81, 56, 55, 40],
                [28, 48, 40, 19, 86, 27, 90]
            ];*/

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