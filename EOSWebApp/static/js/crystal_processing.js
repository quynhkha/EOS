// $("#btn_table_1").onclick(function(e){
//     e.preventDefault();
//     mask_id = document.getElementById('mask_id');
//     url
//     }
//
// );
$(".btn_modal_show_individual_crystal").click(function (e) {
        e.preventDefault();
      crystal_id = $(this).val();
    $.ajax({
        type: "GET",
        url: '/modal-show-individual-crystal/'+ crystal_id.toString() + "/",
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


function plot_confusion_graph(data){
    var graph_data = [
  {
    x: data['labels'],
    y: data['similarities'],
    type: 'bar'
  }
];

Plotly.newPlot('confusion-graph', graph_data);
}

$(".btn_modal_show_conf_graph").click(function (e) {
    e.preventDefault();
    id = $(this).val();
    $.ajax({
        type: "GET",
        url: "/modal-show-conf-graph/" + id.toString() + "/" ,

        success: function (data) {
            plot_confusion_graph(data);
            console.log(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});
