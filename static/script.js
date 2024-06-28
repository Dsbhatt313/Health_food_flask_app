document.addEventListener('DOMContentLoaded', () => {
    const formSections = document.querySelectorAll('form section');
    const nextButtons = document.querySelectorAll('.next-section');
    const prevButtons = document.querySelectorAll('.prev-section');
    let currentSection = 0;

    nextButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            if (validateSection(formSections[currentSection])) {
                formSections[currentSection].style.display = 'none';
                currentSection++;
                formSections[currentSection].style.display = 'block';
            }
        });
    });

    prevButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            formSections[currentSection].style.display = 'none';
            currentSection--;
            formSections[currentSection].style.display = 'block';
        });
    });

    function validateSection(section) {
        const inputs = section.querySelectorAll('input, select, textarea');
        for (let input of inputs) {
            if (!input.checkValidity()) {
                input.reportValidity();
                return false;
            }
        }
        return true;
    }

    formSections.forEach((section, index) => {
        if (index !== currentSection) {
            section.style.display = 'none';
        }
    });
});
