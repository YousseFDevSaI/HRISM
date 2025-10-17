import { LoginComponent } from './login/login.component';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from "@angular/common/http";
import { RouterModule } from "@angular/router";
import { MsalModule, MsalService, MSAL_INSTANCE } from "@azure/msal-angular";
import { IPublicClientApplication, PublicClientApplication, InteractionType, BrowserCacheLocation } from "@azure/msal-browser";
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HrComponent } from './hr/hr.component';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';


export function MSALInstanceFactory(): IPublicClientApplication{
  return new PublicClientApplication({
    auth:{
      clientId:'523aadb8-62c1-42be-810f-cf75ac0a32e2',
      redirectUri:'http://localhost:4200/',
      authority:'https://login.microsoftonline.com/159d77ac-d095-413e-a321-88480be90067'

    },
    cache:{
      cacheLocation:'localStorage',
      storeAuthStateInCookie:false
    }
  })
}
@NgModule({
  declarations: [
    AppComponent,
    HrComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MsalModule,
    FormsModule,
    RouterModule.forRoot([
      { path: "Service", component: HrComponent },
      { path: "",  component: LoginComponent }
    ])
  ],
  providers: [
    DatePipe,
    {

    provide: MSAL_INSTANCE,
    useFactory: MSALInstanceFactory
  },MsalService],
  bootstrap: [AppComponent]
})
export class AppModule { }
