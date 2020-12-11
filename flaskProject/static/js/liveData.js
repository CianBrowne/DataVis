var queryValues = [];

function prepare(names){
    console.log(names)
    let json = {
        query1: names[0],
        query2: names[1]
    };
    queryValues.push(names[0], names[1])
    fetch(`${window.origin}/prepare`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(json),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(){
        live()
        setInterval(updateCSV, 300*1000)
    }

    )

}
function updateCSV(){
    let json = {
        query1: queryValues[0],
        query2: queryValues[1]
    };
      fetch(`${window.origin}/updateCSV`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(json),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
}
function live(){
    Highcharts.chart('container3', {
    chart: {
        type: 'bar',
    },
    title: {
        text: 'Server Monitoring Demo'
    },
    legend: {
        enabled: false
    },
    subtitle: {
        text: 'Instance Load'
    },
    data: {
        googleSpreadsheetKey: '1g7eECgPd-06Ql6dsIYyp_lvUMXvnVW1f9ddOgKg_qIU',
        enablePolling: true,
        dataRefreshRate: 20
    },
    plotOptions: {
        bar: {
            colorByPoint: true
        },
    },
    tooltip: {
        valueDecimals: 1,
        valueSuffix: '%'
    },
    xAxis: {
        type: 'category',
        labels: {
            style: {
                fontSize: '10px'
            }
        }
    },
    yAxis: {
        title: false,

    }
});
}
