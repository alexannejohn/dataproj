<filtering>
  <ul>
    <li each={ checkboxes }>{ title }
      <virtual each={options} >
        <input  data-message="{ parent.field }" type="checkbox" name="{val}" value="{val}" onclick={ parent.update_to_filter }>{val}
      </virtual>
    </li>
  </ul>

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

  </script>

  <style>
    :scope { font-size: 2rem }
    h3 { color: #444 }
    ul { color: #999 }
  </style>
</filtering>