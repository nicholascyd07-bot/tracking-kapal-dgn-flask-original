document.addEventListener('DOMContentLoaded', function () {
    const downloadBtn = document.getElementById('btn-download-chart');
    const chartImg = document.getElementById('disaster-chart');

    if (downloadBtn && chartImg) {
        downloadBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const imageSrc = chartImg.getAttribute('src');

            if (imageSrc) {
                const link = document.createElement('a');
                link.href = imageSrc;
                link.download = 'disaster_type_pie.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        });
    }
});