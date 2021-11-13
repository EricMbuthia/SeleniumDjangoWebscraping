$(function(){
 //add notice
        $("#add_notice").click(function(e){
            e.preventDefault();
            random_form = $('#random_form').serialize();
            $.ajax({
                type: "POST",
                url:"create_db_notice/",
                data:random_form,
                beforeSend:function(){
                     alert("beforeSend");
    
                },
                cache: false,
                dataType: "json",
                success: function(data){
                    // alert(new_drug_category_data);
                    if (data.status === "ok"){
                        $("#my_alert_box").append("<div class='alert alert-success alert-dismissable'><button aria-hidden='true' data-dismiss='alert' class='close' type='button'> × </button>Drug Category Successfuly saved. </div></div>");
                        // $("#new_drug_category_form")[0].reset();
                    }
                    if (data.status === "error"){
                        $("#my_alert_box").append("<div class='alert alert-danger alert-dismissable'><button aria-hidden='true' data-dismiss='alert' class='close' type='button'> × </button> Error! Please check your data again </div></div>");
    
                    }
                    
                }
            });
            return false
        });


        
    //Sccrape Notice
    $("#scrape_notice").click(function(e){
        e.preventDefault();
        scrape_notice_data = $('#scrape_notice_form').serialize();
        $.ajax({
            type: "POST",
            url:"/spider1/inv_rec_update/",
            data:scrape_notice_data,
            beforeSend:function(){
                 alert("beforeSend");

            },
            cache: false,
            dataType: "json",
            success: function(data){
                // alert(new_drug_category_data);
                if (data.status === "ok"){
                    $("#my_alert_box").append("<div class='alert alert-success alert-dismissable'><button aria-hidden='true' data-dismiss='alert' class='close' type='button'> × </button>Drug Category Successfuly saved. </div></div>");
                    $("#scrape_notice_form")[0].reset();
                }
                if (data.status === "error"){
                    $("#my_alert_box").append("<div class='alert alert-danger alert-dismissable'><button aria-hidden='true' data-dismiss='alert' class='close' type='button'> × </button> Error! Please check your data again </div></div>");

                }
                
            }
        });
        return false
    });


//add notice
$("#write_scrape_notice").click(function(e){
    e.preventDefault();
    random_form = $('#random_form2').serialize();
    $.ajax({
        type: "POST",
        url:"/spider1/write_notices_to_file/",
        data:random_form,
        beforeSend:function(){
             alert("beforeSend");

        },
        cache: false,
        dataType: "json",
        success: function(data){
            // alert(new_drug_category_data);
            if (data.status === "ok"){
                $("#my_alert_box").append("<div class='alert alert-success alert-dismissable'><button aria-hidden='true' data-dismiss='alert' class='close' type='button'> × </button>Drug Category Successfuly saved. </div></div>");
                $("#new_drug_category_form")[0].reset();
            }
            if (data.status === "error"){
                $("#my_alert_box").append("<div class='alert alert-danger alert-dismissable'><button aria-hidden='true' data-dismiss='alert' class='close' type='button'> × </button> Error! Please check your data again </div></div>");

            }
            
        }
    });
    return false
});

    });