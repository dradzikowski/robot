var myApp = angular.module('myApp', ['myApp2']);
var myApp2 = angular.module('myApp2', []);

// assigned
// if nothing is in namespace and ngApp is not specified error occurs
// invoke function and call digest from rootScope
// implicit DI
myApp2.controller('someCtrl', function ($scope, $rootScope, helloWorld, helloWorldFromFactory, helloWorldFromService,
                                        myService, myFactory, myProv) {
    $scope.hellos = [
        helloWorld.sayHello(),
        helloWorldFromFactory.sayHello(),
        helloWorldFromService.sayHello()];


    $scope.serviceOutput = "myService = " + myService;
    $scope.factoryOutput = "myFactory = " + myFactory;
    $scope.providerOutput = "myProvider = " + myProv;


    setTimeout(function () {
        $scope.$apply(function () {
            $scope.message = "My message!";
        })
    }, 2000);

    console.log($scope);
    console.log($rootScope);
});

//service style, probably the simplest one
myApp2.service('helloWorldFromService', function () {
    this.sayHello = function () {
        return "Hello, World!"
    };
});

//factory style, more involved but more sophisticated
myApp2.factory('helloWorldFromFactory', function () {
    return {
        sayHello: function () {
            return "Hello, World!"
        }
    };
});

//provider style, full blown, configurable version
myApp2.provider('helloWorld', function () {

    this.name = 'Default';

    this.$get = function () {
        var name = this.name;
        return {
            sayHello: function () {
                return "Hello, " + name + "!"
            }
        }
    };

    this.setName = function (name) {
        this.name = name;
    };
});

//hey, we can configure a provider!
myApp2.config(function (helloWorldProvider) {
    helloWorldProvider.setName('World');
});


// not assigned
// in global namespace
function someCtrl($scope) {
    $scope.message = "My message!";
}

/*
 ################## another way ######################
 */

var MyFunc = function () {

    this.name = "default name";

    this.$get = function () {
        this.name = "new name"
        return "Hello from MyFunc.$get(). this.name = " + this.name;
    };

    return "Hello from MyFunc(). this.name = " + this.name;
};

// returns the actual function
myApp2.service('myService', MyFunc);

// returns the function's return value
myApp2.factory('myFactory', MyFunc);

// returns the output of the function's $get function
myApp2.provider('myProv', MyFunc);