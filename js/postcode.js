var app = angular.module('PostcodeApp', []);

app.controller('PostcodeController', function($scope, $http) {
    $scope.title = 'Bangladesh Post Code';
    $http.get('/data/postcode.json').success(function(data) {
        $scope.divisions = data.data;
        $scope.source = data.meta.source;
        $scope.updated_at = data.meta.updated_at;
        $scope.stats = data.meta.counts;

        $scope.codes = [];
        angular.forEach(data.data, function(dists, div) {
            angular.forEach(dists, function(thanas, dist) {
                angular.forEach(thanas, function(soffs, thana) {
                    angular.forEach(soffs, function(code) {
                        $scope.codes.push({
                            'division': div,
                            'district': dist,
                            'thana': thana,
                            'suboffice': code[0],
                            'postcode': code[1]
                        });
                    });
                });
            });
        });
    });
});

app.directive('tabs', function() {
    return {
        restrict: 'E',
        transclude: true,
        scope: { tabType: '@', title: '@', paneHeader: '@' },
        controller: function($scope, $element) {
            var panes = $scope.panes = [];
            if ($scope.tabType.indexOf('nav-stacked') > 0) {
                $scope.tabClass = 'col-sm-4';
                $scope.paneClass = 'col-sm-8';
            } else {
                $scope.tabClass = 'col-md-12';
                $scope.paneClass = 'col-md-12';
            }

            $scope.select = function(pane) {
                angular.forEach(panes, function(pane) {
                    pane.selected = false;
                });
                pane.selected = true;
            }

            this.addPane = function(pane) {
                if (panes.length == 0) $scope.select(pane);
                panes.push(pane);
            }
        },
        templateUrl: '/templates/tabs.html',
        replace: true
    };
});

app.directive('pane', function() {
    return {
        require: '^tabs',
        restrict: 'E',
        transclude: true,
        scope: { title: '@' },
        link: function(scope, element, attrs, tabsCtrl) {
            tabsCtrl.addPane(scope);
        },
        template:
            '<div class="tab-pane" ng-class="{active: selected}" ng-transclude>' +
            '</div>',
        replace: true
    };
});

app.filter('titlecase', function () {
    return function (input) {
        var words = input.split(' ');
        for (var i = 0; i < words.length; i++) {
            words[i] = words[i].toLowerCase();
            words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
        }
        return words.join(' ');
    }
});
