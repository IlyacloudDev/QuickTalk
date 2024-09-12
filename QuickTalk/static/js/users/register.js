document.getElementById('registerForm').addEventListener('submit', function(event){
    // Останавливаем стандартное поведение формы (перезагрузку страницы)
    event.preventDefault();

    // Получаем элементы полей ввода
    const phoneNumberInput = document.getElementById('phone_number');
    const passwordInput = document.getElementById('password');
    const password2Input = document.getElementById('password2');

    // Очищаем предыдущие ошибки, если они были
    document.getElementById('phone_number_error').style.display = 'none';  // Прячем текст ошибки
    document.getElementById('password_error').style.display = 'none';  
    document.getElementById('password2_error').style.display = 'none';  
    phoneNumberInput.classList.remove('is-invalid');  // Убираем красную границу с поля
    passwordInput.classList.remove('is-invalid'); 
    password2Input.classList.remove('is-invalid');

    // Собираем данные формы для отправки на сервер
    const data = {
        phone_number: phoneNumberInput.value,  // Получаем значение телефона
        password: passwordInput.value,  // Получаем значение пароля
        password2: password2Input.value, // Получаем значение подтверждения пароля
    };

    // Делаем запрос на сервер
    fetch(window.REGISTER_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Формат данных JSON
            'X-CSRFToken': '{{ csrf_token }}' // Добавляем CSRF токен для защиты
        },
        body: JSON.stringify(data) // Преобразуем данные в формат JSON
    })
    .then(response => {
        // Если сервер вернул код 400 (ошибка валидации), преобразуем JSON-ответ в JS-объект для дальнейшей работы
        if (response.status === 400) {
            return response.json();
        }
        // Если сервер вернул успешный ответ, также преобразуем JSON-ответ в JS-объект для дальнейшей работы
        else if (response.ok) {
            return response.json();
        } else {
            // Если что-то пошло не так, вызываем ошибку
            throw new Error('Something went wrong');
        }
    })
    .then(result => {
        if (result.phone_number || result.password || result.password2) {
            // Если есть ошибка с полем "phone_number", отображаем её
            if (result.phone_number) {
                const phoneError = document.getElementById('phone_number_error');  // Находим элемент для ошибки
                phoneError.textContent = result.phone_number[0];  // Устанавливаем текст ошибки
                phoneError.style.display = 'block';  // Показываем ошибку
                phoneNumberInput.classList.add('is-invalid');  // Добавляем красную рамку полю
            }
            // Если есть ошибка с полем "password", отображаем её
            if (result.password) {
                const passwordError = document.getElementById('password_error');  // Находим элемент для ошибки
                passwordError.textContent = result.password[0];  // Устанавливаем текст ошибки
                passwordError.style.display = 'block';  // Показываем ошибку
                passwordInput.classList.add('is-invalid');  // Добавляем красную рамку полю
            }
            // Если есть ошибка с полем "password", отображаем её
            if (result.password2) {
                const password2Error = document.getElementById('password2_error');  // Находим элемент для ошибки
                password2Error.textContent = result.password[0];  // Устанавливаем текст ошибки
                password2Error.style.display = 'block';  // Показываем ошибку
                password2Input.classList.add('is-invalid');  // Добавляем красную рамку полю
            }
        } else if (result.new_user) {
            // Если пользователь создался, перенаправляем его на страницу для входа
            window.location.href = window.LOGIN_PAGE_URL
        }
    })
    .catch(error => {
    // Обрабатываем ошибку запроса
    console.error('Error:', error);
    });
});