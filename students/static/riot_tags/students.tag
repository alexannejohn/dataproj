<students>
  <span class="student-count" if={ count }> { count } student<span if={count == 0 || count > 1 }>s</span></span>
  
  <div class="result-panel" if={ count > 0 }>
    <table class="student-table">
      <tr>
        <th></th>
        <th>Name</th>
        <th>Student #</th>
        <th>Program</th>
      </tr>
      <tr each={students}>
        <td>+</td>
        <td>{ given_name }</td>
        <td>{ student_number }</td>
        <td><span each={enroll in enrollments}>{enroll.session} - {enroll.program}<br></span></td>
      </tr>
    </table>
  </div>

  <script>

  </script>

  <style>
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
    }
    .student-table th{
      text-align: left;
      color: #09839E;
      font-size: 13px;
      font-family: sans-serif;
      min-width: 10px;
    }
    .student-table td{
      text-align: left;
      padding-left: 5px;
      padding-right: 25px;
      margin-bottom: 10px;
      color: #5B5C5C;
      font-size: 13px;
      font-family: sans-serif;
      /*border-bottom: solid #D9D9D9 1px;*/
    }
    .student-table tr{
      border-bottom: solid #D9D9D9 1px;
    }
    table{
      border-collapse: collapse;
    }
  </style>

</students>