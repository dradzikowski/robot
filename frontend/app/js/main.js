angular.module('main', ['chart.js', 'ngTagsInput'])

    .config(function () {
    })
    .controller('MainController', ['$scope', '$filter', 'MainService', '$routeParams',
        function ($scope, $filter, mainService, $routeParams) {

            $scope.getstatistics = function () {
                //key = $scope.key;
                //value = $scope.value;
                $scope.loading = true;
                //data = {"key": "keywords", "value": $scope.value[0].value};
                mainService.getstatistics($scope.value, function (res) {
                    $scope.result = res.data;
                    $scope.loading = false;
                    console.log(res);
                }, function (res) {
                    console.log(res);
                })
            };

              $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
              $scope.series = ['Series A', 'Series B'];
              $scope.data = [
                [65, 59, 80, 81, 56, 55, 40],
                [28, 48, 40, 19, 86, 27, 90]
              ];
              $scope.onClick = function (points, evt) {
                console.log(points, evt);
              };

        }])
    .service('MainService', ['$http', function ($http) {
        var baseUrl = "http://localhost:8001";

        return {
            getstatistics: function (data, success, error) {
                //$http.post(baseUrl + '/find').then(success, error);

                var keywords = [];
                angular.forEach(data, function(obj) {
                  this.push(obj.text);
                }, keywords);

                var keywordsObj = {"keywords":keywords};

                $http({
                    method: 'POST',
                    url: baseUrl + '/findByKeywords/',
                    data: keywordsObj,
                    headers: {'Content-Type': 'application/json'}
                }).then(success, error);
            }
        };
    }]);