var selected_movies = [];
    $(document).ready(function() {
        $('#tbl_movies').DataTable();
    });
    
    $(document).on('click','[name="title"]',function(){
        if($(this).is(':checked')){
            selected_movies.push($(this).data('title'));
        }
        else{
            var index = selected_movies.indexOf($(this).data('title'));
            if(index >-1){
                selected_movies.splice(index,1)
            }
        }
        
        var badges = '';

        $.each(selected_movies,function(i,val){
            badges+='<span class="badge badge-secondary text-capitalize">'+val+' <span class="badge badge-light delete-title" data-id="'+val+'">x</span></span> ';
        });

        console.log(selected_movies);
        $('#badges_titles').html(badges);
    });

    $(document).on('click','.delete-title',function(){
        var id = $(this).data('id');
        $('#'+id).prop('checked',false);
        var index = selected_movies.indexOf(id);
        if(index >-1){
            selected_movies.splice(index,1)
        }

        var badges = '';

        $.each(selected_movies,function(i,val){
            badges+='<span class="badge badge-secondary text-capitalize">'+val+' <span class="badge badge-light delete-title" data-id="'+val+'">x</span></span> ';
        });

        console.log(selected_movies);
        $('#badges_titles').html(badges);
    });
