$(document).ready(function() {
    $('#quality-input').on('input', function() {
        $('#quality-val').text($(this).val());
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
                $('#download-link').attr('href', 'data:image/png;base64,' + data.reconstructed);

                // Update stats
                $('#stat-total-symbols').text(data.huffman_stats.total_symbols);
                $('#stat-unique-symbols').text(data.huffman_stats.unique_symbols);
                $('#stat-encoded-bits').text(data.huffman_stats.encoded_bits);
                $('#stat-original-bits').text(data.huffman_stats.original_bits);

                const ratio = (data.huffman_stats.original_bits / data.huffman_stats.encoded_bits).toFixed(2);
                $('#stat-ratio').text(ratio + ':1');
                $('#stat-psnr').text(data.psnr.toFixed(2) + ' dB');
            },
            error: function(xhr, status, error) {
                $('#loading').hide();
                $('#submit-btn').prop('disabled', false);
                alert('Error processing image: ' + error);
            }
        });
    });
});
