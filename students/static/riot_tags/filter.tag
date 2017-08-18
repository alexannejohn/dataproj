<filtering>

<!-- download enrollment and graduation CSV's -->
  <div class="filter-panel no-border">
    <div class="set-inline-block">
      <select onchange= {enrollcsv}>
        <option value=""  >-session-</option>
        <option each={ session in enroll_sessions } value={session}  >{session}</option>
      </select>
    </div>
    <div class="set-inline-block">
      <img src="static/download-arrow-with-bar.svg" alt="download" height="30" width="30">
    </div>
    <div class="set-inline-block download-link">
      <a href="/enrollcsv?session={enroll_sess}">Enrollment CSV</a><br>
      <a href="/enrollcsv?health=true&session={enroll_sess}">Enrollment CSV - prof. programs</a>
    </div>

    <div class="set-inline-block">
      <select onchange= {gradcsv}>
        <option value=""  >-year-</option>
        <option each={ year in grad_years } value={year}>{year}</option>
      </select>
    </div>
    <div class="set-inline-block">
      <img src="static/download-arrow-with-bar.svg" alt="download" height="30" width="30">
    </div>
    <div class="set-inline-block download-link">
      <a href="/gradcsv?year={grad_y}">Graduation CSV</a><br>
      <a href="/gradcsv?health=true&year={grad_y}">Graduation CSV - prof. programs</a>
    </div>  
  </div>
  
  <!-- All the filter panels -->
  <div class="filter-panel" each={ filter in filters }>
    <div class="title-frame" onclick={ expand_hide } >
      <h1>{ filter.header }</h1>
      <span class="expand-button" >+</span>
    </div>  
    <div class="filter-frame">
      <div each={ row, i in filter.list } class="{ row.field }">
        <h2>{ row.title }</h2>
        
        <span each={ check, i in row.options} class={i > 14 ? 'input-check to-hide' : 'input-check'}>
          <input  data-message="{ row.field }" type="checkbox" name="{check.val}" value="{check.val}" onclick={ parent.update_to_filter }>
            <span class='tooltip'>
              {check.text ? check.text : check.val}
              <span if={ check.hover } class="tooltiptext">{ check.hover }</span>
            </span>
        </span>
        <span class="expand-text" if={ row.options.length > 15 } onclick={expand_hide_options } >see more >></span><br>
        <span data-message="{ row.field }" class="uncheck-all" onclick={uncheck_field}>uncheck all</span><br>
      </div>

      <div if={filter.table =='award'} class="award_title">
        <h2>Award Title</h2>
        <span>
          <input  data-message="award_title" type="text" name="award_title" onchange={ update_search }>
        </span>
      </div>
    </div>  
  </div>

<!-- and search by student number -->
  <div class="filter-panel">
    <div class="title-frame" onclick={ expand_hide }>
      <h1>Search by Student Number</h1>
      <span class="expand-button" >+</span>
    </div>  
    <div class="filter-frame">
        <span> Student number (must match exactly, separate multiple with commas): 
          <input  data-message="student_number" type="text" name="student_number" onchange={ update_search }>
        </span>
    </div>
  </div>

<!-- Saved searches panel -->
  <div class="filter-panel no-border">
    <div class="title-frame" onclick={ expand_hide }>
      <h1>Saved Searches</h1>
      <span class="expand-button" >+</span>
    </div>  
    <div class="filter-frame">
        <table>
          <tr each={search in saved_searches}>
            <td>{search.title}</td>
            <td>{search.created_on.substring(0,10)}</td>
            <td class="load-search" onclick={load_filter} >filter</td>
            <td class="load-search" onclick={load_filter_enrolled} >filter - enrolled only</td>
            <td class="delete-search" onclick={delete_search} >delete</td>
          </tr>
        </table>
    </div>
  </div>



  <script>
    

    var self = this;

    self.to_filter = {}; //Stores which filters are checked
    self.filters = {}; //all the the possible filter options
    self.filters.student_options = {"header": "Filter by Student Details", "table": "student"};
    self.filters.enroll_options = {"header": "Filter by Enrollment", "table": "enroll"};
    self.filters.application_options = {"header": "Filter by Applications", "table": "application"};
    self.filters.graduation_options = {"header": "Filter by Graduation", "table": "graduation"};
    self.filters.award_options = {"header": "Filter by Awards", "table": "award"}

    // load all the filter options
    url = "/filters"
    $.get(url, function (data) {
        self.filters.enroll_options.list = data.enroll_options;
        self.filters.student_options.list = data.student_options;
        self.filters.application_options.list = data.application_options;
        self.filters.graduation_options.list = data.graduation_options;
        self.filters.award_options.list = data.award_options;
        self.grad_years = data.grad_years;
        self.enroll_sessions = data.enroll_sessions;
        self.update()
    });

    // load list of previously saved searches
    url = "/getsearches/"
    $.get(url, function(data){
      self.saved_searches = data.searches
      self.update()
    });

    // helper function
    var arrayObjectIndexOf = function(myArray, searchTerm, property) {
        for(var i = 0, len = myArray.length; i < len; i++) {
            if (myArray[i][property] === searchTerm) return i;
        }
        return -1;
    }

    // execute a saved search - post_filter_students is defined in index.html
    load_filter(e){
      post_filter_students(JSON.stringify(e.item.search.search_json))
    }

    load_filter_enrolled(e){
      post_filter_students_enrolled(JSON.stringify(e.item.search.search_json))
    }

    // set url/button for downloading enrollment csv to specific session
    enrollcsv(e){
      var val = $(e.target).val()
      self.enroll_sess = val
    }

    // set url/button for downloading graduation csv to specific year
    gradcsv(e){
      var val = $(e.target).val()
      self.grad_y = val
    }


    // delete a saved search
    delete_search(e){
        var form = InitializeForm();
        form.append('id', e.item.search.id)
        var url = '/deletesearch/'
        var settings = getPostSettings(url, form);

        $.ajax(settings).done(function (response) {
            data = JSON.parse(response)
            self.saved_searches = data.searches;
            self.update()
        }).fail(function (jqXHR) {
            console.log(jqXHR);
        });
    }

    // used to update filters for text fields (student number, award title)
    update_search(e){
      e.preventUpdate = true
      var field = e.target.dataset.message;
      var val = $(e.target).val()
      if (val != ""){
        self.to_filter[field] = val
      }else{
        delete self.to_filter[field];
      }
    }


    // update program/specialization
    var update_program_spec = function(field){
      
      if (field == 'enroll_program_type' || field == 'enroll_program_level'){
        url = '/filterprogram?'
          url += 'type='
          if(self.to_filter['enroll_program_type']){
            url += (self.to_filter['enroll_program_type'].join() || '')
          }
          url += '&' 
          url += 'level='
          if(self.to_filter['enroll_program_level']){
            url += (self.to_filter['enroll_program_level'].join() || '')
          } 
          url += '&'
        $.get(url, function (data) {
          var index = arrayObjectIndexOf(self.filters.enroll_options.list, "enroll_program", "field")
          self.filters.enroll_options.list[index].options = data;
          self.update()
          delete self.to_filter['enroll_program']
          $('.enroll_program').find('.expand-text').text("<< see less");
          $('.enroll_program').children('.input-check').css("display", "inline-block")
        });
      }
      if (field == 'application_program_type' || field == 'application_program_level'){
        url = '/filterprogram?'
          url += 'type='
          if(self.to_filter['application_program_type']){
            url += (self.to_filter['application_program_type'].join() || '')
          }
          url += '&' 
          url += 'level='
          if(self.to_filter['application_program_level']){
            url += (self.to_filter['application_program_level'].join() || '')
          } 
          url += '&'
        $.get(url, function (data) {
          var index = arrayObjectIndexOf(self.filters.application_options.list, "application_program", "field")
          self.filters.application_options.list[index].options = data;
          self.update()
          delete self.to_filter['application_program']
          $('.application_program').find('.expand-text').text("<< see less");
          $('.application_program').children('.input-check').css("display", "inline-block")
        });
      }
      if (field == 'graduation_program_type' || field == 'graduation_program_level'){
        url = '/filterprogram?'
          url += 'type='
          if(self.to_filter['graduation_program_type']){
            url += (self.to_filter['graduation_program_type'].join() || '')
          }
          url += '&' 
          url += 'level='
          if(self.to_filter['graduation_program_level']){
            url += (self.to_filter['graduation_program_level'].join() || '')
          } 
          url += '&'
        $.get(url, function (data) {
          var index = arrayObjectIndexOf(self.filters.graduation_options.list, "graduation_program", "field")
          self.filters.graduation_options.list[index].options = data;
          self.update()
          delete self.to_filter['graduation_program']
          $('.graduation_program').find('.expand-text').text("<< see less");
          $('.graduation_program').children('.input-check').css("display", "inline-block")
        });
      }
      if (field == 'enroll_program' || field == 'enroll_subject'){
        url = '/filterspecialization?'
          url += 'program='
          if(self.to_filter['enroll_program']){
            url += (self.to_filter['enroll_program'].join() || '')
          }
          url += '&' 
          url += 'subject='
          if(self.to_filter['enroll_subject']){
            url += (self.to_filter['enroll_subject'].join() || '')
          } 
          url += '&'
        $.get(url, function (data) {
          var index = arrayObjectIndexOf(self.filters.enroll_options.list, "enroll_specialization", "field")
          self.filters.enroll_options.list[index].options = data;
          self.update()
          delete self.to_filter['enroll_specialization']
          $('.enroll_specialization').find('.expand-text').text("<< see less");
          $('.enroll_specialization').children('.input-check').css("display", "inline-block")
        });
      }
    }

    // called on every checkbox click. updates self.to_filter
    // depending on what is clicked, updates programs or specializations with filtered options
    update_to_filter(e){
      e.preventUpdate = true
      var checked = e.target.checked;
      var val = e.item.check.val;
      var field = e.target.dataset.message;
      
      // add/delete from to_filter
      if (checked == true){
        if (!self.to_filter[field]){
          self.to_filter[field] = []
        }
        self.to_filter[field].push(val)
      }
      else{
        var index = self.to_filter[field].indexOf(val);
        if (index > -1) {
           self.to_filter[field].splice(index, 1);
        }
        if (self.to_filter[field].length < 1){
          delete self.to_filter[field];
        }
      }

      update_program_spec(field)
    }

    //remove filters for one field
    uncheck_field(e){
      $(e.target).parent().find('input:checkbox:checked').prop('checked', false)
      var field = e.target.dataset.message;
      delete self.to_filter[field];
      update_program_spec(field)
    }

    // expands or hides filter panel
    expand_hide(e){
      e.preventUpdate = true
      var button = $($(e.target).children(".expand-button")[0])
      if (button.text() == "+"){
        button.text("-");
      }else{
        button.text("+");
      }
      $(e.target).siblings(".filter-frame").toggle()
    }

    // when many options, can expand/hide some of them
    expand_hide_options(e){
      e.preventUpdate = true
      if ($(e.target).text().includes("more")){
        $(e.target).text("<< see less");
        $(e.target).siblings(".to-hide").css("display", "inline-block")
      }else{
        $(e.target).text("see more >>");
        $(e.target).siblings(".to-hide").css("display", "none")
      }
    }

  </script>

  <style>
    .download-link{
      margin-right: 20px;
    }
    .download-link a{
      color: #09839E;
      font-style: italic;
      text-decoration: underline;
    }
    .download-link a:hover{
      color: #254299;
      font-style: italic;
      text-decoration: none;
    }
    .set-inline-block{
      display: inline-block;
      vertical-align: middle;
    }
    .filter-panel{
      width: 80%
      margin: 0 auto;
      background: #ffffff;
      min-height: 20px;
      box-shadow:1px 1px 2px 2px #C9C9C9;
      -webkit-box-shadow:1px 1px 2px 2px #C9C9C9;
      -moz-box-shadow:1px 1px 2px 2px #C9C9C9;
      margin: 12px;
      padding: 7px 12px;
      border-left: sienna 2px solid;
      font-family: sans-serif;
    }
    .filter-panel.no-border{
      border-left:none;
    }
    .filter-panel table td{
      padding-right: 15px;
      padding-left: 15px;
    }
    .filter-panel table td.load-search{
      color: darkblue;
      font-style: italic;
      text-decoration: underline;
    }
    .filter-panel table td.delete-search{
      color: red;
      font-style: italic;
      text-decoration: underline;
      padding-left: 30px;
      font-size: 11px;
    }
    .filter-panel table td.load-search:hover{
      color: black;
    }
    .filter-panel table td.delete-search:hover{
      color: black;
    }
    .title-frame{
      height: 20px;
      outline: 1px;
      margin: 2px;
    }
    .filter-frame{
      outline: 1px;
      margin: 2px;
      display: none;
    }
    .title-frame h1{
      color: #09839E;
      font-size: 16px;
      font-family: sans-serif;
      margin: 0;
      display: inline-block;
      pointer-events: none;
    }
    .expand-button{
      color: #09839E;
      font-size: 16px;
      font-weight: bold;
      font-family: sans-serif;
      margin: 0 4px;
      display: inline-block;
      pointer-events: none;
    }
    .expand-text{
      color: #09839E;
      font-size: 14px;
      font-family: sans-serif;
      margin: 0 4px;
      display: inline-block;
    }
    .expand-text:hover{
      color: #0B3C75;
    }
    .uncheck-all{
      color: #09839E;
      font-size: 12px;
      font-family: sans-serif;
      margin: 0 4px;
      display: inline-block;
      font-style: italic;
    }
    .uncheck-all:hover{
      color: #0B3C75;
    }
    .filter-frame h2{
      font-family: sans-serif;
      font-size: 14px;
      color: #B5B5B5;
      margin: 8px 0 3px 0;
      border-bottom: solid #D9D9D9 1px;
    }
    .input-check{
      margin: 0 3px;
      font-family: sans-serif;
      display: inline-block;
      width: 110px;
      vertical-align: top;
    }
    .enroll_specialization .input-check{
      font-size: 13px;
      width: 320px;
    }
    .student_self_id .input-check{
      width: 120px;
    }

    .tooltip {
    position: relative;
    vertical-align: text-bottom;
    }

    .tooltip .tooltiptext {
      visibility: hidden;
      width: 120px;
      background-color: black;
      color: #fff;
      text-align: center;
      padding: 5px 0;
      border-radius: 6px;
      position: absolute;
      z-index: 1;
      width: 120px;
      bottom: 100%;
      left: 50%; 
      margin-left: -60px;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
    }
    .to-hide{
      display: none;
    }
    input[type=checkbox]{
      -webkit-appearance: none;
      background-color: #fafafa;
      border: 1px solid #cacece;
      padding: 8px;
      display: inline-block;
      position: relative;
      vertical-align: bottom;
    }

    input[type=checkbox]:checked {
      background-color: sienna;
    }

    input[type=checkbox]:focus{
      outline: none;
    }


  </style>
</filtering>