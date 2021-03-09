const button = document.getElementById('clear-cart');

button.addEventListener('click', function () {
        if (confirm('Вы точно хотите очистить корзину???')) {
            const link = document.createElement('a');
            link.setAttribute('href', '/clear_cart');
            link.click();
        }
    }
)
