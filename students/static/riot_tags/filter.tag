<filtering>

  <div class="filter-panel">
    <select onchange= {enrollcsv}>
      <option value=""  >-session-</option>
      <option each={ session in enroll_sessions } value={session}  >{session}</option>
    </select>
    <a href="/enrollcsv?session={enroll_sess}">Enrollment CSV</a>

    <select onchange= {gradcsv}>
      <option value=""  >-year-</option>
      <option each={ year in grad_years } value={year}>{year}</option>
    </select>
    <a href="/gradcsv?year={grad_y}">Graduation CSV</a>
  </div>
  
  <div class="filter-panel" each={ filter in filters }>
    <div class="title-frame">
      <h1>{ filter.header }</h1>
      <span class="expand-button" onclick={ expand_hide } >+</span>
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
        <span class="expand-text" if={ row.options.length > 15 } onclick={expand_hide_options } >see more >><span>
      </div>

      <div if={filter.table =='award'} class="award_title">
        <h2>Award Title</h2>
        <span>
          <input  data-message="award_title" type="text" name="award_title" onchange={ update_search }>
        </span>
      </div>




    </div>  
  </div>

  <div class="filter-panel">
    <div class="title-frame">
      <h1>Search by Student Number</h1>
      <span class="expand-button" onclick={ expand_hide } >+</span>
    </div>  
    <div class="filter-frame">
        <span> Student number (exact): 
          <input  data-message="student_number" type="text" name="student_number" onchange={ update_search }>
        </span>
    </div>
  </div>



  <script>
    

    var self = this;

    self.to_filter = {};
    self.filters = {};
    self.filters.student_options = {"header": "Filter by Student Details", "table": "student"};
    self.filters.enroll_options = {"header": "Filter by Enrollment", "table": "enroll"};
    self.filters.application_options = {"header": "Filter by Applications", "table": "application"};
    self.filters.graduation_options = {"header": "Filter by Graduation", "table": "graduation"};
    self.filters.award_options = {"header": "Filter by Awards", "table": "award"}


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

    var arrayObjectIndexOf = function(myArray, searchTerm, property) {
        for(var i = 0, len = myArray.length; i < len; i++) {
            if (myArray[i][property] === searchTerm) return i;
        }
        return -1;
    }

    enrollcsv(e){
      var val = $(e.target).val()
      self.enroll_sess = val
    }

    gradcsv(e){
      var val = $(e.target).val()
      self.grad_y = val
    }

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

    update_to_filter(e){
      e.preventUpdate = true
      var checked = e.target.checked;
      var val = e.item.check.val;
      var field = e.target.dataset.message;
      
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

      if (field == 'enroll_program_type' || field == 'enroll_program_level'){
        url = '/enrollprogramtype?'
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
        url = '/enrollprogramtype?'
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
        url = '/enrollprogramtype?'
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

    expand_hide(e){
      e.preventUpdate = true
      if ($(e.target).text() == "+"){
        $(e.target).text("-");
      }else{
        $(e.target).text("+");
      }
      $(e.target).parent().siblings(".filter-frame").toggle()
    }

    expand_hide_options(e){
      e.preventUpdate = true
      if ($(e.target).text().includes("more")){
        $(e.target).text("<< see less");
        $(e.target).siblings(".to-hide").css("display", "inline-block")
      }else{
        $(e.target).text("see more >>");
        $(e.target).siblings(".to-hide").css("display", "none")
      }
      // $(e.target).siblings(".to-hide").toggle()
    }

  </script>

  <style>
    .filter-panel{
      width: 80%
      margin: 0 auto;
      background: #ffffff;
      min-height: 20px;
      box-shadow:2px 2px 5px 5px #C9C9C9;
      -webkit-box-shadow:2px 2px 5px 5x #C9C9C9;
      -moz-box-shadow:2px 2px 5px 5px #C9C9C9;
      margin: 10px;
      padding: 7px 12px;
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
    }
    .expand-button{
      color: #09839E;
      font-size: 16px;
      font-weight: bold;
      font-family: sans-serif;
      margin: 0 4px;
      display: inline-block;
    }
    .expand-button:hover{
      color: #0B3C75;
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
      width: 100px;
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
    /*display: inline-block;*/
    }

    /* Tooltip text */
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: black;
        color: #fff;
        text-align: center;
        padding: 5px 0;
        border-radius: 6px;
     
        /* Position the tooltip text - see examples below! */
        position: absolute;
        z-index: 1;
        width: 120px;
        bottom: 100%;
        left: 50%; 
        margin-left: -60px;
    }

    /* Show the tooltip text when you mouse over the tooltip container */
    .tooltip:hover .tooltiptext {
        visibility: visible;
    }
    .to-hide{
      display: none;
    }
  </style>
</filtering>