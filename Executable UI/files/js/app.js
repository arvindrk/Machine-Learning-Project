'use strict';

angular.module('angularSmoothscroll', []).directive('smoothScroll', [
  '$log', '$timeout', '$window', function($log, $timeout, $window) {
    /*
        Retrieve the current vertical position
        @returns Current vertical position
        */

        var currentYPosition, elmYPosition, smoothScroll;
        currentYPosition = function() {
          if ($window.pageYOffset) {
            return $window.pageYOffset;
          }
          if ($window.document.documentElement && $window.document.documentElement.scrollTop) {
            return $window.document.documentElement.scrollTop;
          }
          if ($window.document.body.scrollTop) {
            return $window.document.body.scrollTop;
          }
          return 0;
        };
        /*
        Get the vertical position of a DOM element
        @param eID The DOM element id
        @returns The vertical position of element with id eID
        */

        elmYPosition = function(eID) {
          var elm, node, y;
          elm = document.getElementById(eID);
          if (elm) {
            y = elm.offsetTop;
            node = elm;
            while (node.offsetParent && node.offsetParent !== document.body) {
              node = node.offsetParent;
              y += node.offsetTop;
            }
            return y;
          }
          return 0;
        };
        /*
        Smooth scroll to element with a specific ID without offset
        @param eID The element id to scroll to
        @param offSet Scrolling offset
        */

        smoothScroll = function(eID, offSet) {
          var distance, i, leapY, speed, startY, step, stopY, timer, _results;
          startY = currentYPosition();
          stopY = elmYPosition(eID) - offSet;
          distance = (stopY > startY ? stopY - startY : startY - stopY);
          if (distance < 100) {
            scrollTo(0, stopY);
            return;
          }
          speed = Math.round(distance / 100);
        if (true) { //speed>=20
          speed = 20;
        }
        step = Math.round(distance / 25);
        leapY = (stopY > startY ? startY + step : startY - step);
        timer = 0;
        if (stopY > startY) {
          i = startY;
          while (i < stopY) {
            setTimeout('window.scrollTo(0, ' + leapY + ')', timer * speed);
            leapY += step;
            if (leapY > stopY) {
              leapY = stopY;
            }
            timer++;
            i += step;
          }
          return;
        }
        i = startY;
        _results = [];
        while (i > stopY) {
          setTimeout('window.scrollTo(0, ' + leapY + ')', timer * speed);
          leapY -= step;
          if (leapY < stopY) {
            leapY = stopY;
          }
          timer++;
          _results.push(i -= step);
        }
        return _results;
      };
      return {
        restrict: 'A',
        link: function(scope, element, attr) {
          return element.bind('click', function() {
            var offset;
            if (attr.target) {
              offset = attr.offset || 100;
            // $log.log('Smooth scroll: scrolling to', attr.target, 'with offset', offset);
            return smoothScroll(attr.target, offset);
          } else {
            // return $log.warn('Smooth scroll: no target specified');
          }
        });
        }
      };
    }
    ]).directive('smoothScrollJquery', [
    '$log', function($log) {
      return {
        restrict: 'A',
        link: function(scope, element, attr) {
          return element.bind('click', function() {
            var offset, speed, target;
            if (attr.target) {
              offset = attr.offset || 100;
              target = $('#' + attr.target);
              speed = attr.speed || 500;
            // $log.log('Smooth scroll jQuery: scrolling to', attr.target, 'with offset', offset, 'and speed', speed);
            return $('html,body').stop().animate({
              scrollTop: target.offset().top - offset
            }, speed);
          } else {
            // $log.log('Smooth scroll jQuery: no target specified, scrolling to top');
            return $('html,body').stop().animate({
              scrollTop: 0
            }, speed);
          }
        });
        }
      };
    }
    ]);

    
var app = angular.module('app',['angularSmoothscroll']);
///////////////////////////////////////////////////////////HOME CONTROLLER///////////////////////////////////////////////////////////////////

app.controller('homeController', ['$scope','$http',
  function($scope,$http) {
    $scope.type1 = {};
    $scope.cirlce = {};
    $scope.show_img = true;
    $scope.type1.sizeTypes = "mb";
    $scope.progress_data = "Enter the Data for your ";
    $scope.data_blue = "Game.";
    $scope.breakout = true;
    
    $scope.submit_form = function(payload) {
      console.log(payload);
      $scope.progress_class = "progress animated fadeIn";
      $.ajax({
        url:'http://localhost:8000/',
        type:'post',
        data:$('#myForm').serialize(),
        success:function(response){
          $scope.breakout = false;
          $scope.result = response.split(';');
          $('#output').html($scope.result[0]);
          $scope.ajax_success($scope.result[0]);
          $scope.progress_data = 'Estimated RANK : ';
          $scope.data_blue = $scope.result[1];
          $('.progress-bar').css('width 100%');
          $scope.pulse_animate = "";
          $scope.$digest();
          $('[data-toggle="tooltip"]').tooltip()
          $('#tooltip').tooltip({ placement: 'top-right', trigger: 'manual'}).tooltip('show');
        }
      });
      $scope.progress_data = "Please wait, Downloads is being ";
      $scope.data_blue = "Predicted!";
      $scope.pulse_animate = "animated_pulse pulse_head";
      $scope.circle_six_show = true;
      $scope.progress_show = true;
      var i = 1;
      var counterBack = setInterval(function(){
        i++;
        if(i<86 && $scope.breakout == true){
          $('.progress-bar').css('width', (i*1.17)+'%');
        } else {
          clearTimeout(counterBack);
        }
        
      }, 1000);
    }
    
    $scope.ajax_success = function(data){
      console.log("AJAX Function Success");
      if(data == " < 100,000"){
        $scope.progress_tool = "Very Low";
      }
      else if(data == "100,000 - 1,000,000"){
        $scope.progress_tool = "Low";
      }
      else if(data == "1,000,000 - 10,000,000"){
        $scope.progress_tool = "Medium";
      }
      else if(data == "10,000,000 - 100,000,000"){
        $scope.progress_tool = "High";
      }
      else if(data == "100,000,000 - 1,000,000,000"){
        $scope.progress_tool = "Very High";
      }
    }
    
    $scope.clear_form = function(data) {      
      if(data == 0){
        $scope.type1 = {};
      }
      else{
        $scope.type2 = {};
      }
    }
    
    $scope.circle = function(data){
      $scope.circle_one_class = 'animated zoomInUp';
      if(data == 1){
        $scope.circle_one_show = true;
      }
      else if(data == 2){
        $scope.circle_two_show = true;
      }
      else if(data == 3){
        $scope.circle_three_show = true;
      }
      else if(data == 4){
        $scope.circle_four_show = true;
      }
      else if(data == 5){
        $scope.circle_five_show = true;
      }
    }
    
    $scope.animateOut = function(data){
      if(data == 0){
        $scope.show_img = false;
        $scope.show_type1 = true;
        $scope.show_type2 = false;
      }
      else{
        $scope.show_img = false;
        $scope.show_type1 = false;
        $scope.show_type2 = true; 
      }
    }
    
    $scope.animateIn = function(){
      $scope.show_img = true;
      $scope.show_type1 = false;
      $scope.show_type2 = false;
    }
  }]);
