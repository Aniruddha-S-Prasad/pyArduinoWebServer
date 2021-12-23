Highcharts.chart('container', {
    chart: {
      type: 'spline',
      animation: Highcharts.svg, // don't animate in old IE
      marginRight: 10,
      events: {
        load: function () {
  
          // set up the updating of the chart each second
          var series = this.series[0];
          setInterval(() => {
            var x = (new Date()).getTime();// current time
            fetch("/data")
                .then(response => response.json())
                .then(data => {
                    console.log(data.temperature)
                    if (series.data.length > 40) {
                        series.addPoint([x, data.temperature], true, true);
                    }
                    else {
                        series.addPoint([x, data.temperature], true, false);
                    }
                })
            
          }, 2500);
        }
      }
    },
  
    time: {
      useUTC: false
    },
  
    title: {
      text: 'Live random data'
    },
  
    accessibility: {
      announceNewData: {
        enabled: true,
        minAnnounceInterval: 15000,
        announcementFormatter: function (allSeries, newSeries, newPoint) {
          if (newPoint) {
            return 'New point added. Value: ' + newPoint.y;
          }
          return false;
        }
      }
    },
  
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150
    },
  
    yAxis: {
      title: {
        text: 'Value'
      },
      plotLines: [{
        value: 0,
        width: 1,
        color: '#808080'
      }]
    },
  
    tooltip: {
      headerFormat: '<b>{series.name}</b><br/>',
      pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}<br/>{point.y:.2f}'
    },
  
    legend: {
      enabled: false
    },
  
    exporting: {
      enabled: false
    },
  
    series: [{
      name: 'Random data',
      data: []
    }]
  });