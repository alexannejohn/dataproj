<students>
  <!-- shows number of students returned by query -->
  <span class="student-count" if={ count || count==0 }> { count } student<span if={count == 0 || count > 1 }>s</span></span>
  <span if={count > 1000 }> Try limiting your query </span>

  <!-- button to download CSV of students -->
  <div if={ count > 0  && numbers } class="download-link">
    <img src="static/download-arrow-with-bar.svg" alt="download" height="15" width="15">
    <a  href="/downloadcsv?{ numbers }">download csv</a>
  </div>
  
  <!-- table of students -->
  <div class="result-panel" if={ count && numbers}>
    <table class="student-table" if={ count > 0 }>
      <thead>
        <tr>
          <th></th>
          <th>Name</th>
          <th>Student #</th>
          <th>Most recent Program/Specialization</th>
          <th>Sponsorship</th>
          <th>Sponsor</th>
          <th>Graduation</th>
        </tr>
      <thead>
      <tbody each={students}>
        <tr >
          <td onclick={ student_detail } >+</td>  <!-- expand student -->
          <td>{ given_name }</td>
          <td>{ student_number }</td>
          <td>{ most_recent_enrollment}</td>
          <td><span if={ sponsorship }>Yes</span><span if={ !sponsorship }>No</span></td>
          <td>{ sponsor }</td>
          <td>{ graduation_date }</td>
        </tr>
        <tr class="student-details"  > <!-- detailed info for student -->
          
            <td colspan="7" if={details} >
              <div class="student-section">

                <h2>Student Details</h2>
                  <table>
                    <tr>
                      <th>given name</th>
                      <th>surname</th>
                      <th>preferred name</th>
                      <th>student number</th>
                      <th>gender</th>
                      <th>birthdate</th>
                      <th>self-ID</th>
                      <th>city</th>
                      <th>province</th>
                      <th>country</th>
                      <th>financial_hold</th>
                      <th>sponsorship</th>
                      <th>sponsor</th>
                    </tr>
                    <tr>
                      <td>{ details.given_name }</td>
                      <td>{ details.surname }</td>
                      <td>{ details.preferred_name }</td>
                      <td>{ details.student_number }</td>
                      <td>{ details.gender }</td>
                      <td>{ details.birthdate }</td>
                      <td>{ details.self_id }</td>
                      <td>{ details.city }</td>
                      <td>{ details.province }</td>
                      <td>{ details.country }</td>
                      <td><span if={ details.financial_hold }>Yes</span><span if={ !details.financial_hold }>No</span></td>
                      <td><span if={ details.sponsorship }>Yes</span><span if={ !details.sponsorship }>No</span></td>
                      <td>{ details.sponsor }</td>

                    </tr>
                  </table>

                <h2>Previous Institutions</h2>
                  <table if={details.previous_institutions.length > 0}>
                    <tr>
                      <th>institution name</th>
                      <th>transfer credits</th>
                    </tr>
                    <tr each = {pi in details.previous_institutions}>
                      <td>{ pi.institution_name }</td>
                      <td> { pi.transfer_credits }</td>
                    </tr>
                  </table>
                

                <h2>Applications</h2>
                  <table if={details.applications.length > 0}>
                    <tr>
                      <th>session</th>
                      <th>program</th>
                      <th>year lvl</th>
                      <th>re-admission</th>
                      <th>status</th>
                      <th>reason</th>
                      <th>decision</th>
                      <th>action code</th>
                      <th>mult. action</th>

                    </tr>
                    <tr each = {app in details.applications} >
                      <td>{ app.session }</td>
                      <td> { app.program }</td>
                      <td> { app.year_level }</td>
                      <td> { app.re_admission }</td>
                      <td> { app.status }</td>
                      <td> { app.reason }</td>
                      <td> { app.applicant_decision }</td>
                      <td> { app.action_code }</td>
                      <td> { app.multiple_action }</td>
                    </tr>
                  </table>


                <h2>Enrollment</h2>
                  <table if={details.enrolls.length > 0}>
                    <tr>
                      <th>session</th>
                      <th>program</th>
                      <th>specialization 1</th>
                      <th>specialization 2</th>
                      <th>year</th>
                      <th>Reg. Status</th>
                      <th>Standing</th>
                      <th>Average</th>
                    </tr>
                    <tr each = {enroll in details.enrolls} >
                      <td>{ enroll.session }</td>
                      <td> { enroll.program }</td>
                      <td> { enroll.specialization_1 }</td>
                      <td> { enroll.specialization_2 }</td>
                      <td> { enroll.year_level }</td>
                      <td> { enroll.regi_status }</td>
                      <td> { enroll.sessional_standing }</td>
                      <td> { enroll.sessional_average }</td>
                    </tr>
                  </table>

                <h2>Graduation</h2>
                  <table if={details.graduations.length > 0}>
                    <tr>
                      <th>program</th>
                      <th>specialization 1</th>
                      <th>specialization 2</th>
                      <th>conferral period year</th>
                      <th>month</th>
                      <th>status</th>
                      <th>reason</th>
                      <th>doctoral citation</th>
                      <th>dual degree</th>
                      <th>ceremony date</th>
                    </tr>
                    <tr each = {grad in details.graduations} >
                      <td>{ grad.program }</td>
                      <td> { grad.specialization_1 }</td>
                      <td> { grad.specialization_2 }</td>
                      <td> { grad.conferral_period_year }</td>
                      <td> { grad.conferral_period_month }</td>
                      <td> { grad.grad_application_status }</td>
                      <td> { grad.status_reason }</td>
                      <td> { grad.doctoral_citation }</td>
                      <td> { grad.dual_degree }</td>
                      <td> { grad.ceremony_date }</td>
                    </tr>
                  </table>


                <h2>Awards</h2>
                  <table if={details.awards.length > 0}>
                    <tr>
                      <th>session</th>
                      <th>award title</th>
                      <th>Award Amount</th>
                      <th>Award type</th>
                      <th>status</th>
                    </tr>
                    <tr each = {award in details.awards} >
                      <td>{ award.session }</td>
                      <td> { award.award_title }</td>
                      <td> { award.award_amount }</td>
                      <td> { award.award_type }</td>
                      <td> { award.status }</td>
                    </tr>
                  </table>


              </div>
            
            </td>
      
          
        </tr>
      <tbody>
    </table>
    <!-- paginated list - next and previous buttons -->
    <span if={links} class="next-prev">
      <button data-message="{ links.previous }" disabled="{!links.previous}"  onclick={page_next}>previous</button>
      <button data-message="{ links.next }" disabled="{!links.next}" onclick={page_next}>next</button>
    </span>
  </div>

  <!-- map! -->
  <div class="mapping" if= { count && numbers}>
      <button class="map-button" onclick="setmap()">View on Map</button>
      <div id="mapid"></div>
  </div>

  <script>
    // so can reference self (riot tag object) within other functions
    var self = this;

    // helper functions
    var arrayObjectIndexOf = function(myArray, searchTerm, property) {
        for(var i = 0, len = myArray.length; i < len; i++) {
            if (myArray[i][property] === searchTerm) return i;
        }
        return -1;
    }

    // go to next or previous page of results
    page_next(e){
      var form = InitializeForm();
      form.append('filters', JSON.stringify(filter_form.to_filter))
      var url = e.target.dataset.message;
      var settings = getPostSettings(url, form);

      $.ajax(settings).done(function (response) {
          data = JSON.parse(response)
          self.students = data.students
          self.count = data.count
          self.numbers = data.numbers
          self.links = data.links
          self.update();
      }).fail(function (jqXHR) {
          console.log(jqXHR);
      });
    }

    // load detailed info for student
    student_detail(e){
      index = arrayObjectIndexOf(self.students, e.item.student_number, 'student_number')
      e.preventUpdate = true
      if ($(e.target).text() == "+"){
        url = '/studentdetail?student_number=' + e.item.student_number;
        $.get(url, function (data) {
          self.students[index].details = data.student_details;
          self.update()
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
    .download-link{
      display: inline-block;
    }
    .download-link img{
      margin-bottom: -3px;
    }
    .download-link a{
      margin-bottom: 4px;
      color: #09839E;
      font-style: italic;
      text-decoration: underline;
    }
    .download-link a:hover{
      color: #254299;
      font-style: italic;
      text-decoration: none;
    }
    .student-details{
      display: none;
      height:40px;
      border-bottom: solid #D9D9D9 1px;
    }
    .result-panel{
      width: 80%
      margin: 0 auto;
      background: #ffffff;
      box-shadow:2px 2px 5px 5px #C9C9C9;
      -webkit-box-shadow:2px 2px 5px 5x #C9C9C9;
      -moz-box-shadow:2px 2px 5px 5px #C9C9C9;
      margin: 10px;
      padding: 7px 8px 7px 3px;
      margin-bottom: 20px;
      border-right: sienna 1px solid;
      border-bottom: sienna 1px solid;
    }
    .student-count{
      color: #09839E;
      font-size: 18px;
      font-family: sans-serif;
      font-weight: bold;
      margin: 0;
      display: inline-block;
      margin-left: 40px;
      margin-top: 50px;
      margin-right: 30px;
    }
    .student-table th{
      color: #09839E;
      font-size: 12px;
      font-family: sans-serif;
      min-width: 10px;
      padding-left: 5px;
      padding-right: 10px;
      text-transform: lowercase;
      text-align: left;
    }
    .student-table td{
      text-align: left;
      padding-left: 5px;
      padding-right: 10px;
      margin-bottom: 10px;
      color: #5B5C5C;
      font-size: 14px;
      font-family: sans-serif;
      padding-top: 4px;
      padding-bottom: 4px;
    }
    .student-table tr{
      border-bottom: solid #EDEDED 1px;
    }
    .student-table tbody:nth-last-child(2) tr{
      border-bottom: none;
    }
    .student-table{
      margin-bottom: 10px;
      width: 100%
    }
    table{
      border-collapse: collapse;
    }
    h2{
      font-family: sans-serif;
      font-size: 12px;
      color: #B5B5B5;
      margin: 8px 0 3px 0;
      border-bottom: solid #D9D9D9 1px;
    }
    .student-section th{
      text-align: center;
      color: #636363;
      text-transform: uppercase;
      font-size: 8px;
      font-family: sans-serif;
      min-width: 10px;
      vertical-align: top;
      padding-left: 5px;
      padding-right: 5px;
    }
    .student-section td{
      text-align: center;
      padding-left: 5px;
      padding-right: 10px;
      margin-bottom: 10px;
      color: #5B5C5C;
      font-size: 14px;
      font-family: sans-serif;
    }
    .student-section tr{
      border-bottom: none;
      border-top: none;
    }
    .student-section{
      padding-left: 10px;
      margin-bottom: 30px;
      margin-top: 20px;
    }
    .student-section table{
      margin-left: 20px;
    }
    .next-prev button {
      padding: 3px;
      font-size: 14px;
    }
    .next-prev button:disabled{
      opacity: 0.5
    }
    #mapid{ 
        width: 80%;
        margin: auto;
        height: 580px;
        display: None;
        border: 3px solid grey;
        border-radius: 3px;
        margin-top: 30px;
    }
    .map-button{
        margin-left: 10px;
    }
  </style>

</students>