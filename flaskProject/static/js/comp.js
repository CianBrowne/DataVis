let containers = ['container', 'container2']
// let drilldownArray = [];
//
// let drilldown1 = [drilldownArray[0], drilldownArray[1]]
// let drilldown2 = [drilldownArray[2], drilldownArray[3]]
// function drilldownData(data){
//     //console.log(data)
//     let id = (data[0].split(" ")[0].toLowerCase())
//     for(i in data){
//         if(i != 0){
//             //console.log(data[i].drilldown)
//         let json = {"name": data[i].name, "id": data[i].drilldown, "y": data[i].y }
//         drilldownArray.push(json)
//         }
//
//     }
//     console.log(drilldownArray)
// }
function test(info, drilldownData){
    let drillArray = []
    let drillArray2 = []
    for(i in drilldownData){
        if(i != 0){
            let json = {"name": drilldownData[i].name, "id": drilldownData[i].drilldown, "y": drilldownData[i].y }
            drillArray.push(json)
        }
    }
    for(i in drilldownData){
        if(i != 0){
            drillArray2.push([drilldownData[i].name, drilldownData[i].y])
        }
    }
    console.log(drillArray2)
    console.log(drillArray)
    let settings = info[0]
   // console.log(settings)
    info.shift()
    let data = info
    console.log(data)
    //console.log(settings)
    let container = containers[0]
    containers.shift()
    //console.log(containers)
   // let test = JSON.parse(data)
    //console.log(test)
    console.log(data)
    Highcharts.chart(container, {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: settings
    },
    tooltip: {
      pointFormat: '<b>{point.y:,.0f}</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Sentiment',
        colorByPoint: true,
        data: data
    }],
        drilldown: {
            series: [{
                name: drillArray[0].name,
                id: drillArray[0].id,
                data:[
                    [
                        drillArray[0].name,
                        drillArray[0].y
                    ],
                    [
                        drillArray[1].name,
                        drillArray[1].y
                    ]
                ]
            }]
        }
});
}