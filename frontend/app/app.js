'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', ['ngRoute', 'ngStorage', 'myApp.version', 'main'])
    .config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {

        $routeProvider
            .otherwise({redirectTo: '/main'})
            .when('/signIn', {
                templateUrl: 'signIn/signIn.html',
                controller: 'SignInController'
            })
            .when('/signUp', {
                templateUrl: 'signUp/signUp.html',
                controller: 'SignUpController'
            })
            .when('/main', {
                templateUrl: 'templates/main.html',
                controller: 'MainController'
            });

        /*$httpProvider.interceptors.push(['$q', '$location', '$localStorage', function($q, $location, $localStorage) {
            return {
                'request': function (config) {
                    config.headers = config.headers || {};
                    if ($localStorage.user && $localStorage.user.token) {
                        config.headers.Authorization = 'Bearer ' + $localStorage.user.token;
                    }
                    return config;
                },
                'responseError': function(response) {
                    if(response.status === 401 || response.status === 403) {
                        $location.path('/signIn');
                    }
                    return $q.reject(response);
                }
            };
        }]);*/

    }])

    .service('IdentityService', ['$http', '$localStorage', function($http, $localStorage){
        var baseUrl = "http://localhost:8001";

        return {
            signIn: function(data, success, error) {
                $http.post(baseUrl + '/o/token/', $.param(data), {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(success).error(error)
            },
            signUp: function(data, success, error) {
                $http.post(baseUrl + 'users', data).success(success).error(error)
            },
            logout: function() {
                delete $localStorage.user;
            }
        };
    }])

    .controller('IdentityController', ['$scope', '$localStorage', 'IdentityService', function($scope, $localStorage, IdentityService) {
        if ($localStorage.user) {
            if ($localStorage.user.username) {
                $scope.username = $localStorage.user.username;
            }
        }

        $scope.signOut = function() {
            IdentityService.logout();
        }
    }])

    .controller('SignInController', ['$scope', 'IdentityService', '$localStorage','$location', function($scope, IdentityService, $localStorage, $location) {
        $scope.signIn = function () {
            var formData = {
                grant_type: "password",
                username: $scope.username,
                password: $scope.password
            };

            delete $localStorage.user;

            IdentityService.signIn(formData,
                function(res) {
                    var user = {
                        username: $scope.username,
                        token: res.access_token
                    };
                    $localStorage.user = user;
                    $location.path('/main');
                },
                function(res) {
                    console.log(res);
                }
            );
        }
    }])

    .controller('SignUpController', ['$scope', '$location', 'IdentityService', function($scope, $location, IdentityService) {
        $scope.signUp = function () {
            var formData = {
                username: $scope.username,
                password: $scope.password
            };

            IdentityService.signUp(formData,
                function(res) {
                    console.log(res);
                },
                function(res) {
                    console.log(res);
                }
            );
        }
    }]);