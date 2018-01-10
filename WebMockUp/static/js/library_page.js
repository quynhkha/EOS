
$(".btn_modal_show_crystal").click(function (e) {
        e.preventDefault();
      mask_id = $(this).val();
    $.ajax({
        type: "GET",
        url: '/modal-show-crystal/'+ mask_id.toString() + "/",
         beforeSend: function () {
            document.body.style.cursor = "wait";
            document.getElementById('modal-crystal-img').src ='';
        },
           complete: function () {
            document.body.style.cursor = "default";
        },
        success: function (data) {
          document.getElementById('modal-crystal-img').src = "data:image/jpeg;charset=utf-8;base64,"+data['image_data'];
          document.getElementById('modal-crystal-name').innerText = data['image_name'];
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});

// $(".btn_download_crystal").click(function(e){
//        e.preventDefault();
//       mask_id = $(this).val();
//     $.ajax({
//         type: "GET",
//         url: '/download-crystal/'+ mask_id.toString() + "/",
//          beforeSend: function () {
//             document.body.style.cursor = "wait";
//         },
//            complete: function () {
//             document.body.style.cursor = "default";
//         },
//         success: function (data) {
//             alert("Downloaded");
//         },
//         error: function (data) {
//             console.log(data);
//             alert('error');
//         }
//     });
// });

