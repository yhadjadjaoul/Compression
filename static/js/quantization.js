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

                // Update formula display if needed
                let scaleFormula = "";
                if (quality < 50) {
                    scaleFormula = `Qualité < 50 : S = 5000 / ${quality} = ${(5000/quality).toFixed(2)}`;
                } else {
                    scaleFormula = `Qualité >= 50 : S = 200 - 2 * ${quality} = ${(200 - 2 * quality).toFixed(2)}`;
                }
                $('#formula-scale').text(scaleFormula);
            }
        });
    }

    function updatePreview() {
        if (!currentImage) return;
        console.log("Updating preview for quality: " + $('#quality-input').val());

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
                console.log("Preview data received, PSNR: " + data.psnr);
                $('#preview-original-container').html(`<img src="data:image/png;base64,${data.original}" class="img-preview shadow-sm">`);
                $('#preview-reconstructed-container').html(`<img src="data:image/png;base64,${data.reconstructed}" class="img-preview shadow-sm">`);
                $('#psnr-val').text(data.psnr.toFixed(2));
            },
            error: function(xhr, status, error) {
                console.error("Error updating preview: " + error);
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
