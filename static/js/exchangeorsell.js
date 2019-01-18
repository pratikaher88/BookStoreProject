document.getElementById("priceid").disabled = true;

var sell_or_exchange = $("#id_sell_or_exchange");

function refreshOptions() {
    if (sell_or_exchange.val() === "Sell") {
        document.getElementById("priceid").disabled = false;
    } else {
        if (sell_or_exchange.val() === "Exchange") {
            document.getElementById("priceid").value = '';
            document.getElementById("priceid").disabled = true;
        }
    }
}
refreshOptions();

sell_or_exchange.on("change", refreshOptions);
