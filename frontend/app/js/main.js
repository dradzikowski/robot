angular.module('main', ['chart.js', 'ngTagsInput', 'ngResource', 'ui.bootstrap'])

    .config(function () {
    })
    .controller('MainController', ['$scope', '$filter', 'MainService', '$routeParams', '$rootScope', 'Utils',
        function ($scope, $filter, mainService, $routeParams, $rootScope, utils) {

            $scope.getstatistics = function () {
                //key = $scope.key;
                //value = $scope.value;
                $scope.loading = true;
                //data = {"key": "keywords", "value": $scope.value[0].value};
                mainService.getstatistics($scope.value, function (res) {
                    //$scope.result = res.data;
                    $scope.loading = false;

                    $scope.itemsList = res.data.articles;

                    $scope.itemsPerPage = 5;
                    $scope.currentPage = 1;

                    $scope.pageCount = function () {
                        return Math.ceil($scope.itemsList.length / $scope.itemsPerPage);
                    };

                    $scope.totalItems = $scope.itemsList.length;
                    $scope.$watch('currentPage + itemsPerPage', function () {
                        var begin = (($scope.currentPage - 1) * $scope.itemsPerPage),
                            end = begin + $scope.itemsPerPage;

                        $scope.filteredItems = $scope.itemsList.slice(begin, end);
                        console.log($scope.filteredItems);
                    });

                    console.log("Response for findByKeywords/");
                    console.log(res);

                    //TODO clear charts after each search
                    var dataForChart = utils.prepareDataForChart(res.data);

                    $scope.labels = dataForChart['labels'];
                    $scope.series = dataForChart['series'];
                    $scope.data = dataForChart['data'];
                    $scope.options = {
                        scaleBeginAtZero: true
                    };
                    $scope.onClick = function (points, evt) {
                        console.log(points, evt);
                    };

                }, function (res) {
                    $scope.loading = false;
                    console.log(res);
                })
            };

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
            }
        };
    }]).factory('Utils', ['$filter', function ($filter) {
    return {
        prepareDataForChart: function (result) {
            var siteSeries = ['TechCrunch'];
            var dateLabels = [];
            var occurencesData = [];
            var chartData = {};

            var dates = this.spanDates();

            dates.forEach(function (date) {
                chartData[date] = 0;
            });

            //TODO date_crawled is not exactly the date I want
            result['articles'].forEach(function (entry) {
                chartData[entry.date_crawled] += 1;
            });

            dates.forEach(function (val) {
                dateLabels.push(val);
                occurencesData.push(chartData[val]);
            });

            var occurencesDataArray = [];
            occurencesDataArray.push(occurencesData);

            dataForChart = {};
            dataForChart['labels'] = dateLabels;
            dataForChart['data'] = occurencesDataArray;
            dataForChart['series'] = siteSeries;

            console.log("Data prepared for chart:");
            console.log(dataForChart);
            return dataForChart;
        },
        spanDates: function () {
            var dateToday = new Date();
            var datePointer = new Date();
            datePointer.setMonth(datePointer.getMonth() - 1);

            dates = [];

            while (datePointer < dateToday) {
                datePointer.setDate(datePointer.getDate() + 1);
                dates.push($filter('date')(datePointer, 'yyyy-MM-dd'));
            }

            return dates;
        }
    }
}]);
