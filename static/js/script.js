var variants = 5;
function addOption() {
    if (variants > 9) {
        alert('Максимальное кол-во вариантов: 10');
    } else {
        variants++;
        $("#options").append('<input id="option_' + variants + '" type="text" name="option[]" placeholder="Вариант №' + variants + '" class="form-control x"/>');
    }
}

function deleteOption() {
    if (variants < 3) {
        alert('Минимальное кол-во вариантов: 2');
    } else {
        $("#option_" + variants).remove();
        variants--;
    }
}

function captchaRefresh() {
    $("#captcha").html('<img src="/captcha/" alt="" id="captcha"/>');
}