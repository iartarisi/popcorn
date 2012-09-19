google.setOnLoadCallback(packages_by_distro);

function packages_by_distro() {
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Distro');
    data.addColumn('number', 'Packages');
    data.addRows({{ distro_packages|safe }});

    // Set chart options
    var options = {
        chartArea: {width: '100%', height: '70%'},
        backgroundColor: '#f7f7f7'
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('distro_packages_chart'));
    chart.draw(data, options);
}