<filtering>
  

  <div class="filter-panel">
    <div class="title-frame">
      <h1>Filter by Enrollment</h1>
      <span class="expand-button" onclick={ expand_hide } >+</span>
    </div>  
    <div class="filter-frame">
      <div each={ checkboxes }>
        <h2>{ title }</h2>
        <span each={options} class="input-check">
          <input  data-message="{ parent.field }" type="checkbox" name="{val}" value="{val}" onclick={ parent.update_to_filter }>{val}
        </span>
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
        self.checkboxes = data;
        self.update()
    });

    update_to_filter(e){
      var checked = e.target.checked;
      var val = e.item.val;
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
    }

    expand_hide(e){
      console.log($(e.target).text())
      console.log($(e.target).parent().siblings(".filter-frame"))
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
    }
  </style>
</filtering>