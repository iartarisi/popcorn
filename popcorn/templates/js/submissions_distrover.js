google.setOnLoadCallback(submissions_by_distrover);

function submissions_by_distrover() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Distro');
    data.addColumn('number', 'Submissions');
    data.addRows({{submissions_distrover}});

    var options = {
        backgroundColor: '#f7f7f7',
        chartArea: {width: '100%', height: '70%'},
        legend: {position: 'in'}
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('submissions_distrover'));
    chart.draw(data, options);
}
