$(document).ready(function() {
    let currentImage = null;

    function getFreqColor(r, c) {
        // Simple heuristic for frequency separation in 8x8 block
        const dist = r + c;
        if (dist < 5) return 'freq-low';
        if (dist < 10) return 'freq-med';
        return 'freq-high';
    }

    function renderMatrix(containerId, table) {
        const $container = $('#' + containerId);
        $container.empty();
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const val = table[r][c];
                const colorClass = getFreqColor(r, c);
                $container.append(`<div class="matrix-cell ${colorClass}">${val}</div>`);
            }
        }
    }

    function updateQuantizationData() {
        const quality = $('#quality-input').val();
        $('#quality-val').text(quality);
        $('#target-quality').text(quality);

        $.ajax({
            url: '/api/quantization_data',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ quality: quality }),
            success: function(data) {
                renderMatrix('base-matrix', data.base_table);
                renderMatrix('resulting-matrix', data.resulting_table);
                $('#scale-factor').text('x ' + data.scale.toFixed(2));

                // Update formula display
                let scaleFormula = "";
                if (quality < 50) {
                    scaleFormula = `Quality < 50: S = 5000 / ${quality} = ${(5000/quality).toFixed(2)}`;
                } else {
                    scaleFormula = `Quality >= 50: S = 200 - 2 * ${quality} = ${(200 - 2 * quality).toFixed(2)}`;
                }
                $('#formula-scale').text(scaleFormula);
            }
        });
    }

    function updatePreview() {
        if (!currentImage) return;

        // Show loading spinner and clear previous reconstructed image
        $('#loading-spinner').show();
        $('#preview-reconstructed-container').empty();
        $('#psnr-val').text('-');

        const quality = $('#quality-input').val();
        const formData = new FormData();
        formData.append('image', currentImage);
        formData.append('quality', quality);

        $.ajax({
            url: '/api/quantization_preview',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                $('#loading-spinner').hide();
                $('#preview-original-container').html(`<img src="data:image/png;base64,${data.original}" class="img-preview shadow-sm">`);
                $('#preview-reconstructed-container').html(`<img src="data:image/png;base64,${data.reconstructed}" class="img-preview shadow-sm">`);
                $('#psnr-val').text(data.psnr.toFixed(2));

                // Update download links
                $('#dl-reconstructed-png').attr('href', 'data:image/png;base64,' + data.reconstructed);
                $('#dl-reconstructed-bmp').attr('href', 'data:image/bmp;base64,' + data.reconstructed_bmp);
                $('#dl-reconstructed-jpg').attr('href', 'data:image/jpeg;base64,' + data.reconstructed_jpg);
                $('#download-links').show();
            },
            error: function(xhr, status, error) {
                $('#loading-spinner').hide();
                console.error("Error updating preview: " + error);
                $('#preview-reconstructed-container').html(`<p class="text-danger">Error processing image</p>`);
            }
        });
    }

    // Debounce preview updates
    let timeout = null;
    $('#quality-input').on('input', function() {
        $('#quality-val').text($(this).val());
        $('#target-quality').text($(this).val());

        clearTimeout(timeout);
        timeout = setTimeout(function() {
            updateQuantizationData();
            updatePreview();
        }, 100);
    });

    $('#image-input').on('change', function(e) {
        currentImage = e.target.files[0];
        updatePreview();
    });

    // Initial load
    updateQuantizationData();
});
