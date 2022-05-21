$(document).ready(function(){
    $(window).on("resize",(e)=>{
        if ($(".ContentTable").width() > $(".ContentTable").parent().width())
            $(this.Element).addClass("ContentTableResponsive");
        else
            $(this.Element).removeClass("ContentTableResponsive");
    })
    $(window).trigger("resize")
    HideLightBox()
    $("#AllLightBox").click(function(e){
        if(e.target === this)
            HideLightBox()
    })
})

function convertFaNumber(str) {
    var persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g];
    var arabicNumbers = [/٠/g, /١/g, /٢/g, /٣/g, /٤/g, /٥/g, /٦/g, /٧/g, /٨/g, /٩/g];
    for (var i = 0; i < 10; i++) {
        str = str.toString().replace(persianNumbers[i], i).replace(arabicNumbers[i], i);
    }
    return str;
}

function CallMethod(PageUrl, dataParam, SuccessFunction, FailFunction, HaveLoading) {
    if (HaveLoading)
        $("#AllLoading").fadeIn(500);
    if (SuccessFunction == undefined)
        SuccessFunction = function () { };
    if (FailFunction == undefined)
        FailFunction = function () { };

    if (dataParam != null && dataParam != "" && dataParam != undefined)
        dataParam = convertFaNumber(dataParam);

    $.ajax({
        type: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("userAgent", navigator.userAgent);
        },
        url: PageUrl,
        data: dataParam,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        timeout: 999999,
        success: function (response) {
            console.log(PageUrl)
            console.log(response)
            if (HaveLoading) {
                $("#AllLoading").fadeOut(250);
            }
            if (response.isSuccess == false) {
                ShowToast(response.statusMessage);
                return;
            }
            SuccessFunction(response.resultObject || response);
        },
        failure: function (response) {
            if (HaveLoading)
                $("#AllLoading").fadeOut(250, function () {
                    ShowToast("خطا در اتصال به سرویس دهنده");
                });
            else
                ShowToast("خطا در اتصال به سرویس دهنده");
            FailFunction(response.statusMessage);
        }
    });
}

function ShowToast(n) {
    $("#AllToast").addClass("show");
    $("#AllToast").html(n);
    setTimeout(function(){
        $("#AllToast").removeClass("show");
    },n.split(" ").length / 3 * 1e3 + 500)
}

function ShowLightBox(contentId,submitFunc,cancelFunc){
    $("#btnLigthBoxAccept").off("click")
    $("#btnLigthBoxAccept").on("click",function(e){
        submitFunc()
        HideLightBox()
    })

    $("#btnLightBoxCancel").off("click");
    $("#btnLightBoxCancel").show();
    if(cancelFunc)
        $("#btnLightBoxCancel").on("click",function(e){
            cancelFunc()
            HideLightBox(contentId)
        });
    else
        $("#btnLightBoxCancel").hide();
    $(contentId.startsWith("#") ? contentId : "#" + contentId).show().appendTo("#LightBoxContentContainer")
    
    $("#AllLightBox").show(250)
    
}

function HideLightBox(ct=""){
    if(ct)
        $(ct.startsWith("#") ? ct:"#"+ct).hide()
    $("#AllLightBox").hide(250)
}