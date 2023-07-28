import startPage from './startPage.js';
import doSelect from './doSelect.js';

$(document).ready(function () {
    $("#root").html(startPage());
    setInterval(() => {
        doSelect()
    }, 1000);
});
