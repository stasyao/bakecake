// Скрипт подгрузился, взяли текущую цену из конструктора торта
const priceFromConstructor = Number.parseInt(
    document.querySelector('#total_price').textContent
);

// Собираем в DOM нужные элементы
const currentPriceDisplay = document.querySelector('#total_price');
const deliveryDateTimeInput = document.querySelector('#id_delivery_time');
const userPromoCodeBlock = document.querySelector('#promoBlock');
const userPromoCodeInput = document.querySelector('#promo');
const userPromoCodeHiddenInput = document.querySelector('#promo_code');
const promoCodeCheckingResult = document.querySelector('#promocode_checking');
const totalPriceHiddenInput = document.querySelector('#price');
const orderForm = document.querySelector('.form-group');
const totalPriceLabel = document.querySelector('#cakePriceLabel');

/*
Логика подсчета итоговой цены
*/
// Вводим переменные для коэффициента срочности и коэффициента промокода
let urgencyRate = 0;
let promoCodeRate = 0;
// Функция для подсчета цены
const getTotalPrice = () => priceFromConstructor * (
    1 - promoCodeRate + urgencyRate
);

/* Логика изменения лэйбла поля с ценой */
const showPriceLabel = () => {
    if (promoCodeRate && urgencyRate) {
        totalPriceLabel.innerHTML = '<span class="text-success">&ndash;промокод</span> <span class="text-danger">+срочность</span>';
    } else if (promoCodeRate) {
        totalPriceLabel.innerHTML = '<span class="text-success">&ndash;промокод</span>'
    } else if (urgencyRate) {
        totalPriceLabel.innerHTML = '<span class="text-danger">+срочность</span>'
    } else {
        totalPriceLabel.innerHTML = ''
    }
}

/*
Логика изменения цены в зависимости от промокода
*/
const changePriceDueToUrgency = () => {
    const startTime = Date.now();
    const endTime = Date.parse(deliveryDateTimeInput.value);
    const interval = (endTime - startTime) / 3600000;
    const notification = document.querySelector('#raise_price_notification');
    if (interval < 5) {
        urgencyRate = 0;
        notification.innerHTML = '<span style="color: red;">Время доставки меньше 5 часов, так быстро только пирожков можно напечь</span>';
    }
    if (interval >= 5 && interval < 24) {
        urgencyRate = 0.2;
        notification.innerHTML = 'Доставка в пределах 24 часов увеличивает цену на 20%';
    }
    if (interval >= 24) {
        urgencyRate = 0;
        notification.innerHTML = '';
    }
    currentPriceDisplay.innerHTML = `${getTotalPrice()} &#8381;`;
    showPriceLabel();
}

/*
Логика изменения цены в зависимости от промокода
*/

// список для хранения полученных с сервера данных о промокоде
// с этими данными будут сравниваться инпуты юзера
const promoCodeStatus = [];
// функция для запроса к API, ответ распиливается и помещается в список promoCodeStatus
async function getPromoCodeStatus() {
    const response = await fetch('http://localhost:8000/get_code');
    const { actualCode, thisClientUsed } = await response.json();
    console.log(actualCode);
    promoCodeStatus.push(actualCode, thisClientUsed);
}

const userPromoCodeInputHandler = () => {
        const userInput = document.querySelector('#promo').value;
        // распиливаем полученные от сервера данные
        const [actualCode, thisClientUsed] = promoCodeStatus;
        if (userInput === actualCode) {
            if (thisClientUsed) {
                promoCodeCheckingResult.classList.add('text-danger');
                promoCodeCheckingResult.innerHTML = 'Вы уже использовали этот промокод.';
            } else {
                // если промик верный и используют впервые отключаем инпут, он уже незачем
                userPromoCodeInput.disabled = true;
                promoCodeCheckingResult.classList.add('text-success');
                promoCodeCheckingResult.classList.remove('text-danger');
                promoCodeCheckingResult.innerHTML = 'Ура! Промокод верный! Ваша скидка &mdash; 20%.\nСтоимость заказа пересчитана.';
                userPromoCodeHiddenInput.value = actualCode;
                // Обновляем коэффициент цены с промокодом
                promoCodeRate = 0.2;
                // Выводим цену с учетом промика и срочности заказа
                currentPriceDisplay.innerHTML = `${getTotalPrice()} &#8381;`;
                showPriceLabel();
            }
        } else if (userInput.length > 0) {
            promoCodeCheckingResult.innerHTML = 'К сожалению, у нас нет такого промокода.';
            promoCodeCheckingResult.classList.remove('text-success');
            promoCodeCheckingResult.classList.add('text-danger');
        } else {
            promoCodeCheckingResult.innerHTML = '';
        }
    }

/* Вешаем слушателей */
window.addEventListener(
    'load',
    async () => {
        // запрашиваем с сервера данные об актуальном промокоде
        await getPromoCodeStatus();
        const [actualCode, _] = promoCodeStatus;
        // блокируем поле с промиком, если актуальных промиков нет
        if (!actualCode) {
            userPromoCodeBlock.remove();
        }
    }
)

// Повесили слушателя события инпута в поле с датой и временем
deliveryDateTimeInput.addEventListener(
    'input',
    changePriceDueToUrgency
)

// Повесили слушателя события инпута в поле для ввода промика
userPromoCodeInput.addEventListener(
    'keyup',
    userPromoCodeInputHandler
)

// Повесли слушателя на сабмит формы, чтобы он пробросил в скрытый инпут итоговую цену
orderForm.addEventListener(
    'submit',
    () => {
        totalPriceHiddenInput.value = getTotalPrice();
    }
)
