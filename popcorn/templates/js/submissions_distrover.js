google.setOnLoadCallback(submissions_by_distrover);

function submissions_by_distrover() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Distro');
    data.addColumn('number', 'Submissions');
    data.addRows({{submissions_distrover}});

    var options = {
        vAxis: {title: 'Submissions',  titleTextStyle: {color: '#D9230F'}},
        hAxis: {title: 'Distro', titleTextStyle: { color: '#D9230F'}},
        backgroundColor: '#f7f7f7'
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('submissions_distrover'));
    chart.draw(data, options);
}
