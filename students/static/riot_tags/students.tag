<students>
  <span class="student-count" if={ count }> { count } student<span if={count == 0 || count > 1 }>s</span></span>
  
  <div class="result-panel" if={ count > 0 }>
    <table class="student-table">
      <thead>
        <tr>
          <th></th>
          <th>Name</th>
          <th>Student #</th>
          <th>Program/Specialization</th>
          <th>Applications</th>
          <th>Graduation</th>
          <th>Awards</th>
        </tr>
      <thead>
      <tbody each={students}>
        <tr >
          <td onclick={ expand_hide } >+</td>
          <td>{ given_name }</td>
          <td>{ student_number }</td>
          <td>

              {recent_enrollment.session} - 
              <span if={!recent_enrollment.specialization_1}> {recent_enrollment.program}</span>
              <span>{recent_enrollment.specialization_1}</span>
              <span if={recent_enrollment.specialization_2}>, {recent_enrollment.specialization_2}</span>
              <br>

          </td>
          <td>{applied}
            <!-- <span each={app in applications}>
              {app.session} - 
              {app.program}
              <br>
            </span> -->
          </td>
          <td>{grad}
            <!-- <span each={grad in graduations}>
              {grad.ceremony_date} - 
              {grad.program}
              <br>
            </span> -->
          </td>
          <td>
            <span each={aw in awards}>
              {aw.session} - 
              {aw.award_title}
              <br>
            </span>
          </td>
        </tr>
        <tr class="student-details">

        </tr>
      <tbody>
    </table>
    <a href="/downloadcsv?{ numbers }">download csv</a>
  </div>

  <script>
    expand_hide(e){
      e.preventUpdate = true
      if ($(e.target).text() == "+"){
        $(e.target).text("-");
      }else{
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