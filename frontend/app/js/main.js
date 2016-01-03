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

                    dataForChart = mainService.prepareDataForChart($scope.result);

                    console.log(dataForChart);
                    $scope.labels = dataForChart['labels'];
                    $scope.series = dataForChart['series'];
                    $scope.data = dataForChart['data'];
                    $scope.onClick = function (points, evt) {
                        console.log(points, evt);
                    };

                }, function (res) {
                    console.log(res);
                })
            };

            /*
            $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
            $scope.series = ['Series A', 'Series B'];
            $scope.data = [
                [65, 59, 80, 81, 56, 55, 40],
                [28, 48, 40, 19, 86, 27, 90]
            ];
            $scope.onClick = function (points, evt) {
                console.log(points, evt);
            };*/


        }])
    .service('MainService', ['$http', function ($http) {
        var baseUrl = "http://localhost:8001";

        return {
            getstatistics: function (data, success, error) {
                //$http.post(baseUrl + '/find').then(success, error);

                var keywords = [];
                angular.forEach(data, function (obj) {
                    this.push(obj.text);
                }, keywords);

                var keywordsObj = {"keywords": keywords};

                $http({
                    method: 'POST',
                    url: baseUrl + '/findByKeywords/',
                    data: keywordsObj,
                    headers: {'Content-Type': 'application/json'}
                }).then(success, error);
            },
            prepareDataForChart: function (result) {
                //TODO complete refactor
                var siteSeries = ['TechCrunch'];
                var dateLabels = [];
                var occurencesData = [];
                var chartData = {};

                result['articles'].forEach(function (entry) {
                    if (chartData[entry.art_date] > 0) {
                        chartData[entry.art_date] += 1;
                    }
                    else chartData[entry.art_date] = 1;
                });

                var properties = [];
                for (var property in chartData) {
                    if (chartData.hasOwnProperty(property)) {
                        properties.push(property);
                    }
                }
                properties.sort();
                properties.forEach(function (val) {
                    dateLabels.push(val);
                    occurencesData.push(chartData[val]);
                });

                var occurencesDataArray = [];
                occurencesDataArray.push(occurencesData);

                dataForChart = {};
                dataForChart['labels'] = dateLabels;
                dataForChart['data'] = occurencesDataArray;
                dataForChart['series'] = siteSeries;

                console.log(dataForChart);
                return dataForChart;
            }
        };
    }]);