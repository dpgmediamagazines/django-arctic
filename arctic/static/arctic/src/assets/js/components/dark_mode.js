var startDarkToggle = function() {
    var darkModeRadio = document.getElementsByName("dark-option");
    var darkModeContainer = document.getElementById('dark-mode-container');
    var lightRadio = document.getElementById('light-radio');
    var darkRadio = document.getElementById('dark-radio');
    if(darkModeContainer) {
        darkModeContainer.classList.remove('hide');
        for (let i = 0; i < darkModeRadio.length; i++) {
            darkModeRadio[i].addEventListener("change", function(event) {
                toggleDark(darkRadio.checked);
                localStorage.setItem('darkMode', darkRadio.checked);
                var darkModeStorage = localStorage.getItem('darkMode');
            });
        }
    }

    // check if dark mode is on
    var darkModeStorage = localStorage.getItem('darkMode');
    if (darkModeStorage == 'true') {
        if (darkRadio) {
            darkRadio.checked = true; //does not trigger change event
        }
        toggleDark(true);
    }
}
var startDarkMode = function(darkMode) {
    var mqd = window.matchMedia("(prefers-color-scheme: dark)");
    if (darkMode != 'toggle') {
        // check if browser does not suport and turn on toggle
        if (!mqd.matches) {
            var mql = window.matchMedia("(prefers-color-scheme: light)");
            var mqnp = window.matchMedia("(prefers-color-scheme: no-preference)");
            if (!mql.matches && !mqnp.matches) {
                startDarkToggle();
                return false;
            }
        }
        mqd.addListener(toggleDark);
        document.addEventListener("DOMContentLoaded", function() {
            toggleDark(mqd.matches);
        });

    } else {
        startDarkToggle();
    }
}

function toggleDark(state) {
    if (state) {
        document.body.classList.add("dark");
    } else {
        document.body.classList.remove("dark");
    }
}
