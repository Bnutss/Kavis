document.addEventListener('DOMContentLoaded', function () {
    const loader = document.getElementById('loader');
    const container = document.querySelector('.container');
    const langButtons = document.querySelectorAll('.lang-btn');
    const langForm = document.getElementById('langForm');
    const form = document.querySelector('.login-form');
    const errorBox = document.getElementById('errorBox');
    const inputs = document.querySelectorAll('.input-group input');

    setTimeout(() => {
        loader.classList.add('hidden');
        container.classList.add('visible');
    }, 1500);

    langButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const selectedLang = this.dataset.lang;
            const languageInput = langForm.querySelector('input[name="language"]');

            loader.classList.remove('hidden');
            container.classList.remove('visible');

            if (languageInput) {
                languageInput.value = selectedLang;
            } else {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'language';
                input.value = selectedLang;
                langForm.appendChild(input);
            }

            setTimeout(() => {
                langForm.submit();
            }, 300);
        });
    });

    inputs.forEach(input => {
        input.addEventListener('input', function () {
            if (errorBox.classList.contains('active')) {
                errorBox.classList.remove('active');
            }
        });

        input.addEventListener('blur', function () {
            if (this.value) {
                this.setAttribute('valid', '');
            } else {
                this.removeAttribute('valid');
            }
        });
    });

    form.addEventListener('submit', function (e) {
        const username = document.getElementById('id_username').value.trim();
        const password = document.getElementById('id_password').value;

        if (!username || !password) {
            e.preventDefault();

            const errorMessages = {
                'tr': 'Lütfen tüm alanları doldurun',
                'en': 'Please fill in all fields'
            };

            const currentLang = document.documentElement.lang || 'tr';
            errorBox.textContent = errorMessages[currentLang] || errorMessages['tr'];
            errorBox.classList.add('active');

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderBottomColor = '#ff3333';
                    setTimeout(() => {
                        input.style.borderBottomColor = '';
                    }, 2000);
                }
            });
            return;
        }

        const submitBtn = form.querySelector('.submit-btn');
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
    });

    setTimeout(() => {
        document.querySelector('.login-box').style.animation = 'fadeInUp 0.8s ease forwards';
    }, 1600);
});

const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);