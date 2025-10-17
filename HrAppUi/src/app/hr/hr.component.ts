import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MsalService } from '@azure/msal-angular';
import { AuthenticationResult } from "@azure/msal-browser";
import { environment } from '../../Enviroments/enviroments';

@Component({
  selector: 'app-hr',
  templateUrl: './hr.component.html',
  styleUrl: './hr.component.css'
})
export class HrComponent {
IsLoading: any;
searchData: any;
dimensions: any = [];
selectedFile: any = null;
liness: any = [];
data: any;
file_names: any;
names: any;
glAcc: any;
showOptions: any = false;
userEmail: any;
user_department: any;
beingViewedFile: any;
approvals: any = [];
actions: any;
chartOfAccounts: any = [];
seledctedTransactions: any = [];
constructor(private http: HttpClient, private router: Router, private msalService: MsalService){}

ngOnInit(): void {
  //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
  //Add 'implements OnInit' to the class.

    this.IsLoading = true;
    if (this.msalService.instance.getActiveAccount() != null) {
        this.userEmail = this.msalService.instance.getActiveAccount()?.username;
        let jsonObject: any = { Email: this.userEmail };
        this.http.put(environment.BackEndUrl + 'login/', jsonObject).subscribe((response) => {
          this.user_department = response;



        this.http.get(environment.BackEndUrl + 'get-ca/').subscribe(
          (response) => {
            this.chartOfAccounts = response;

            this.IsLoading = false;
          },
        (err) => {
          alert("Couldn't Retrieve Chart of Accounts")
        })


        this.http.get(environment.BackEndUrl + 'get-dim/').subscribe(
          (response) => {
            this.dimensions = response;
          })

        this.http.get(environment.BackEndUrl + 'get-files/').subscribe((response) => {
          this.file_names = response;
          this.names = this.file_names.Files
        },
      (err)=>{
        console.log(err)
      });
    });
        }else {
      alert("Login First Please")
      this.router.navigate([""]);
  }
  this.msalService.handleRedirectObservable().subscribe({
      next: (result: AuthenticationResult) => {},
      error: (error) => console.log(error),
  });
}

onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    this.selectedFile = input.files[0];
  } else {
    console.error('No file selected or file input is null.');
  }
}

onUpload() {

  const formData = new FormData();
  formData.append('file', this.selectedFile, this.selectedFile.name);
  formData.append('file_name', this.selectedFile.name);
  this.http.post(environment.BackEndUrl + 'upload/', formData).subscribe(
    (response) => {
      this.IsLoading = true;
      let body = {
        excelSheetName : this.selectedFile.name
      }
      this.http.post(environment.BackEndUrl + 'excel/', body).subscribe((response) => {
        this.data = response;
        this.liness = this.data.lines
        this.beingViewedFile = this.selectedFile.name
        this.IsLoading = false
        this.selectedFile = null;
        this.http.get(environment.BackEndUrl + 'get-files/').subscribe((response) => {
          this.file_names = response;
          this.names = this.file_names.Files
        },
      (err)=>{
        console.log(err)
      });

      },

      (error) => {console.error(error); this.IsLoading = false})

    },
    (error) => {console.error(error); this.IsLoading = false}
  );
}


readFilesLines(fileName: string) {
  let body = {
    excelSheetName : fileName
  }
  this.IsLoading = true;
  this.http.post(environment.BackEndUrl + 'excel/', body).subscribe((response) => {
    this.data = response;
    this.liness = this.data.lines
    this.IsLoading = false
    this.selectedFile = null;
  }, (err) => {
    alert("File Does Not Exists.")
    this.IsLoading = false;
    this.liness = [];
  });
}


approveFile(fileName: string, userEmail: string){
  let body = {
    excelSheetName : fileName,
    userEmail : userEmail
  }
  this.IsLoading = true;
  this.http.post(environment.BackEndUrl + 'approve/', body).subscribe((response)=>{
    this.IsLoading = false;
    alert("File Approved.")
    this.getFileApprovals()
  }, (err)=> {
    alert("File Not Approved.")
  });
}

getFileApprovals(){
  let body = {
    excelSheetName : this.beingViewedFile,
  }
  this.http.put(environment.BackEndUrl + 'approve/', body).subscribe((response)=>{
    this.IsLoading = false;
    this.actions = response
    this.approvals = this.actions.actions
    console.log(this.approvals)
  }, (err)=> {
    alert("something went wrong")
  });
}

captureCheckboxValue(value: any) {
  if (this.seledctedTransactions.includes(value)) {
      let index = this.seledctedTransactions.indexOf(value);
      this.seledctedTransactions.splice(index, 1);
  } else {
      this.seledctedTransactions.push(value);
  }
  if (this.seledctedTransactions.length < 1) {
      this.seledctedTransactions = [];
  }
  console.log("hi  ", this.seledctedTransactions);
}

setGLAccount2(listOfTransactions: [], GLAccount: String) {

}

logout() {
  sessionStorage.clear();
  this.msalService.logout();
}


}
