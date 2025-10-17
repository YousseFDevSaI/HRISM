import { Component, OnInit, NgModule } from "@angular/core";
import { MsalBroadcastService, MsalService } from "@azure/msal-angular";
import { Router } from "@angular/router";
import { AuthenticationResult } from "@azure/msal-browser";
import { environment } from "../../Enviroments/enviroments";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { GlobalvService } from "../globalv.service";



@Component({
    selector: "app-login",
    templateUrl: "./login.component.html",
    styleUrls: ["./login.component.css"],
})
export class LoginComponent implements OnInit {
    IsLoggedIn = false;
    IsLoading = false;
    obj: any;
    User_details: any = {};
    section: any;
    input_otp: any;
    exisitanceStatus: any = {};
    login_stat: any = {};
    timeLeft: any;
    otpgen: any;
    User_email_obj: any;

    constructor(private gservice: GlobalvService, private http: HttpClient, private router: Router, private msalService: MsalService, private msalBroadcastService: MsalBroadcastService) {}
    ngOnInit(): void {
        this.IsLoading = false;
        this.set_section('login')


        this.msalService.handleRedirectObservable().subscribe({
            next: (result: AuthenticationResult) => {
                if (result != null && result.account != null) {
                    this.IsLoading = true;
                    this.gservice.setEmail(result.account.username);
                    this.msalService.instance.setActiveAccount(result.account);
                    const httpOptions: Object = {
                        headers: new HttpHeaders({
                            Authorization: "Bearer " + result.accessToken,
                        }),
                        responseType: "blob",
                    };
                    this.obj = {
                Email: this.msalService.instance.getActiveAccount()?.username,
            };
                    const objectIdOrUpn = result.account.username;
                    this.http.get<any>(`https://graph.microsoft.com/v1.0/users/${objectIdOrUpn}/photo/$value`, httpOptions).subscribe(
                        (blob: Blob) => {
                            sessionStorage.setItem("PIM", URL.createObjectURL(blob));
                            this.http.post<any>(environment.BackEndUrl + "login/", this.obj, { headers: headers }).subscribe(
                                (response) => {
                                    if (response["Status"] == "User Exist") {
                                        this.router.navigate(["Service"]);
                                    } else {
                                        alert("User Not Registred Please Contact Our Support Team.");
                                        this.IsLoading = true;
                                        this.msalService.logout();
                                    }
                                },
                                (error) => {
                                  this.IsLoading = true;
                                  alert("Error Occured Please Contact Our Support Team.")
                                  this.msalService.logout()
                                }
                            );
                        }
                    );

                    const headers = new HttpHeaders({ "Content-Type": "application/json" });
                    var obj = {
                        Email: result.account.username,
                    };
                }
            },
            error: (error) => {
                alert("Error While Uthanticating User From Outlook");
                this.msalService.logout();
                sessionStorage.clear();
            },
        });
    }

    login() {
        this.IsLoading = true;
        this.msalService.loginRedirect({
            scopes: ["user.read"], // Scopes for the token
        });
    }

    set_section(view: string) {
      this.section = view
    }















}
