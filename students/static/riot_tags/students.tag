<students>
  <span class="student-count" if={ count }> { count } student<span if={count == 0 || count > 1 }>s</span></span>
  
  <div class="result-panel" if={ count > 0 }>
    <table class="student-table">
      <thead>
        <tr>
          <th></th>
          <th>Name</th>
          <th>Student #</th>
          <th>Most recent Program/Specialization</th>
          <th>Graduation</th>
          <th>Applied</th>
          <th>Awards</th>
        </tr>
      <thead>
      <tbody each={students}>
        <tr >
          <td onclick={ student_detail } >+</td>
          <td>{ given_name }</td>
          <td>{ student_number }</td>
          <td>{ most_recent_enrollment}</td>
          <td>{ graduation_date }</td>
          <td>{ applied }</td>
          <td>{ total_award_amount }</td>
        </tr>
        <tr class="student-details"  >
          
            <td colspan="4" if={details} >{ details.given_name }</td>
      
          
        </tr>
      <tbody>
    </table>
    <a href="/downloadcsv?{ numbers }">download csv</a>
  </div>

  <script>

    var self = this;

    var arrayObjectIndexOf = function(myArray, searchTerm, property) {
        for(var i = 0, len = myArray.length; i < len; i++) {
            if (myArray[i][property] === searchTerm) return i;
        }
        return -1;
    }

    student_detail(e){
      index = arrayObjectIndexOf(self.students, e.item.student_number, 'student_number')
      e.preventUpdate = true
      if ($(e.target).text() == "+"){

        console.log(e);

        url = '/studentdetail?student_number=' + e.item.student_number;
        $.get(url, function (data) {
          self.students[index].details = data.student_details;
          self.update()
          console.log(data)
        });

        $(e.target).text("-");
      }else{
        delete self.students[index].details;
        $(e.target).text("+");
      }
      $(e.target).parent().siblings(".student-details").toggle()
    }

  </script>

  <style>
    .student-details{
      display: none;
      height:40px;
      border-bottom: solid #D9D9D9 1px;
    }
    .result-panel{
      width: 80%
      margin: 0 auto;
      background: #ffffff;
      min-height: 20px;
      box-shadow:2px 2px 5px 5px #C9C9C9;
      -webkit-box-shadow:2px 2px 5px 5x #C9C9C9;
      -moz-box-shadow:2px 2px 5px 5px #C9C9C9;
      margin: 10px;
      padding: 7px 8px 7px 3px;
      margin-bottom: 450px;
    }
    .student-count{
      color: #09839E;
      font-size: 18px;
      font-family: sans-serif;
      font-weight: bold;
      margin: 0;
      display: inline-block;
      margin-left: 20px;
      margin-top: 50px;
    }
    .student-table th{
      text-align: left;
      color: #09839E;
      font-size: 12px;
      font-family: sans-serif;
      min-width: 10px;
    }
    .student-table td{
      text-align: left;
      padding-left: 5px;
      padding-right: 10px;
      margin-bottom: 10px;
      color: #5B5C5C;
      font-size: 14px;
      font-family: sans-serif;
      /*border-bottom: solid #D9D9D9 1px;*/
    }
    .student-table tr{
      border-bottom: solid #D9D9D9 1px;
      border-top: solid #D9D9D9 2px;
    }
    table{
      border-collapse: collapse;
    }
  </style>

</students>