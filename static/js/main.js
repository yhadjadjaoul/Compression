$(document).ready(function() {
    let metricsChart = null;
    let currentData = null;

    $('#quality-input').on('input', function() {
        $('#quality-val').text($(this).val());
    });

    $('#metric-select').on('change', function() {
        if (currentData) {
            updateUI(currentData);
        }
    });

    $('#upload-form').on('submit', function(e) {
        e.preventDefault();

        const formData = new FormData();
        const imageFile = $('#image-input')[0].files[0];
        const quality = $('#quality-input').val();

        if (!imageFile) return;

        formData.append('image', imageFile);
        formData.append('quality', quality);

        $('#results').hide();
        $('#loading').show();
        $('#submit-btn').prop('disabled', true);

        $.ajax({
            url: '/process',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                currentData = data;
                $('#loading').hide();
                $('#results').show();
                $('#submit-btn').prop('disabled', false);

                // Update images
                $('#img-original').attr('src', 'data:image/png;base64,' + data.original);
                $('#img-r').attr('src', 'data:image/png;base64,' + data.r_channel);
                $('#img-g').attr('src', 'data:image/png;base64,' + data.g_channel);
                $('#img-b').attr('src', 'data:image/png;base64,' + data.b_channel);
                $('#img-y').attr('src', 'data:image/png;base64,' + data.y_channel);
                $('#img-u').attr('src', 'data:image/png;base64,' + data.u_channel);
                $('#img-v').attr('src', 'data:image/png;base64,' + data.v_channel);
                $('#img-dct').attr('src', 'data:image/png;base64,' + data.dct_y);
                $('#img-reconstructed').attr('src', 'data:image/png;base64,' + data.reconstructed);

                // Update download links
                $('#dl-original').attr('href', 'data:image/png;base64,' + data.original);
                $('#dl-original-bmp').attr('href', 'data:image/bmp;base64,' + data.original_bmp);
                $('#dl-r').attr('href', 'data:image/png;base64,' + data.r_channel);
                $('#dl-r-bmp').attr('href', 'data:image/bmp;base64,' + data.r_channel_bmp);
                $('#dl-g').attr('href', 'data:image/png;base64,' + data.g_channel);
                $('#dl-g-bmp').attr('href', 'data:image/bmp;base64,' + data.g_channel_bmp);
                $('#dl-b').attr('href', 'data:image/png;base64,' + data.b_channel);
                $('#dl-b-bmp').attr('href', 'data:image/bmp;base64,' + data.b_channel_bmp);
                $('#dl-y').attr('href', 'data:image/png;base64,' + data.y_channel);
                $('#dl-y-bmp').attr('href', 'data:image/bmp;base64,' + data.y_channel_bmp);
                $('#dl-u').attr('href', 'data:image/png;base64,' + data.u_channel);
                $('#dl-u-bmp').attr('href', 'data:image/bmp;base64,' + data.u_channel_bmp);
                $('#dl-v').attr('href', 'data:image/png;base64,' + data.v_channel);
                $('#dl-v-bmp').attr('href', 'data:image/bmp;base64,' + data.v_channel_bmp);
                $('#dl-dct').attr('href', 'data:image/png;base64,' + data.dct_y);
                $('#dl-dct-bmp').attr('href', 'data:image/bmp;base64,' + data.dct_y_bmp);
                $('#dl-reconstructed-png').attr('href', 'data:image/png;base64,' + data.reconstructed);
                $('#dl-reconstructed-bmp').attr('href', 'data:image/bmp;base64,' + data.reconstructed_bmp);
                $('#dl-reconstructed-jpg').attr('href', 'data:image/jpeg;base64,' + data.reconstructed_jpg);

                // Update stats
                $('#stat-total-symbols').text(data.huffman_stats.total_symbols);
                $('#stat-unique-symbols').text(data.huffman_stats.unique_symbols);
                $('#stat-encoded-bits').text(data.huffman_stats.encoded_bits);
                $('#stat-original-bits').text(data.huffman_stats.original_bits);

                const ratio = (data.huffman_stats.original_bits / data.huffman_stats.encoded_bits).toFixed(2);
                $('#stat-ratio').text(ratio + ':1');

                updateUI(data);
            },
            error: function(xhr, status, error) {
                $('#loading').hide();
                $('#submit-btn').prop('disabled', false);
                alert('Error processing image: ' + error);
            }
        });
    });

    function updateUI(data) {
        const metric = $('#metric-select').val();
        const quality = $('#quality-input').val();

        let score = data[metric];
        let unit = metric === 'psnr' ? ' dB' : '';
        $('#stat-score').text(score.toFixed(4) + unit);

        $('#chart-title').text($('#metric-select option:selected').text().split(' ')[0]);
        updateMetricChart(data.metrics_plot_data, quality, metric);
    }

    function updateMetricChart(plotData, currentQuality, metric) {
        const ctx = document.getElementById('metrics-chart').getContext('2d');
        const labels = plotData.map(d => d.quality);
        const values = plotData.map(d => d[metric]);
        const labelName = $('#metric-select option:selected').text().split(' ')[0];

        if (metricsChart) {
            metricsChart.destroy();
        }

        metricsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: labelName,
                    data: values,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    pointBackgroundColor: labels.map(q => q == currentQuality ? 'red' : 'rgb(75, 192, 192)'),
                    pointRadius: labels.map(q => q == currentQuality ? 6 : 3)
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Quality'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: labelName
                        }
                    }
                }
            }
        });
    }
});
