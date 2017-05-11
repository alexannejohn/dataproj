<filtering>
  

  <div class="filter-panel">
    <div class="title-frame">
      <h1>Filter by Student Details</h1>
      <span class="expand-button" onclick={ expand_hide } >+</span>
    </div>  
    <div class="filter-frame">
      <div each={ row, i in student_options }>
        <h2>{ row.title }</h2>
        <span each={ check, i in row.options} class="input-check">
          <input  data-message="{ row.field }" type="checkbox" name="{check.val}" value="{check.val}" onclick={ parent.update_to_filter }>
            <span class="tooltip">{check.val}
              <span if={ check.hover } class="tooltiptext">{ check.hover }</span>
            </span>
        </span>
      </div>
    </div>  
  </div>

  <div class="filter-panel">
    <div class="title-frame">
      <h1>Filter by Enrollment</h1>
      <span class="expand-button" onclick={ expand_hide } >+</span>
    </div>  
    <div class="filter-frame">
      <div each={ row, i in enroll_options }>
        <h2>{ row.title }</h2>
        <div each={ check, i in row.options} class={i > 15 ? 'input-check to-hide' : 'input-check'}>
          <input  data-message="{ row.field }" type="checkbox" name="{check.val}" value="{check.val}" onclick={ parent.update_to_filter }>
            <span class="tooltip">{check.val}
              <span if={ check.hover } class="tooltiptext">{ check.hover }</span>
            </span>
        </div>
      </div>
    </div>
  </div>


  <br>
  <br>
  <br>

  <script>
    var self = this;

    self.to_filter = {};

    url = "/filters"
    $.get(url, function (data) {
        self.enroll_options = data.enroll_options;
        self.student_options = data.student_options;
        self.update()
    });

    update_to_filter(e){
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
          self.enroll_options[3].options = data;
          self.update()
          delete self.to_filter['enroll_program']
        });
      }
    }

    expand_hide(e){
      if ($(e.target).text() == "+"){
        $(e.target).text("-");
      }else{
        $(e.target).text("+");
      }
      $(e.target).parent().siblings(".filter-frame").toggle()
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
    }

    .tooltip {
    position: relative;
    display: inline-block;
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
    /*.to-hide{
      display: none;
    }*/
  </style>
</filtering>