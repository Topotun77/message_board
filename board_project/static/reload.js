function autoRefresh() {
    const refreshElement = document.getElementById('reload');
    if (refreshElement) {
        setTimeout(() => {
            location.reload(true);
        }, 10000);
        console.log("Страница обновляется...");
    } else {
        console.log("Элемент с id='reload' отсутствует.");
    }
}
window.onload = autoRefresh;