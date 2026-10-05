document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('select-all-magtype');
    const itemCheckboxes = document.querySelectorAll('.magtype-item');

    if (!selectAllCheckbox || itemCheckboxes.length === 0) return;

    // Fungsi untuk memperbarui status "Pilih Semua"
    function updateSelectAllStatus() {
        const allChecked = Array.from(itemCheckboxes).every(cb => cb.checked);
        selectAllCheckbox.checked = allChecked && itemCheckboxes.length > 0;
    }

    // 1. Saat "Pilih Semua" diklik -> centang / lepas centang seluruh opsi
    selectAllCheckbox.addEventListener('change', function() {
        itemCheckboxes.forEach(cb => {
            cb.checked = selectAllCheckbox.checked;
        });
    });

    // 2. Jika salah satu opsi diklik -> perbarui status "Pilih Semua"
    itemCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateSelectAllStatus);
    });

    // Jalankan sekali saat halaman selesai dimuat
    updateSelectAllStatus();
});